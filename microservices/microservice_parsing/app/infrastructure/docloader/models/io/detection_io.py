from pydantic import BaseModel
from typing import Union, TypedDict, Literal
from dataclasses import dataclass

@dataclass
class BBox(TypedDict):
    """
    A class representing a bounding box with coordinates and a label.

    Attributes:
        x1 (float): The x-coordinate of the top-left corner of the bounding box.
        y1 (float): The y-coordinate of the top-left corner of the bounding box.
        x2 (float): The x-coordinate of the bottom-right corner of the bounding box.
        y2 (float): The y-coordinate of the bottom-right corner of the bounding box.
        label (str, optional): The label or class of the object detected within the bounding box.
        confidence (float, optional): The confidence score of the detection.
    """
    x1: float
    """
    The x-coordinate of the top-left corner of the bounding box.
    """
    y1: float
    """
    The y-coordinate of the top-left corner of the bounding box.
    """
    x2: float
    """
    The x-coordinate of the bottom-right corner of the bounding box.
    """
    y2: float
    """
    The y-coordinate of the bottom-right corner of the bounding box.
    """
    label: str = None
    """
    The label or class of the object detected within the bounding box.
    """
    confidence: float = None
    """
    The confidence score of the detection.
    """

@dataclass
class DetectionOutput(TypedDict):
    """
    A class representing the result of a detection operation.

    Attributes:
        bboxes (list[BBox]): A list of bounding boxes detected in the image.
        image (str): The encoded image in which the detection was performed.
    """
    image: str
    """
    The image in which the detection was performed.
    """ 
    bboxes: Union[list[BBox], list]
    """
    A list of bounding boxes detected in the image.
    """