import carla
import pygame

from src.ecarla.creator import ScenarioCreator

from typing import Any, Dict, List, Tuple, Callable


class CreateScenario():
    """Creates scenario.
    """
    def __init__(
        self,
        client: Any,
        resolution: Tuple[int, int],
        out_path: str,
        world_map: str = None,
        world_weather: str = None,
        vehicle_type: str = "vehicle.tesla.cybertruck",
        record_start_time: float = 20.0,
        record_delta_time: float = 60.0
    ) -> None:
        # Create required actors for scenario creator
        cam_transform = carla.Transform(
            carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)
        )
        sensors = [{
            "name": "rgb",
            "type": "sensor.camera.rgb",
            "options": {},
            "transform": cam_transform,
            "converter": None
        }]

        # Run scenario creator
        scenario_creator = ScenarioCreator(
            client=client,
            resolution=resolution,
            out_path=out_path,
            sensors=sensors,
            start_time=0.0,
            delta_time=0.04,
            world_map=world_map,
            world_weather=world_weather,
            client_timeout=5.0,
            init_sleep=0.0,
            vehicle_type=vehicle_type,
            record_start_time=record_start_time,
            record_delta_time=record_delta_time
        )
        scenario_creator.loop()
