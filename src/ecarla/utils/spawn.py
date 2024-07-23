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

    # === User Functions === #
    def get_vehicles(self) -> List[Any]:
        """Returns list of all vehicles.
        """
        return self.all_vehicles

    def destroy_vehicles(self) -> None:
        """Destroy all vehicles.
        """
        for vehicle in self.all_vehicles:
            vehicle.destroy()
        print("All vehicles destroyed.")

    def spawn_vehicles(
        self,
        num_vehicles: int = 1,
        vehicle_type: str = None
    ) -> None:
        """Spawns vehicles.
        """
        if vehicle_type is not None:
            assert num_vehicles == 1, (
                "Only 1 vehicle can be spawned when choosing vehicle type."
            )
        if vehicle_type is None:
            self.world_bp_vehicles = (self.world.get_blueprint_library().filter("vehicle.*"))
        else:
            self.world_bp_vehicles = [self.world.get_blueprint_library().find(vehicle_type)]
        self.world_bp_vehicles = [
            v for v in self.world_bp_vehicles
            if int(v.get_attribute("number_of_wheels")) == 4
        ]

        # Spawn vehicles
        self.spawn_points = self.map.get_spawn_points()
        self.num_spawns = len(self.spawn_points)
        if num_vehicles < self.num_spawns:
            np.random.shuffle(self.spawn_points)
        for i, point in enumerate(self.spawn_points):
            if i >= num_vehicles:
                break
            bp = np.random.choice(self.world_bp_vehicles)
            if bp.has_attribute("color"):
                vehicle_color = np.random.choice(bp.get_attribute("color").recommended_values)
                bp.set_attribute("color", vehicle_color)
            if bp.has_attribute("driver_id"):
                vehicle_id = np.random.choice(bp.get_attribute("driver_id").recommended_values)
                bp.set_attribute("driver_id", vehicle_id)
            bp.set_attribute("role_name", "autopilot")
            # Apply physics
            vehicle = self.world.spawn_actor(bp, point)
            physics_control = vehicle.get_physics_control()
            physics_control.use_sweep_wheel_collision = True
            vehicle.apply_physics_control(physics_control)
            vehicle.set_autopilot(False)
            # Add to vehicles list
            self.all_vehicles.append(vehicle)
