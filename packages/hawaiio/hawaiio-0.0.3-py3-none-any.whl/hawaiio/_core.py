import time as ostime
import types
import typing

from ._base import Clock

__all__ = ("run", "sleep", "time")


class WallClock(Clock):
    _time: float

    def start(self):
        self._time = ostime.time()

    def time(self) -> float:
        return self._time

    def to_sleep_time(self, deadline: float) -> float:
        return deadline - self._time

    def tick(self):
        self._time = ostime.time()


DEFAULT_CLOCK = WallClock()


def run(
    coro: typing.Coroutine[None, None, typing.T], clock: Clock = None
) -> typing.T:
    if clock is None:
        clock = DEFAULT_CLOCK

    with Clock.configure(clock):
        while True:
            try:
                coro.send(None)
            except StopIteration as exc:
                return exc.value
            else:
                clock.tick()


@types.coroutine
def sleep(seconds: float):
    if seconds < 0:
        raise ValueError(f"'seconds' must be positive (got {seconds})")

    clock = Clock.get()
    start = clock.time()
    deadline = start + seconds

    while clock.to_sleep_time(deadline) > 0:
        yield


def time() -> float:
    return Clock.get().time()
