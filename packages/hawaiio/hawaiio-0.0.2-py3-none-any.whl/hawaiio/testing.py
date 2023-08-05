from ._base import Clock


class MockClock(Clock):
    ticks: int

    def start(self):
        self.ticks = 0

    def tick(self):
        self.ticks += 1

    def time(self) -> int:
        return self.ticks

    def to_sleep_time(self, deadline: float) -> float:
        return deadline - self.ticks
