from typing import List
import numpy as np
import easyocr
from PIL import Image

from app.infrastructure.docloader.interfaces.base_recognizer import BaseRecognizer
from app.infrastructure.docloader.models.io import BBox

class EnglishRecognizer(BaseRecognizer):
    """
    Recognizer for English text using EasyOCR.
    """
    
    def __init__(self, languages=["en"], gpu=False):
        """
        Initialize the English text recognizer with EasyOCR.
        
        Args:
            languages (list): Languages to detect (default: ["en"])
            gpu (bool): Whether to use GPU acceleration if available (default: False)
        """
        self.reader = easyocr.Reader(languages, gpu=gpu)
        
    def recognize(self, image: Image.Image, bboxes: List[BBox]) -> str:
        """
        Recognize English text in the given image within the specified bounding boxes.

        Args:
            image: Image to be processed
            bboxes: List of bounding boxes to extract text from

        Returns:
            Recognized text as a string
        """
        # Convert PIL Image to numpy array for EasyOCR
        image_np = np.array(image)
        result_texts = []
        
        for bbox in bboxes:
            # Extract coordinates from the bounding box
            x1, y1, x2, y2 = int(bbox["x1"]), int(bbox["y1"]), int(bbox["x2"]), int(bbox["y2"])
            
            # Crop the image based on bounding box
            cropped_image = image_np[y1:y2, x1:x2]
            
            # Perform OCR on the cropped image
            results = self.reader.readtext(cropped_image, detail=0)  # detail=0 returns just the text
            
            # Join all detected text in the bounding box
            text = " ".join(results)
            result_texts.append(text)
        
        # Combine all recognized texts with newlines between them
        return "\n".join(result_texts)