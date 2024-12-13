import os
import shutil

import carla

from read import ReadScenario

from typing import Dict, List


def get_town_and_weather_names(
        filename: str, towns_assoc: Dict, weather_assoc: Dict
    ) -> List:
    """Gets town and weather names.
    """
    world_info = []
    for town_name in towns_assoc.keys():
        if town_name in filename:
            world_info.append(towns_assoc[town_name])
    for weather_name in weather_assoc.keys():
        if weather_name in filename:
            world_info.append(weather_assoc[weather_name])
    return world_info


if __name__ == "__main__":
    # Main directories
    data_dir = "/home/jad/datasets/carla/scenarios/both"
    out_dir = "/home/jad/datasets/carla/ewiz/260p/both"

    # Data associations
    towns_assoc = {
        "_town2_": "Town02",
        "_town4_": "Town04",
        "_town7_": "Town07",
        "_town10_": "Town10HD"
    }
    weather_assoc = {
        "_clear-sunset": "ClearSunset",
        "_clear-noon": "ClearNoon",
        "_cloudy-sunset": "CloudySunset",
        "_cloudy-noon": "CloudyNoon"
    }

    # Camera transforms and sensors
    cam_transform = carla.Transform(
        carla.Location(x=2.8, z=1.8), carla.Rotation(pitch=-15)
    )
    sensors = [
        {
            "name": "gray",
            "type": "sensor.camera.rgb",
            "options": {
                "sensor_tick": "0.04"
            },
            "transform": cam_transform,
            "converter": None
        },
        {
            "name": "events",
            "type": "sensor.camera.dvs",
            "options": {
                "positive_threshold": "0.3",
                "negative_threshold": "0.3"
            },
            "transform": cam_transform,
            "converter": None
        },
        {
            "name": "flow",
            "type": "sensor.camera.optical_flow",
            "options": {
                "sensor_tick": "0.04"
            },
            "transform": cam_transform,
            "converter": None
        }
    ]

    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            town_name, town_weather = get_town_and_weather_names(file, towns_assoc, weather_assoc)
            save_path = os.path.join(out_dir, os.path.splitext(os.path.basename(file))[0])
            print("Processing:", file_path + "...")

            # Setup simulation
            client = carla.Client("localhost", 2000)
            resolution = (260, 346)
            out_path = save_path
            sensors = sensors
            start_time = 1.0
            delta_time = 0.001
            world_map = town_name
            world_weather = town_weather
            record_path = file_path
            record_delta_time = 60.0

            # Run scenario
            read_scenario = ReadScenario(
                client, resolution, out_path,
                sensors, start_time, delta_time,
                world_map, world_weather,
                record_path, record_delta_time
            )
