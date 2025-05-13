from PIL import Image, ImageOps
from torchvision.ops import nms
import torch
import numpy as np
from typing import Union, Tuple, overload

class BBoxProcessor:
    """
    A class to process bounding boxes for images.
    """

    @staticmethod
    def expand_bbox(x1: float,
                    y1: float, 
                    x2: float, 
                    y2: float, 
                    img_width: float, 
                    img_height: float, 
                    expand_ratio: float = 0.01
                    ) -> tuple[float, float, float, float]:
        """Expand a bbox by a given ratio while keeping it within image bounds."""
        w = x2 - x1
        h = y2 - y1

        dw = w * expand_ratio
        dh = h * expand_ratio

        new_x1 = max(0, x1 - dw)
        new_y1 = max(0, y1 - dh)
        new_x2 = min(img_width, x2 + dw)
        new_y2 = min(img_height, y2 + dh)

        return new_x1, new_y1, new_x2, new_y2
    
    @overload
    @staticmethod
    def filter_and_sort_boxes(pred_bboxes: torch.Tensor,
                              pred_labels: torch.Tensor,
                              pred_scores: torch.Tensor,
                              label_id: int,
                              conf_threshold: float = 0.75,
                              iou_threshold: float = 0.3) -> Tuple[torch.Tensor, torch.Tensor]: ...
    
    @overload
    @staticmethod
    def filter_and_sort_boxes(pred_bboxes: np.ndarray,
                              pred_labels: np.ndarray,
                              pred_scores: np.ndarray,
                              label_id: int,
                              conf_threshold: float = 0.75,
                              iou_threshold: float = 0.3) -> Tuple[torch.Tensor, torch.Tensor]: ...

    @staticmethod
    def filter_and_sort_boxes(pred_bboxes: list[list[float]],
                              pred_labels: list[int],
                              pred_scores: list[float],
                              label_id: int,
                              conf_threshold: float = 0.75,
                              iou_threshold: float = 0.3) -> list:
        if not isinstance(pred_bboxes, torch.Tensor):
            pred_bboxes = torch.tensor(pred_bboxes)
        if not isinstance(pred_labels, torch.Tensor):
            pred_labels = torch.tensor(pred_labels)
        if not isinstance(pred_scores, torch.Tensor):
            pred_scores = torch.tensor(pred_scores)

        mask = (pred_labels == label_id) & (pred_scores > conf_threshold)
        boxes = pred_bboxes[mask]
        scores = pred_scores[mask]
        
        # Apply NMS to remove overlapping boxes
        keep_indices = nms(boxes, scores, iou_threshold)
        boxes = boxes[keep_indices]

        # Sort boxes: by y_min if rows/headers, x_min if columns
        if label_id in [2, 3]:  # rows or headers
            sorted_boxes = sorted(boxes.tolist(), key=lambda box: box[1])
        else:  # columns
            sorted_boxes = sorted(boxes.tolist(), key=lambda box: box[0])

        return sorted_boxes

    @overload
    @staticmethod
    def get_bbox_containment_ratio(bbox1: list[float], bbox2: list[float]) -> float: ...

    @staticmethod
    def get_bbox_containment_ratio(bbox1: tuple[float, float, float, float], 
                                   bbox2: tuple[float, float, float, float]) -> float:
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2

        # Intersection coordinates
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        # Compute intersection area
        inter_w = max(0, inter_x_max - inter_x_min)
        inter_h = max(0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h

        # bbox1 area
        bbox1_area = (x1_max - x1_min) * (y1_max - y1_min)

        if bbox1_area == 0:
            return 0.0  # Avoid division by zero

        # Percentage of bbox1 inside bbox2
        return inter_area / bbox1_area

    @overload
    @staticmethod
    def get_intersection_box(bbox1: list[float], boxx2: list[float]) -> Union[None, tuple[float, float, float, float]]: ...

    @staticmethod
    def get_intersection_box(bbox1: tuple[float, float, float, float], 
                             bbox2: tuple[float, float, float, float]) -> Union[None, tuple[float, float, float, float]]:
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])

        if x2 <= x1 or y2 <= y1:
            return None  # No intersection

        return (x1, y1, x2, y2) 
    
    @staticmethod
    def resize_to_aspect(image: Image.Image, aspect_ratio=(16, 9), fill_color=(255, 255, 255)):
        """Resize image to the target aspect ratio by padding."""
        img_w, img_h = image.size
        target_w = img_w
        target_h = int(target_w * aspect_ratio[1] / aspect_ratio[0])

        if target_h < img_h:
            target_h = img_h
            target_w = int(target_h * aspect_ratio[0] / aspect_ratio[1])

        pad_w = (target_w - img_w) // 2
        pad_h = (target_h - img_h) // 2

        return ImageOps.expand(image, (pad_w, pad_h, pad_w, pad_h), fill=fill_color)
    
    @staticmethod
    def intersection_area(bbox1: tuple[float, float, float, float], 
                          bbox2: tuple[float, float, float, float]) -> float:
        x_left   = max(bbox1[0], bbox2[0])
        y_top    = max(bbox1[1], bbox2[1])
        x_right  = min(bbox1[2], bbox2[2])
        y_bottom = min(bbox1[3], bbox2[3])

        if x_right < x_left or y_bottom < y_top:
            return 0  # no overlap

        return (x_right - x_left) * (y_bottom - y_top)