__all__ = ("Clock",)


class Clock:
    _instance: "Clock"

    def __init__(self):
        self._time: float = 0

    @classmethod
    def set(cls, clock: "Clock"):
        cls._instance = clock

    @classmethod
    def get(cls) -> "Clock":
        try:
            return cls._instance
        except AttributeError:
            raise RuntimeError(
                "Clock hasn't started yet. "
                "Are you accessing it outside an asynchronous function?"
            )

    def start(self):
        raise NotImplementedError

    def time(self) -> float:
        raise NotImplementedError

    def to_sleep_time(self, deadline: float) -> float:
        raise NotImplementedError

    def tick(self):
        raise NotImplementedError
