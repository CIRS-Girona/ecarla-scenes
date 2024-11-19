import time

import carla
import pygame

from .base import ScenarioBase
from .utils.game import Game
from .utils.sensor import Sensor
from .utils.sync import SensorSync

from .utils.spawn import VehicleSpawner, TrafficSpawner
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
        num_vehicles: int = None,
        num_peds: int = None,
        **kwargs
    ) -> None:
        super().__init__(
            client=client, resolution=resolution, out_path=out_path,
            start_time=start_time, delta_time=delta_time, **kwargs
        )
        self.vehicle_type = vehicle_type
        self.record_start_time = record_start_time
        self.record_delta_time = record_delta_time
        self.num_vehicles = num_vehicles
        self.num_peds = num_peds
        self._init_vehicles()
        self._init_sensors(vehicle=self.active_vehicle)
        self._init_control(vehicle=self.active_vehicle)

    def _init_vehicles(self) -> None:
        """Initializes scenario creator.
        """
        self.vehicle_spawner = VehicleSpawner(client=self.client, world=self.world)
        self.vehicle_spawner.spawn_vehicles(num_vehicles=1, vehicle_type=self.vehicle_type)
        self.traffic_spawner = TrafficSpawner(
            client=self.client,
            world=self.world,
            num_vehicles=self.num_vehicles,
            num_peds=self.num_peds
        )
        self.active_vehicle = self.vehicle_spawner.get_vehicles()[0]
        time.sleep(10)

    def _init_control(self, vehicle: Any) -> None:
        """Initializes manual control.
        """
        self.control = ManualControl(world=self.world, actor=vehicle)

    def _render(self, data: Dict[str, Any]) -> None:
        """Renders RGB image in window.
        """
        if "rgb" in data.keys():
            if data["rgb"] is not None:
                rgb_image = extract.extract_rgb(data=data["rgb"], sim_time=self.sim_time)[2]
                self.game.render_image(image=rgb_image, blend=False)
        self.game.render_sim_time(time=self.sim_time)
        # Recording status
        if self.record_flag == self.end_record_flag:
            self.game.render_text(text="Not recording...")
        elif self.record_flag == True and self.end_record_flag == False:
            self.game.render_text(text="Recording...")
        # Flip display
        self.game.flip()

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
                self.record_flag = False
                self.end_record_flag = False
                # Main loop
                while True:
                    # Start recording
                    if self.sim_time > self.record_start_time and self.record_flag == False:
                        self.client.start_recorder(self.out_path, True)
                        self.record_flag = True
                    # Stop recording
                    if self.sim_time > (
                        self.record_start_time + self.record_delta_time
                    ) and self.record_flag == True and self.end_record_flag == False:
                        self.client.stop_recorder()
                        self.end_record_flag = True

                    # Tick PyGame window
                    if self.game.should_quit():
                        return
                    self.game.tick_clock()
                    # Parse data
                    data = sensor_sync.tick(timeout=2.0)
                    # Render data
                    self._render(data=data)
                    # Vehicle control
                    self.game.tick_clock_busy_loop(fps=60)
                    game_clock = self.game.get_clock()
                    if self.control.parse_control(clock=game_clock):
                        return

                    # Print status
                    print("=====", "Frame ID:", data["world"], "=====")
                    print("RGB Data:", data["rgb"] is not None)
                    print("Sim Time:", str(timedelta(seconds=self.sim_time)))
                    print("Real Time:", str(timedelta(seconds=time.time() - self.real_time)))

                    # Update simulation time
                    self.sim_time += self.delta_time
        finally:
            self.game.quit()
            self._reset_settings()
            self.vehicle_spawner.destroy_vehicles()
            self._destroy_sensors()
            self.traffic_spawner.destroy_traffic()
            print("All simulation elements reset.")
