<h1 align="center">
    eCARLA-Scenes
</h1>

<h4 align="center">
    Synthetic Event-based Optical Flow Dataset for Autonomous Field Vehicles
</h4>

<div align="center">

<!-- Add badges here -->
[Introduction](#introduction) •
[Getting Started](#getting-started) •
[Dataset Generation](#dataset-generation) •
[Citation](#citation) •
[Acknowledgements](#acknowledgements) •
[Related Projects](#related-projects)

</div>


## Introduction
This repository hosts a synthetic event-based optical flow dataset, meticulously designed to simulate diverse environments under varying weather conditions using the [CARLA](https://carla.org/) simulator. The dataset is specifically tailored for autonomous field vehicles, featuring event streams, grayscale images, and corresponding ground truth optical flow.

In addition to the dataset, this repository provides a user-friendly pipeline for generating custom datasets, including optical flow displacements and grayscale images. The generated data leverages the optimized [eWiz](https://google.com) framework, ensuring efficient storage, access, and processing.

The dataset is available on [Zenodo](https://zenodo.org/), while the data generation pipeline can be utilized by cloning this repository. Whether you're a researcher or developer, this resource is an ideal starting point for advancing event-based vision systems in real-world autonomous applications.

## Getting Started
### Prerequisites
The file [requirements.txt](https://google.com) contains the necessary Python packages for this project. To install, run:
```bash
pip install -r requirements.txt
```

This pipeline has been tested with [CARLA 0.9.13](https://github.com/carla-simulator/carla/releases/tag/0.9.13), and it is recommended to use version 0.9.13 or later for optimal compatibility. Ensure that the simulator is installed and running before utilizing this pipeline.

## Dataset Generation
The Python-based pipeline includes, both, a scenario creator, and a scenario reader. The scenario creator allows for the creation of driving scenarios in which the user can select their desired map. The vehicle can then be controlled with the arrow keys around the environment for any desired duration. The scenario reader, on the other hand, is responsible for acquiring the sensors' data.

### Scenario Creator
The file [create_scenario.py](https://google.com) corresponds to the scenario creator script. Open the script, replace the arguments inside, then simply run the script. The script's arguments are explained below:
```
--client Simulator's host location.
--resolution Window's resolution.
--out_path Output scenario file path. The path should absolute ending with the ".log" file extension.
--world_map Desired map to load. World map namings can be found on the simulator's official website.
--world_weather Weather preset. Weather preset namings can be found on the simulator's official website. Naming examples include "ClearNoon", "CloudySunset", etc.
--vehicle_type Vehicle type to control.
--record_start_time Recording starting timestamp in s.
--record_delta_time Recording duration in s.
--num_vehicles Number of other vehicles to spawn. Makes the scene dynamic.
--num_peds Number of pedestrians to spawn. Makes the scene dynamic.
```

After running the script, the window appears along with the simulation time and recording status on the top left corner. When the recording starts, control the car as desired. After the set duration and when recording stops, you can kill the script.

> **Note:** The vehicle can be controlled with the `W`, `A`, `S`, `D` keys. To apply the reverse gear, press the `Q` key.

### Scenario Reader
Add more information here

### Generated Dataset
Add more information here

| Test | Test | Test |
| ---- | ---- | ---- |
| Test | Test | Test |
| Test | Test | Test |

## Citation
Add more information here

## Acknowledgements
Add more information here

## Related Projects
Add more information here
