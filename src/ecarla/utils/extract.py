import numpy as np

from typing import Any, Dict, List, Tuple, Callable


# TODO: Review events timestamps
def extract_events(events: Any) -> np.ndarray:
    """Extracts events data from simulation.
    """
    raw_events = np.frombuffer(events.raw_data, dtype=([
        ("x", np.uint16), ("y", np.uint16), ("t", np.int64), ("pol", bool)
    ]))
    events = np.zeros((raw_events[:]["x"].shape[0], 4), dtype=np.float64)
    events[:, 0] = raw_events[:]["x"]
    events[:, 1] = raw_events[:]["y"]
    events[:, 2] = raw_events[:]["t"]
    events[:, 3] = raw_events[:]["pol"]
    return events

def extract_rgb(image: Any) -> np.ndarray:
    """Extracts RGB image from simulation.
    """
    raw_image = np.frombuffer(image.raw_data, dtype=np.uint8)
    raw_image = np.reshape(raw_image, (image.height, image.width, 4))
    raw_image = raw_image[:, :, :3]
    raw_image = raw_image[:, :, ::-1]
    return raw_image

def extract_gray(image: Any) -> np.ndarray:
    """Extracts grayscale image from simulation.
    """
    raw_image = np.frombuffer(image.raw_data, dtype=np.uint8)
    raw_image = np.reshape(raw_image, (image.height, image.width, 4))
    raw_image = raw_image[:, :, :3]
    raw_image = raw_image[:, :, ::-1]
    raw_image = np.dot(raw_image[..., :3], [0.299, 0.587, 0.114])
    return raw_image

def extract_flow(flow: Any) -> np.ndarray:
    """Extracts flow data from simulation.
    """
    raw_flow = np.array([(p.x, p.y) for p in flow], dtype=np.float64)
    raw_flow = raw_flow.reshape((flow.height, flow.width, 2))
    raw_flow[:, :, 0] *= flow.width*-0.5
    raw_flow[:, :, 1] *= flow.height*0.5
    return raw_flow
