import carla
import pygame

from src.ecarla.reader import ScenarioReader

from typing import Any, Dict, List, Tuple, Callable


class ReadScenario():
    """Reads scenario.
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
        record_path: str = None,
        record_delta_time: float = 60.0
    ) -> None:
        # TODO: Modify hard-coded arguments
        # Run scenario reader
        scenario_reader = ScenarioReader(
            client=client,
            resolution=resolution,
            out_path=out_path,
            sensors=sensors,
            start_time=start_time,
            delta_time=delta_time,
            world_map=world_map,
            world_weather=world_weather,
            client_timeout=5.0,
            init_sleep=0.0,
            record_path=record_path,
            record_delta_time=record_delta_time
        )
        scenario_reader.loop()
