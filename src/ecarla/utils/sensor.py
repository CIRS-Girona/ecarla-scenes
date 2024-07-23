import queue
from queue import Empty

from typing import Any, Dict, List, Tuple, Callable


class Sensor():
    """Sensor.
    """
    def __init__(
        self,
        world: Any,
        actor: Any,
        sensor: Dict[str, Any],
        delta_time: float = 0.1
    ) -> None:
        self.world = world
        self.actor = actor
        self.sensor = sensor
        self.delta_time = delta_time

        # Sensor attributes
        self.world_bp = self.world.get_blueprint_library()
        self._init_sensor()

    def _init_sensor(self) -> None:
        """Initializes sensor.
        """
        # Sensor configurations
        self.name: str = self.sensor["name"]
        self.type: str = self.sensor["type"]
        self.options: Dict[str, Any] = self.sensor["options"]
        self.transform: Any = self.sensor["transform"]
        self.converter: Any = self.sensor["converter"]

        # Sensor synchronization
        self.sync_flag = False
        self.frame_count = 1
        if "sensor_tick" in self.options.keys():
            self.parsing_freq = int(float(self.options["sensor_tick"])/self.delta_time)
        else:
            self.parsing_freq = 1

        # Spawn sensor
        self.sensor_obj = self.world_bp.find(self.type)
        for option in self.options.keys():
            self.sensor_obj.set_attribute(option, self.options[option])
        self.sensor_obj = self.world.spawn_actor(
            self.sensor_obj, self.transform, attach_to=self.actor
        )

    # TODO: Add code here
