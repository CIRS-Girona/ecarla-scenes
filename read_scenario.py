# TODO: Complete documentation
"""This is an example script to read a scenario in which you...
"""
import carla

from read import ReadScenario


if __name__ == "__main__":
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
                "positive_threshold": "0.5",
                "negative_threshold": "0.4"
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

    # Setup simulation
    client = carla.Client("localhost", 2000)
    resolution = (260, 346)
    out_path = "/home/jad/datasets/carla/ewiz/dynamic_town2_forward_cloudy-sunset"
    sensors = sensors
    start_time = 1.0
    delta_time = 0.01
    world_map = "Town02"
    world_weather = "CloudySunset"
    record_path = "/home/jad/datasets/carla/scenarios/both/dynamic_town2_forward_cloudy-sunset.log"
    record_delta_time = 60.0

    # Create scenario object
    read_scenario = ReadScenario(
        client, resolution, out_path,
        sensors, start_time, delta_time,
        world_map, world_weather,
        record_path, record_delta_time
    )
