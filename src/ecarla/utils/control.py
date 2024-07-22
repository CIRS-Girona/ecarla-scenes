import carla
import pygame
from pygame.locals import *

from typing import Any, Dict, List, Tuple, Callable


class ManualControl():
    """Manual control.
    """
    def __init__(self, world: Any, actor: Any) -> None:
        self.world = world
        self.actor = actor
        self._init_control()

    def _init_control(self) -> None:
        """Initializes control.
        """
        self.vehicle_control = carla.VehicleControl()
        self.vehicle_lights = carla.VehicleLightState.NONE
        self.steer_cache = 0.0
