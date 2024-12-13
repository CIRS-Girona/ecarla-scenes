"""This is an example script to record a scenario in which you manually control
the vehicle.
"""
import carla

from create import CreateScenario


if __name__ == "__main__":
    # Setup simulation
    client = carla.Client("localhost", 2000)
    resolution = (720, 1080)
    out_path = "/home/jad/datasets/carla/scenarios/both/dynamic_town10_sway_cloudy-noon.log"
    world_map = "Town10HD"
    world_weather = "CloudyNoon"
    vehicle_type = "vehicle.tesla.cybertruck"
    record_start_time = 20
    record_delta_time = 60
    num_vehicles = 30
    num_peds = 20

    # Create scenario object
    create_scenario = CreateScenario(
        client, resolution, out_path, world_map, world_weather, vehicle_type,
        record_start_time, record_delta_time, num_vehicles, num_peds
    )
