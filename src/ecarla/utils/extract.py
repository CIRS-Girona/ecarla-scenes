import numpy as np
import flow_vis

from typing import Any, Dict, List, Tuple, Callable


def extract_events(
    data: Any, sim_time: float
) -> Tuple[np.ndarray, np.ndarray]:
    """Extracts events data from simulation.
    """
    raw_data = np.frombuffer(data.raw_data, dtype=([
        ("x", np.uint16),
        ("y", np.uint16),
        ("t", np.int64),
        ("pol", bool)
    ]))
    # Extract raw events
    events = np.zeros((raw_data[:]["x"].shape[0], 4), dtype=np.float64)
    events[:, 0] = raw_data[:]["x"]
    events[:, 1] = raw_data[:]["y"]
    events[:, 2] = sim_time*1e6
    events[:, 3] = raw_data[:]["pol"]
    events = events.astype(np.int64)
    # Extract events image
    image = np.zeros((data.height, data.width, 3), dtype=np.uint8)
    image[raw_data[:]["y"], raw_data[:]["x"], raw_data[:]["pol"]*2] = 255
    return events, None, image


# TODO: Add surface format change
def extract_rgb(
    data: Any, sim_time: float
) -> Tuple[np.ndarray, int]:
    """Extracts RGB image from simulation.
    """
    raw_data = np.frombuffer(data.raw_data, dtype=np.uint8)
    # Extract RGB image
    rgb = np.reshape(raw_data, (data.height, data.width, 4))
    rgb = rgb[:, :, :3]
    rgb = rgb[:, :, ::-1]
    # Extract simulation time
    time = int(sim_time*1e6)
    return rgb, time, rgb


def extract_gray(
    data: Any, sim_time: float
) -> Tuple[np.ndarray, int, np.ndarray]:
    """Extracts grayscale image from simulation.
    """
    raw_data = np.frombuffer(data.raw_data, dtype=np.uint8)
    # Extract RGB image
    rgb = np.reshape(raw_data, (data.height, data.width, 4))
    rgb = rgb[:, :, :3]
    rgb = rgb[:, :, ::-1]
    # Convert to grayscale image
    gray = np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
    # Extract simulation time
    time = int(sim_time*1e6)
    # Convert to surface
    surface = np.repeat(gray[..., None], 3, axis=2)
    return gray, time, surface


def extract_flow(
    data: Any, sim_time: float
) -> Tuple[np.ndarray, int, np.ndarray]:
    """Extracts flow data from simulation.
    """
    raw_data = np.array([(p.x, p.y) for p in data], dtype=np.float64)
    # Extract optical flow
    flow = raw_data.reshape((data.height, data.width, 2))
    flow[:, :, 0] *= data.width*-0.5
    flow[:, :, 1] *= data.height*0.5
    # Convert to surface
    surface = flow_vis.flow_to_color(flow_uv=flow, convert_to_bgr=False)
    # Convert flow format
    flow = np.transpose(flow, (2, 0, 1))
    # Extract simulation time
    time = int(sim_time*1e6)
    return flow, time, surface
