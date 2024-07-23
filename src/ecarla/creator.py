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


class ScenarioCreator(ScenarioBase):
    """Scenario creator.
    """
    def __init__(
        self,
        client: Any,
        resolution: Tuple[int, int],
        out_path: str,
        start_time: float = 0.5,
        delta_time: float = 0.1,
        vehicle_type: str = "vehicle.tesla.cybertruck",
        record_start_time: float = 20.0,
        record_delta_time: float = 60.0,
        **kwargs
    ) -> None:
        super().__init__(
            client=client, resolution=resolution, out_path=out_path,
            start_time=start_time, delta_time=delta_time, **kwargs
        )
        self.vehicle_type = vehicle_type
        self.record_start_time = record_start_time
        self.record_delta_time = record_delta_time
        self._init_vehicles()
        self._init_sensors(vehicle=self.active_vehicle)
        self._init_control(vehicle=self.active_vehicle)

    def _init_vehicles(self) -> None:
        """Initializes scenario creator.
        """
        self.vehicle_spawner = VehicleSpawner(client=self.client, world=self.world)
        self.vehicle_spawner.spawn_vehicles(num_vehicles=1, vehicle_type=self.vehicle_type)
        self.active_vehicle = self.vehicle_spawner.get_vehicles()[0]

    def _init_control(self, vehicle: Any) -> None:
        """Initializes manual control.
        """
        self.control = ManualControl(world=self.world, actor=vehicle)
