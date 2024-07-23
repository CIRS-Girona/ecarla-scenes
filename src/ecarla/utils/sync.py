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

    # === User Functions === #
    def tick(self, timeout: float = 2.0) -> Dict[str, Any]:
        """Ticks simulation and returns data for all sensors.
        """
        data = {"world": None}
        for sensor in self.sensors:
            data.update({sensor.get_name(): None})

        # Tick simulation
        self.world_frame = self.world.tick()
        data["world"] = self.world_frame

        # Get sensors data
        if self.iter >= self.start_iter:
            for sensor in self.sensors:
                data[sensor.get_name()] = sensor.read_data(
                    world_frame=self.world_frame,
                    sensor_queue=self.sensors_queues[sensor.get_name()],
                    timeout=timeout
                )
        self.iter += 1
        return data

    # === Iterator Functions === #
    def __enter__(self) -> None:
        """Initializes iterator.
        """
        def create_queue(name: str, on_tick: Any) -> None:
            """Creates queue.
            """
            q = queue.Queue()
            on_tick(q.put)
            self.sensors_queues.update({name: q})

        # Create sensors queues
        create_queue(name="world", on_tick=self.world.on_tick)
        for sensor in self.sensors:
            create_queue(name=sensor.get_name(), on_tick=sensor.get_obj().listen)
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Runs on exit.
        """
        pass
