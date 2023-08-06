import asyncio
import functools
import logging
import signal
import threading
import warnings
from typing import Optional, Callable, Collection

from kopf.engines import peering
from kopf.engines import posting
from kopf.reactor import handling
from kopf.reactor import lifecycles
from kopf.reactor import queueing
from kopf.reactor import registries

logger = logging.getLogger(__name__)


def run(
        loop: Optional[asyncio.AbstractEventLoop] = None,
        lifecycle: Optional[Callable] = None,
        registry: Optional[registries.GlobalRegistry] = None,
        standalone: bool = False,
        priority: int = 0,
        peering_name: Optional[str] = None,
        namespace: Optional[str] = None,
):
    """
    Run the whole operator synchronously.

    This function should be used to run an operator in normal sync mode.
    """
    loop = loop if loop is not None else asyncio.get_event_loop()
    try:
        loop.run_until_complete(operator(
            lifecycle=lifecycle,
            registry=registry,
            standalone=standalone,
            namespace=namespace,
            priority=priority,
            peering_name=peering_name,
        ))
    except asyncio.CancelledError:
        pass


async def operator(
        lifecycle: Optional[Callable] = None,
        registry: Optional[registries.GlobalRegistry] = None,
        standalone: bool = False,
        priority: int = 0,
        peering_name: Optional[str] = None,
        namespace: Optional[str] = None,
):
    """
    Run the whole operator asynchronously.

    This function should be used to run an operator in an asyncio event-loop
    if the operator is orchestrated explicitly and manually.

    It is efficiently `spawn_tasks` + `run_tasks` with some safety.
    """
    existing_tasks = await _all_tasks()
    operator_tasks = await spawn_tasks(
        lifecycle=lifecycle,
        registry=registry,
        standalone=standalone,
        namespace=namespace,
        priority=priority,
        peering_name=peering_name,
    )
    await run_tasks(operator_tasks, ignored=existing_tasks)


async def spawn_tasks(
        lifecycle: Optional[Callable] = None,
        registry: Optional[registries.GlobalRegistry] = None,
        standalone: bool = False,
        priority: int = 0,
        peering_name: Optional[str] = None,
        namespace: Optional[str] = None,
) -> Collection[asyncio.Task]:
    """
    Spawn all the tasks needed to run the operator.

    The tasks are properly inter-connected with the synchronisation primitives.
    """
    loop = asyncio.get_running_loop()

    # The freezer and the registry are scoped to this whole task-set, to sync them all.
    lifecycle = lifecycle if lifecycle is not None else lifecycles.get_default_lifecycle()
    registry = registry if registry is not None else registries.get_default_registry()
    event_queue = asyncio.Queue(loop=loop)
    freeze_flag = asyncio.Event(loop=loop)
    should_stop = asyncio.Event(loop=loop)
    tasks = []

    # A top-level task for external stopping by setting a stop-flag. Once set,
    # this task will exit, and thus all other top-level tasks will be cancelled.
    tasks.extend([
        loop.create_task(_stop_flag_checker(should_stop)),
    ])

    # K8s-event posting. Events are queued in-memory and posted in the background.
    # NB: currently, it is a global task, but can be made per-resource or per-object.
    tasks.extend([
        loop.create_task(posting.poster(
            event_queue=event_queue)),
    ])

    # Monitor the peers, unless explicitly disabled.
    ourselves: Optional[peering.Peer] = peering.Peer.detect(
        id=peering.detect_own_id(), priority=priority,
        standalone=standalone, namespace=namespace, name=peering_name,
    )
    if ourselves:
        tasks.extend([
            loop.create_task(peering.peers_keepalive(
                ourselves=ourselves)),
            loop.create_task(queueing.watcher(
                namespace=namespace,
                resource=ourselves.resource,
                handler=functools.partial(peering.peers_handler,
                                          ourselves=ourselves,
                                          freeze=freeze_flag))),  # freeze is set/cleared
        ])

    # Resource event handling, only once for every known resource (de-duplicated).
    for resource in registry.resources:
        tasks.extend([
            loop.create_task(queueing.watcher(
                namespace=namespace,
                resource=resource,
                handler=functools.partial(handling.custom_object_handler,
                                          lifecycle=lifecycle,
                                          registry=registry,
                                          resource=resource,
                                          event_queue=event_queue,
                                          freeze=freeze_flag))),  # freeze is only checked
        ])

    # On Ctrl+C or pod termination, cancel all tasks gracefully.
    if threading.current_thread() is threading.main_thread():
        loop.add_signal_handler(signal.SIGINT, should_stop.set)
        loop.add_signal_handler(signal.SIGTERM, should_stop.set)
    else:
        logger.warning("OS signals are ignored: running not in the main thread.")

    return tasks


async def run_tasks(root_tasks, *, ignored: Collection[asyncio.Task] = frozenset()):
    """
    Orchestrate the tasks and terminate them gracefully when needed.

    The root tasks are expected to run forever. Their number is limited. Once
    any of them exits, the whole operator and all other root tasks should exit.

    The root tasks, in turn, can spawn multiple sub-tasks of various purposes.
    They can be awaited, monitored, or fired-and-forgot.

    The hung tasks are those that were spawned during the operator runtime,
    and were not cancelled/exited on the root tasks termination. They are given
    some extra time to finish, after which they are forcely terminated too.

    .. note::
        Due to implementation details, every task created after the operator's
        startup is assumed to be a task or a sub-task of the operator.
        In the end, all tasks are forcely cancelled. Even if those tasks were
        created by other means. There is no way to trace who spawned what.
        Only the tasks that existed before the operator startup are ignored
        (for example, those that spawned the operator itself).
    """
    try:
        # Run the infinite tasks until one of them fails/exits (they never exit normally).
        root_done, root_pending = await _wait(root_tasks, return_when=asyncio.FIRST_COMPLETED)
    except asyncio.CancelledError:
        # If the operator is cancelled, propagate the cancellation to all the sub-tasks.
        # There is no graceful period: cancel as soon as possible, but allow them to finish.
        root_cancelled, root_left = await _stop(root_tasks, title="Root", cancelled=True)
        hung_tasks = await _all_tasks(ignored=ignored)
        hung_cancelled, hung_left = await _stop(hung_tasks, title="Hung", cancelled=True)
        raise
    else:
        # If the operator is intact, but one of the root tasks has exited (successfully or not),
        # cancel all the remaining root tasks, and gracefully exit other spawned sub-tasks.
        root_cancelled, root_left = await _stop(root_pending, title="Root", cancelled=False)
        hung_tasks = await _all_tasks(ignored=ignored)
        try:
            # After the root tasks are all gone, cancel any spawned sub-tasks (e.g. handlers).
            # TODO: assumption! the loop is not fully ours! find a way to cancel our spawned tasks.
            hung_done, hung_pending = await _wait(hung_tasks, timeout=5.0)
        except asyncio.CancelledError:
            # If the operator is cancelled, propagate the cancellation to all the sub-tasks.
            hung_cancelled, hung_left = await _stop(hung_tasks, title="Hung", cancelled=True)
            raise
        else:
            # If the operator is intact, but the timeout is reached, forcely cancel the sub-tasks.
            hung_cancelled, hung_left = await _stop(hung_pending, title="Hung", cancelled=False)

    # If succeeded or if cancellation is silenced, re-raise from failed tasks (if any).
    await _reraise(root_done | root_cancelled | hung_done | hung_cancelled)


async def _all_tasks(ignored: Collection[asyncio.Task] = frozenset()) -> Collection[asyncio.Task]:
    current_task = asyncio.current_task()
    return {task for task in asyncio.all_tasks()
            if task is not current_task and task not in ignored}


async def _wait(tasks, *, timeout=None, return_when=asyncio.ALL_COMPLETED):
    if not tasks:
        return set(), ()
    done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=return_when)
    return done, pending


async def _stop(tasks, title, cancelled):
    if not tasks:
        logger.debug(f"{title} tasks stopping is skipped: no tasks given.")
        return set(), set()

    for task in tasks:
        task.cancel()

    # If the waiting (current) task is cancelled before the wait is over,
    # propagate the cancellation to all the awaited (sub-) tasks, and let them finish.
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    except asyncio.CancelledError:
        # If the waiting (current) task is cancelled while propagating the cancellation
        # (i.e. double-cancelled), let it fail without graceful cleanup. It is urgent, it seems.
        pending = {task for task in tasks if not task.done()}
        are = 'are' if not pending else 'are not'
        why = 'double-cancelled at stopping' if cancelled else 'cancelled at stopping'
        logger.debug(f"{title} tasks {are} stopped: {why}; tasks left: {pending!r}")
        raise  # the repeated cancellation, handled specially.
    else:
        # If the cancellation is propagated normally and the awaited (sub-) tasks exited,
        # consider it as a successful cleanup.
        are = 'are' if not pending else 'are not'
        why = 'cancelled normally' if cancelled else 'finished normally'
        logger.debug(f"{title} tasks {are} stopped: {why}; tasks left: {pending!r}")
        return done, pending


async def _reraise(tasks):
    for task in tasks:
        try:
            task.result()  # can raise the regular (non-cancellation) exceptions.
        except asyncio.CancelledError:
            pass


async def _stop_flag_checker(should_stop):
    try:
        await should_stop.wait()
    except asyncio.CancelledError:
        pass  # operator is stopping for any other reason
    else:
        logger.debug("Stop-flag is raised. Operator is stopping.")


def create_tasks(loop: asyncio.AbstractEventLoop, *arg, **kwargs):
    """
    .. deprecated:: 1.0
        This is a synchronous interface to `spawn_tasks`.
        It is only kept for backward compatibility, as it was exposed
        via the public interface of the framework.
    """
    warnings.warn("kopf.create_tasks() is deprecated: "
                  "use kopf.spawn_tasks() or kopf.operator().",
                  DeprecationWarning)
    return loop.run_until_complete(spawn_tasks(*arg, **kwargs))
