from doctr.io import DocumentFile
from doctr.io.elements import Document
from doctr.models.detection import detection_predictor
from doctr.models.builder import DocumentBuilder

from app.infrastructure.docloader.interfaces import BaseDetector
from app.infrastructure.docloader.models.io import BBox, DetectionOutput

from typing import Literal, Union
import base64
from PIL import Image
import numpy as np
import io

class DoctrDetector(BaseDetector):
    """
    Doctr Detector class for document detection.
    """
    def __init__(self,
                 model_name: Literal[
                    "db_resnet34",
                    "db_resnet50",
                    "db_mobilenet_v3_large",
                    "linknet_resnet18",
                    "linknet_resnet34",
                    "linknet_resnet50",
                    "fast_tiny",
                    "fast_small",
                    "fast_base",
                 ] = "db_resnet50",
                 pretrained: bool = True,
                 assume_straight_pages: bool = True,
                 preserve_aspect_ratio: bool = True,
                 symmetric_pad: bool = True,
                 batch_size: int = 2):
        self.detection_model = detection_predictor(
            arch=model_name,
            pretrained=pretrained,
            assume_straight_pages=assume_straight_pages,
            preserve_aspect_ratio=preserve_aspect_ratio,
            symmetric_pad=symmetric_pad,
            batch_size=batch_size,
        )
        self._builder = DocumentBuilder()

    def _build_document_layout(self, 
                               np_doc: list[np.ndarray],
                               detection_result: Union[list[dict[str, np.ndarray]], tuple[list[dict[str, np.ndarray]], list[np.ndarray]]],
                               ) -> Document:
        # Required shapes
        page_shapes = [np.array(np_doc[0]).shape[:2]]  # [(H, W)]
        boxes = list(detection_result[0].values())[0][:, :4]  # (N, 4)
        scores = list(detection_result[0].values())[0][:, 4]  # (N,)

        # Dummy text predictions: you can leave text blank
        dummy_text_preds = [[("", 1.0) for _ in range(len(boxes))]]

        # Dummy crop orientations: no rotation
        dummy_crop_orientations = [{"value": 0, "confidence": None} for _ in range(len(boxes))]

        # Document-level orientation: None or 0
        dummy_orientations = [{"value": 0, "confidence": None}]

        # Optional: skip language detection
        dummy_languages = None

        return self._builder(
            pages=[np.array(np_doc[0])],
            boxes=[boxes],
            objectness_scores=[scores],
            text_preds=dummy_text_preds,
            page_shapes=page_shapes,
            crop_orientations=[dummy_crop_orientations],
            orientations=dummy_orientations,
            languages=dummy_languages
        )

    def detect(self, image: Image.Image) -> DetectionOutput:
        """
        Detect anomalies in the given data.

        Args:
            images: Image or list of images to be processed.

        Returns:
            Detected bounding boxes.
        """

        if image.mode != "RGB":
            image = image.convert("RGB")

        with io.BytesIO() as buffer:
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

        doc = DocumentFile.from_images([image_bytes])
        detection_result = self.detection_model(doc)

        layout = self._build_document_layout(
            np_doc=doc,
            detection_result=detection_result
        )

        w, h = image.size
        bboxes: list[BBox] = [
            BBox(
                x1=word.geometry[0][0] * w,
                y1=word.geometry[0][1] * h,
                x2=word.geometry[1][0] * w,
                y2=word.geometry[1][1] * h,
                label=word.value  # optional
            )
            for block in layout.pages[0].blocks
            for line in block.lines
            for word in line.words
        ]

        return DetectionOutput(
            image=base64_image,
            bboxes=bboxes
        )