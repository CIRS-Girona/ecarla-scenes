import time

import carla
import pygame

from .utils.game import Game
from .utils.sensor import Sensor
from .utils.sync import SensorSync

from typing import Any, Dict, List, Tuple, Callable


class ScenarioBase():
    """Scenario base.
    """
    def __init__(
        self,
        client: Any,
        resolution: Tuple[int, int],
        out_path: str,
        sensors: Dict[str, Any] = None,
        start_time: float = 0.5,
        delta_time: float = 0.1,
        world_map: str = None,
        world_weather: str = None,
        client_timeout: float = 10.0,
        init_sleep: float = 5.0
    ) -> None:
        self.client = client
        self.resolution = resolution
        self.out_path = out_path
        self.sensors = sensors
        self.start_time = start_time
        self.delta_time = delta_time
        self.world_map = world_map
        self.world_weather = world_weather
        self.client_timeout = client_timeout
        self.init_sleep = init_sleep
        self._init_simulation()
        self._init_game()

    def _init_simulation(self) -> None:
        """Initializes simulation.
        """
        self.client.set_timeout(self.client_timeout)
        if self.world_map is not None:
            self.client.load_world(self.world_map)
        time.sleep(self.init_sleep)
        self.world = self.client.get_world()
        if self.world_weather is not None:
            self.world_weather = getattr(
                carla.WeatherParameters, self.world_weather
            )
            self.world.set_weather(self.world_weather)
        self.init_settings = self.world.get_settings()
        self.world.apply_settings(carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_time
        ))

    def _init_game(self) -> None:
        """Initializes PyGame window.
        """
        self.game = Game(resolution=self.resolution)

    def _init_sensors(self, vehicle: Any) -> None:
        """Initializes sensors.
        """
        for sensor in self.sensors:
            sensor["options"].update({"image_size_y": f"{self.resolution[0]}"})
            sensor["options"].update({"image_size_x": f"{self.resolution[1]}"})
        self.active_sensors: List[Sensor] = []
        for sensor in self.sensors:
            self.active_sensors.append(Sensor(
                world=self.world, actor=vehicle,
                sensor=sensor, delta_time=self.delta_time
            ))

    # === Main Looping Function === #
    def loop(self) -> None:
        """Loops synchronous simulation.
        """
        raise NotImplementedError

    # === Private Functions === #
    def _reset_settings(self) -> None:
        """Resets simulation settings.
        """
        self.world.apply_settings(self.init_settings)
        print("Simulation settings reset.")

    def _destroy_sensors(self) -> None:
        """Destroys sensors.
        """
        for sensor in self.active_sensors:
            sensor.get_obj().destroy()
        print("Sensors destroyed.")
