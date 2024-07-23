import time

import carla
import pygame

from .base import ScenarioBase

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
