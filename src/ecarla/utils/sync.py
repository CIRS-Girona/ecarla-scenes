import queue

from .sensor import Sensor

from typing import Any, Dict, List, Tuple, Callable


class SensorSync():
    """Sensor synchronizer.
    """
    def __init__(
        self,
        world: Any,
        sensors: List[Sensor],
        delta_time: float,
        start_time: float
    ) -> None:
        self.world = world
        self.sensors = sensors
        self.delta_time = delta_time
        self.start_time = start_time
        self._init_sync()

    def _init_sync(self) -> None:
        """Initializes sensor synchronizer.
        """
        self.sensors_queues = {}
        self.iter = 0
        self.start_iter = int(self.start_time/self.delta_time)
