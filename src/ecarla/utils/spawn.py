import carla
import pygame
import numpy as np

from typing import Any, Dict, List, Tuple, Callable


class VehicleSpawner():
    """Vehicle spawner.
    """
    def __init__(self, client: Any, world: Any) -> None:
        self.client = client
        self.world = world
        self.map = self.world.get_map()
        self.settings = self.world.get_settings()

        # All available vehicles in the simulation
        self.all_vehicles = []

    # TODO: Add code here
