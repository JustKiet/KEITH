from abc import ABC, abstractmethod
from PIL import Image
from app.infrastructure.docloader.models.io import DetectionOutput

class BaseDetector(ABC):
    """
    Base class for all detectors.
    """

    @abstractmethod
    def detect(self, image: Image.Image) -> DetectionOutput:
        """
        Detect anomalies in the given data.
        
        Args:
            image: Image to be processed.
        
        Returns:
            Detected bounding boxes.
        """
        raise NotImplementedError