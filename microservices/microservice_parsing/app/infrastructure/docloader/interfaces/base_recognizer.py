from abc import ABC, abstractmethod
from PIL import Image
from app.infrastructure.docloader.models.io import BBox, DetectionOutput
from typing import overload
from typing import List

class BaseRecognizer(ABC):
    """
    Base class for all recognizers.
    """
    @abstractmethod
    def recognize(self, image: Image.Image, bboxes: List[BBox]) -> str:
        """
        Recognize text in the given images.

        Args:
            images: List of images to be processed.
            bboxes: List of lists of bounding boxes corresponding to each image.

        Returns:
            Recognized text.
        """
        raise NotImplementedError
