import time

import carla
import pygame

from .base import ScenarioBase
from .utils.game import Game
from .utils.sensor import Sensor
from .utils.sync import SensorSync

from .utils.spawn import VehicleSpawner
from .utils.control import ManualControl

from .utils import extract

from datetime import timedelta

from typing import Any, Dict, List, Tuple, Callable


class ScenarioReader(ScenarioBase):
    """Scenario reader.
    """
    def __init__(
        self,
        client: Any,
        resolution: Tuple[int, int],
        out_path: str,
        start_time: float = 0.5,
        delta_time: float = 0.1,
        **kwargs
    ) -> None:
        super().__init__(
            client=client, resolution=resolution, out_path=out_path,
            start_time=start_time, delta_time=delta_time, **kwargs
        )
        self.images = {}

    # TODO: Check if it works on grayscale data
    def _extract_data(self, data: Dict[str, Any]) -> None:
        """Extracts sensor data.
        """
        for sensor_name in data.keys():
            if data[sensor_name] is not None:
                data[sensor_name] = getattr(
                    extract, "extract_" + sensor_name
                )(data[sensor_name])
                self.images.update({sensor_name: data[sensor_name]})

    # === Main Looping Function === #
    def loop(self) -> None:
        """Loops synchronous simulation.
        """
        try:
            self.sim_time = 0.0
            self.real_time = time.time()
            # Run in synchronous mode
            with SensorSync(
                world=self.world, sensors=self.active_sensors,
                start_time=self.start_time, delta_time=self.delta_time
            ) as sensor_sync:
                # Main loop
                while True:
                    # Tick PyGame window
                    if self.game.should_quit():
                        return
                    self.game.tick_clock()
                    # Parse data
                    data = sensor_sync.tick(timeout=2.0)
                    # TODO: Continue code here
        finally:
            pass
            # TODO: Continue code here
