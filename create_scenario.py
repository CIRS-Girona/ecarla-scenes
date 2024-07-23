"""This is an example script to record a scenario in which you manually control
the vehicle.
"""
import carla

from create import CreateScenario


if __name__ == "__main__":
    # Setup simulation
    client = carla.Client("localhost", 2000)
    resolution = (260, 346)
    out_path = "/home/jad/Documents/datasets/carla/scenarios/scenario.log"
    world_map = None
    world_weather = None
    vehicle_type = "vehicle.tesla.cybertruck"
    record_start_time = 20
    record_delta_time = 60

    # Create scenario object
    create_scenario = CreateScenario(
        client, resolution, out_path, world_map, world_weather, vehicle_type,
        record_start_time, record_delta_time
    )
