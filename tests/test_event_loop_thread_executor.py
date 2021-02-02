from asyncio_tools.event_loop_thread_executor import EventLoopThreadExecutor


async def foo_async() -> str:
    return "the result"


def test_execute_sync() -> None:
    with EventLoopThreadExecutor() as exec:
        assert "the result" == exec(foo_async())
