from contextlib import contextmanager

__all__ = ("Clock",)


class Clock:
    _instance: "Clock"

    def __init__(self):
        self._time: float = 0

    @classmethod
    @contextmanager
    def configure(cls, clock: "Clock"):
        cls._instance = clock
        clock.start()
        try:
            yield
        finally:
            del cls._instance

    @classmethod
    def get(cls) -> "Clock":
        try:
            return cls._instance
        except AttributeError:
            raise RuntimeError(
                "Clock hasn't started yet. "
                "Did you try to access it outside of 'run()'?"
            )

    def start(self):
        raise NotImplementedError

    def time(self) -> float:
        raise NotImplementedError

    def to_sleep_time(self, deadline: float) -> float:
        raise NotImplementedError

    def tick(self):
        raise NotImplementedError
