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

In addition to the dataset, this repository provides a user-friendly pipeline for generating custom datasets, including optical flow displacements and grayscale images. The generated data leverages the optimized [eWiz](https://github.com/CIRS-Girona/ewiz) framework, ensuring efficient storage, access, and processing.

The dataset is available on [Zenodo](10.5281/zenodo.14412251), while the data generation pipeline can be utilized by cloning this repository. Whether you're a researcher or developer, this resource is an ideal starting point for advancing event-based vision systems in real-world autonomous applications.

## Getting Started
### Prerequisites
The file [requirements.txt](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/requirements.txt) contains the necessary Python packages for this project. To install, run:
```bash
pip install -r requirements.txt
```

This pipeline has been tested with [CARLA 0.9.13](https://github.com/carla-simulator/carla/releases/tag/0.9.13), and it is recommended to use version 0.9.13 or later for optimal compatibility. Ensure that the simulator is installed and running before utilizing this pipeline.

## Dataset Generation
The Python-based pipeline includes, both, a scenario creator, and a scenario reader. The scenario creator allows for the creation of driving scenarios in which the user can select their desired map. The vehicle can then be controlled with the arrow keys around the environment for any desired duration. The scenario reader, on the other hand, is responsible for acquiring the sensors' data.

### Scenario Creator
The file [create_scenario.py](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/create_scenario.py) corresponds to the scenario creator script. Open the script, replace the arguments inside, then simply run the script. The script's arguments are explained below:
```
--client               Simulator's host location.
--resolution           Window's resolution.
--out_path             Output scenario file path. The path should absolute ending with the ".log" file extension.
--world_map            Desired map to load. World map namings can be found on the simulator's official website.
--world_weather        Weather preset. Weather preset namings can be found on the simulator's official website. Naming examples include "ClearNoon", "CloudySunset", etc.
--vehicle_type         Vehicle type to control.
--record_start_time    Recording starting timestamp in s.
--record_delta_time    Recording duration in s.
--num_vehicles         Number of other vehicles to spawn. Makes the scene dynamic.
--num_peds             Number of pedestrians to spawn. Makes the scene dynamic.
```

After running the script, the window appears along with the simulation time and recording status on the top left corner. When the recording starts, control the car as desired. After the set duration and when recording stops, you can kill the script.

> **Note:** The vehicle can be controlled with the `W`, `A`, `S`, `D` keys. To apply the reverse gear, press the `Q` key.

### Scenario Reader
The file [read_scenario.py](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/read_scenario.py) corresponds to the scenario reader script. The scenario reader reads a CARLA recording file with the ".log" format, and replays the simulation. While the simulation is playing, the user can choose which sensors to use and capture data accordingly. For now, we support the event-based camera, the RGB camera, and optical flow sensor.

After defining your sensors and arguments inside the [read_scenario.py](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/read_scenario.py) file, you have to run the script while the simulator is running. The script requires the following arguments:
```
--client               Simulator's host location.
--resolution           Window's resolution.
--out_path             Output dataset directory. The dataset is saved using the "eWiz" format.
--sensors              List of sensors to use for the recording.
--start_time           Starting timestamp to operate the sensors.
--delta_time           Simulation ticking rate in s.
--world_map            Desired map to load. World map namings can be found on the simulator's official website.
--world_weather        Weather preset. Weather preset namings can be found on the simulator's official website. Naming examples include "ClearNoon", "CloudySunset", etc.
--record_path          Path of recording ".log" file.
--record_delta_time    Recording duration in s.
```

The `--sensors` argument takes as input a dictionary. An example sensors input can be found below:
```python
# Apply imports
import carla

# Camera transforms and sensors with respect to the active vehicle
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
```

Currently, only these three sensors are supported. The arguments that you can modify are the `options` and `transform` arguments. The `options` are nothing but the corresponding options of each sensor which can be found in the CARLA [documentation](https://carla.readthedocs.io/en/latest/ref_sensors/). The `transform` argument is the location of the sensor with respect to the active vehicle.

> **Note:** For now, the `name` and `type` arguments need to be written exactly like the example above. Also, the `converter` argument can be kept to `None` as we plan to add more functionalities in the future. You can check the example for both scripts [create_scenario.py](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/create_scenario.py), and [read_scenario.py](https://github.com/CIRS-Girona/ecarla-scenes/blob/main/read_scenario.py) to understand the input arguments.

### Generated Dataset
We provide some generated dataset sequences on the [Zenodo](10.5281/zenodo.14412251) platform. These datasets can be downloaded [here](10.5281/zenodo.14412251). We provide both static and dynamic scenes in which we have other vehicles and walking pedestrians. Moreover, the datasets are taken in different environments and weather conditions. All sequences have three main variations: forward, backward, and sway.

A summary of the provided dataset can be found in the table below:

<div align="center">

| Number | Type | Map | Weather |
| ------ | ---- | --- | --------|
| 01 | Static | Town02 | CloudySunset |
| 04 | Static | Town02 | ClearSunset |
| 07 | Static | Town07 | ClearNoon |
| 10 | Static | Town07 | CloudyNoon |
| 13 | Static | Town07 | ClearSunset |
| 16 | Static | Town10HD | ClearNoon |
| 19 | Static | Town10HD | CloudyNoon |
| 22 | Dynamic (Pedestrians) | Town07 | ClearNoon |
| 25 | Dynamic (Cars) | Town04 | CloudyNoon |
| 28 | Dynamic (Both) | Town02 | ClearSunset |
| 30 | Dynamic (Both) | Town10 | ClearSunset |

</div>

All datasets have a resolution of `260x346p`, however, if you want to use another resolution, you can create and record your own scenarios.

## Citation
This repository is related to the paper below. If you find this repository please do not hesitate to give it a star :star2:!
```bibtex
@misc{mansourCarla2024,
    title={eCARLA-scenes: A synthetically generated dataset for event-based optical flow prediction},
    author={Jad Mansour and Hayat Rajani and Rafael Garcia and Nuno Gracias},
    year={2024},
    eprint={2412.09209},
    archivePrefix={arXiv},
    primaryClass={cs.CV},
    url={https://arxiv.org/abs/2412.09209},
}
```

Also, if you have any questions do not hesitate to contact me at [jad.mansour@udg.edu](mailto:jad.mansour@udg.edu).

## Acknowledgements
This dataset makes use of the [CARLA simulator](https://carla.org/).

Jad Mansour was supported by the Joan Oró Grant no. 2024 FI-2 00762. The study was supported in part by the SIREC project, funded by the Ministerio de Ciencia e Innovación, Gobierno de España under agreement no. PID2020-116736RB-IOO.

## Related Projects
Related projects to this work are:

* [eWiz: An Event-based Data Manipulation Library](https://github.com/CIRS-Girona/ewiz)
