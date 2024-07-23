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

    def _parse_vehicle_keys(self, keys: Dict, ms: float) -> None:
        """Parses vehicle keys.
        """
        # Throttle control
        if keys[K_UP] or keys[K_w]:
            self.vehicle_control.throttle = min(
                self.vehicle_control.throttle + 0.05, 1.0
            )
        else:
            self.vehicle_control.throttle = 0.0
        # Brake control
        if keys[K_DOWN] or keys[K_s]:
            self.vehicle_control.brake = min(
                self.vehicle_control.brake + 0.2, 1.0
            )
        else:
            self.vehicle_control.brake = 0.0
        # Steer control
        steer_increment = 0.0005*ms
        if keys[K_LEFT] or keys[K_a]:
            if self.steer_cache > 0.0:
                self.steer_cache = 0.0
            else:
                self.steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            if self.steer_cache < 0.0:
                self.steer_cache = 0.0
            else:
                self.steer_cache += steer_increment
        else:
            self.steer_cache = 0.0
        self.steer_cache = min(0.7, max(-0.7, self.steer_cache))
        self.vehicle_control.steer = round(self.steer_cache, 1)
        # Apply control
        self.vehicle_control.hand_break = keys[K_SPACE]
        self.actor.apply_control(self.vehicle_control)

    # === User Functions === #
    def parse_control(self, clock: pygame.time.Clock) -> bool:
        """Parses vehicle control.
        """
        vehicle_curr_lights = self.vehicle_lights
        # Iterate over keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if self.should_quit(event.key):
                    return True

            # Reverse gear
            if event.key == K_q:
                self.vehicle_control.gear = 1 if self.vehicle_control.reverse else -1
        # Vehicle control
        self._parse_vehicle_keys(keys=pygame.key.get_pressed(), ms=clock.get_time())
        self.vehicle_control.reverse = self.vehicle_control.gear < 0
        # Lights control
        if self.vehicle_control.brake:
            vehicle_curr_lights |= carla.VehicleLightState.Brake
        else:
            vehicle_curr_lights &= ~carla.VehicleLightState.Brake
        if self.vehicle_control.reverse:
            vehicle_curr_lights |= carla.VehicleLightState.Reverse
        else:
            vehicle_curr_lights &= ~carla.VehicleLightState.Reverse
        if vehicle_curr_lights != self.vehicle_lights:
            self.vehicle_lights = vehicle_curr_lights
            self.actor.set_light_state(carla.VehicleLightState(self.vehicle_lights))

    def should_quit(self, key: Any) -> bool:
        """Quits PyGame on key stroke.
        """
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)
