import os
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

from ewiz.core.utils import create_dir, save_json
from ewiz.data.writers import WriterEvents, WriterGray, WriterFlow

from datetime import timedelta

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
        record_path: str = None,
        record_delta_time: float = 60.0,
        **kwargs
    ) -> None:
        super().__init__(
            client=client, resolution=resolution, out_path=out_path,
            start_time=start_time, delta_time=delta_time, **kwargs
        )
        self.record_path = record_path
        self.record_delta_time = record_delta_time
        # TODO: Change hard-coded values
        self.out_path = create_dir(self.out_path)
        self.images = {"events": None, "gray": None, "flow": None}
        self._save_props()
        self._init_writers()
        self._read_recording()
        self._init_sensors(vehicle=self.active_actor)
        time.sleep(10)

    # TODO: Check format requirements
    def _save_props(self) -> None:
        """Saves camera properties.
        """
        props = {}
        props.update({"sensor_size": self.resolution})
        print("# ===== Saving Data Properties ===== #")
        file_path = os.path.join(self.out_path, "props.json")
        save_json(props, file_path)
        print("# ===== Data Properties Saved ===== #")

    def _init_writers(self) -> None:
        """Initializes writers.
        """
        self.events_writer = WriterEvents(self.out_path)
        self.gray_writer = WriterGray(self.out_path)
        self.flow_writer = WriterFlow(self.out_path)

    def _read_recording(self) -> None:
        """Reads recording.
        """
        self.client.replay_file(self.record_path, 0, 0, 0, False)
        self.world.tick()
        # TODO: Use this later
        self.world_actors = self.world.get_actors().filter("vehicle.*")
        self.active_actor = self.world_actors[0]
        for actor in self.world_actors:
            if actor.attributes["role_name"] == "hero":
                self.active_actor = actor

    def _destroy_actors(self) -> None:
        """Destroy all actors.
        """
        self.active_actor.destroy()
        """
        actors = self.world.get_actors()
        for actor in actors:
            actor.destroy()
        """

    def _extract_data(self, data: Dict[str, Any]) -> None:
        """Extracts sensor data.
        """
        for sensor_name in data.keys():
            if data[sensor_name] is not None and sensor_name != "world":
                data[sensor_name] = getattr(
                    extract, "extract_" + sensor_name
                )(data[sensor_name], sim_time=self.sim_time)
                self.images.update({sensor_name: data[sensor_name][2]})
        return data

    def _save_data(self, data: Dict[str, Any]) -> None:
        """Saves data to disk.
        """
        for sensor_name in data.keys():
            if data[sensor_name] is not None and sensor_name != "world":
                if sensor_name == "events":
                    self.events_writer.write(events=data[sensor_name][0])
                elif sensor_name == "gray":
                    self.gray_writer.write(gray_image=data[sensor_name][0], time=data[sensor_name][1])
                elif sensor_name == "flow":
                    self.flow_writer.write(flow=data[sensor_name][0], time=data[sensor_name][1])
                else:
                    # TODO: Add error message
                    raise NotImplementedError

    def _print_data(self, data: Dict[str, Any]) -> None:
        """Prints data status.
        """
        for sensor_name, info in data.items():
            print(sensor_name + ":", info is not None)

    def _map_data(self) -> None:
        """Maps data.
        """
        self.events_writer.map_time_to_events()
        self.gray_writer.map_time_to_gray()
        self.gray_writer.map_gray_to_events()
        self.flow_writer.map_time_to_flow()
        self.flow_writer.map_flow_to_events()

    def _render_display(self) -> None:
        """Renders display.
        """
        if self.images["gray"] is not None:
            self.game.render_image(self.images["gray"], blend=False)
        if self.images["events"] is not None:
            self.game.render_image(self.images["events"], blend=True)
        if self.images["flow"] is not None:
            self.game.render_image(self.images["flow"], blend=True)

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
                # Main loop
                while True:
                    # Tick PyGame window
                    if self.game.should_quit():
                        return
                    self.game.tick_clock()
                    # Parse data
                    data = sensor_sync.tick(timeout=2.0)
                    # Print status
                    print("=====", "Frame ID:", data["world"], "=====")
                    # Extract data
                    data = self._extract_data(data)
                    self._print_data(data)
                    print("Sim Time:", str(timedelta(seconds=self.sim_time)))
                    print("Real Time:", str(timedelta(seconds=time.time() - self.real_time)))
                    self._save_data(data)
                    self._render_display()

                    if self.sim_time > self.start_time:
                        self.game.render_sim_time(self.sim_time)
                    self.game.flip()

                    self.sim_time += self.delta_time
                    if self.sim_time > (self.record_delta_time - self.start_time):
                        return
        # TODO: Debug code here
        except Exception as error:
            print(error)
        finally:
            self.game.quit()
            self._reset_settings()
            self._destroy_actors()
            print("Actors destroyed.")
            self._destroy_sensors()
            print("All simulation elements reset.")
            print("# === Mapping Data === #")
            self._map_data()
