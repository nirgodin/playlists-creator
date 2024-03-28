from asyncio import AbstractEventLoop, new_event_loop
from typing import Generator

from _pytest.fixtures import fixture


@fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = new_event_loop()
    yield loop
    loop.close()
