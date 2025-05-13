from app.infrastructure.docloader.models.io import BBox
from app.infrastructure.docloader.interfaces import BaseRecognizer
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from typing import Union, Literal

class ThaiOCRRecognizer(BaseRecognizer):
    def __init__(self):
        self.recognition_model = VisionEncoderDecoderModel.from_pretrained(
            'openthaigpt/thai-trocr',
        )
        self.processor = TrOCRProcessor.from_pretrained('openthaigpt/thai-trocr')

    def recognize(
        self,
        image: Image.Image,
        bboxes: list[BBox],
        output: Literal["list", "str"] = "str",
    ) -> Union[str, list[str]]:
        """
        Recognize text from a list of bounding boxes.

        Args:
            image: PIL.Image.Image
            bboxes: list[BBox]
            output: Literal["list", "str"] = "str"

        Returns:
            Union[str, list[str]]
        """
        texts = []

        for bbox in bboxes:
            box = (
                int(bbox["x1"]),
                int(bbox["y1"]),
                int(bbox["x2"]),
                int(bbox["y2"]),
            )

            crop = image.crop(box)
            pixel_values = self.processor(images=crop, return_tensors="pt").pixel_values
            generated_ids = self.recognition_model.generate(pixel_values)
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            splitted = text.split()

            if splitted and len(splitted[-1]) == 1:
                text = splitted[0]

            print(text, end=" ", flush=True)

            texts.append(text)

        if output == "list":
            return texts

        texts_str = " ".join(texts)

        return texts_str.strip()