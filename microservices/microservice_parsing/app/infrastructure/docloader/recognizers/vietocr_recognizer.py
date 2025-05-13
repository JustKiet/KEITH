from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

from app.infrastructure.docloader.models.io import BBox
from app.infrastructure.docloader.interfaces import BaseRecognizer

from PIL import Image
from typing import Union, Literal, Union

class VietOCRRecognizer(BaseRecognizer):
    def __init__(
        self,
        model_name: Literal[
            "vgg_transformer",
            "resnet_transformer",
            "resnet_fpn_transformer",
            "vgg_seq2seq",
            "vgg_convseq2seq",
            "vgg_decoderseq2seq",
            "base",
        ] = "vgg_transformer",
        device: str = "cpu",
        config: Cfg = None,
        **kwargs,
    ):
        if config is not None:
            self.config = config
        else:
            self.config = Cfg.load_config_from_name(model_name)
            self.config['cnn']['pretrained'] = False
            self.config["device"] = device 

        self.recognition_model = Predictor(config=self.config)

    def recognize(
        self,
        image: Image.Image,
        bboxes: list[BBox],
        output: Literal["list", "str"] = "str",
    ) -> Union[str, list[str]]:
        """
        Recognize text from either:
        - A single image and its bounding boxes
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
            text = self.recognition_model.predict(crop)
            splitted = text.split()

            if splitted and len(splitted[-1]) == 1:
                text = splitted[0]

            texts.append(text)

        if output == "list":
            return texts

        texts_str = " ".join(texts)

        return texts_str.strip()
