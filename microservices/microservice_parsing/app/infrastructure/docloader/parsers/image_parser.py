from app.infrastructure.docloader.interfaces import BaseDetector, BaseRecognizer, BaseParser
from app.infrastructure.docloader.utils import ImageProcessor
from app.infrastructure.docloader.detectors import DoctrDetector
from app.infrastructure.docloader.recognizers import VietOCRRecognizer
from PIL import Image
from loguru import logger

class ImageParser(BaseParser):
    def __init__(self, 
                 detector: BaseDetector = None,
                 recognizer: BaseRecognizer = None) -> None:
        self.detector = detector
        if self.detector is None:
            self.detector = DoctrDetector()
        
        self.recognizer = recognizer
        if self.recognizer is None:
            self.recognizer = VietOCRRecognizer()

    def parse(self, image: Image.Image):
        # Check for rotation and correct it
        image = ImageProcessor.rotate_image(image)

        # Detect text boxes
        detection = self.detector.detect(image)

        logger.info(f"Detected {len(detection['bboxes'])} text boxes.")
        
        # Recognize text within detected boxes
        text = self.recognizer.recognize(image, bboxes=detection['bboxes'])
        
        return text