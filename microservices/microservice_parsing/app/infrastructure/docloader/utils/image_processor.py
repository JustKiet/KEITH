from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2
from typing import Literal
from loguru import logger
import base64
import io
import mimetypes

class ImageProcessor:
    @staticmethod
    def enhance_image(image: Image.Image) -> Image.Image:
        """Enhance the image to improve OCR accuracy while preserving fine details."""

        # Chuyển sang đen trắng
        image = image.convert("L")
        # Tăng độ tương phản
        image = ImageEnhance.Contrast(image).enhance(2.0)
        # Tăng độ nét
        image = image.filter(ImageFilter.SHARPEN)
        # Resize x1.5
        image = image.resize((int(image.width * 1.5), int(image.height * 1.5)), resample=Image.LANCZOS)

        return image


    @staticmethod
    def detect_rotation_contour(image: Image.Image) -> float:
        """Detects the skew angle of text using contour-based rotation."""
        # Convert PIL image to grayscale NumPy array
        image_np = np.array(image.convert("L"))

        # Apply binary thresholding
        _, thresh = cv2.threshold(image_np, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            logger.warning("No text detected.")
            return 0

        # Get the minimum area bounding box for the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest_contour)
        angle = rect[-1]

        # Adjust angle to be within -45 to +45 degrees
        if angle < -45:
            angle += 90

        logger.info(f"Detected rotation angle: {angle}°")
        return angle

    @staticmethod
    def detect_rotation_hough(image: Image.Image) -> int:
        """Detects rotation using Hough Line Transform and returns 90° or 180° correction."""
        # Convert PIL image to grayscale NumPy array
        image_np = np.array(image.convert("L"))

        # Apply edge detection
        edges = cv2.Canny(image_np, 50, 150, apertureSize=3)

        # Detect lines using Hough Transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        if lines is None:
            logger.warning("No lines detected.")
            return 0  # No rotation needed

        # Compute the dominant angle
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90  # Convert from radians to degrees
            angles.append(angle)

        avg_angle = np.median(angles)  # Use median to avoid outliers

        # Normalize to closest 90° or 180°
        if -135 < avg_angle < -80:
            corrected_angle = 90
        elif -180 < avg_angle < -135 or 45 < avg_angle < 135:
            corrected_angle = 180
        else:
            corrected_angle = 0  # No rotation needed

        logger.info(f"Detected skew: {avg_angle}° -> Rotating by {corrected_angle}°")
        return corrected_angle

    @staticmethod
    def rotate_image(image: Image.Image,
                     method: Literal["hough", "contour"] = "hough") -> Image.Image:
        """Rotate the image based on the detected angle while preserving all content."""
        
        if method == "hough":
            rotation_value = ImageProcessor.detect_rotation_hough(image)
        elif method == "contour":
            rotation_value = ImageProcessor.detect_rotation_contour(image)

        if rotation_value == 0:
            return image  # No rotation needed

        # Convert PIL image to NumPy
        image_np = np.array(image)

        # Get image dimensions
        h, w = image_np.shape[:2]

        # Compute rotation matrix with expanded bounds
        center = (w // 2, h // 2)
        rot_mat = cv2.getRotationMatrix2D(center, -rotation_value, 1.0)  # Negative for correct direction

        # Compute new bounding box size
        cos = np.abs(rot_mat[0, 0])
        sin = np.abs(rot_mat[0, 1])
        new_w = int(h * sin + w * cos)
        new_h = int(h * cos + w * sin)

        # Adjust transformation matrix
        rot_mat[0, 2] += (new_w - w) / 2
        rot_mat[1, 2] += (new_h - h) / 2

        # Apply rotation with new canvas size
        rotated_np = cv2.warpAffine(image_np, rot_mat, (new_w, new_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

        # Convert back to PIL image
        return Image.fromarray(rotated_np)
    
    @staticmethod
    def encode_image(image: Image.Image) -> str:
        """
        Encode the image into a base64 string.

        Args:
            image (Image.Image): The PIL image object.

        Returns:
            str: The base64-encoded image string.
        """
        encoded_string = base64.b64encode(image).decode('utf-8')
        return encoded_string
    
    @staticmethod
    def decode_image(encoded_string: str) -> Image.Image:
        """
        Decode a base64 string into a PIL image.

        Args:
            encoded_string (str): The base64-encoded image string.

        Returns:
            Image.Image: The decoded PIL image object.
        """
        decoded_bytes = base64.b64decode(encoded_string)
        return Image.open(io.BytesIO(decoded_bytes))
    
    @staticmethod
    def construct_png(image: Image.Image) -> bytes:
        """
        Construct a valid PNG image from the PIL image.

        Args:
            image (Image.Image): The PIL image object.
        
        Returns:
            bytes: The .PNG image bytes.
        """
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    
    @staticmethod
    def validate_image_path(image_path: str) -> Literal["image/jpeg", "image/png"]:
        """
        Validate that the file is a JPG, JPEG, or PNG.

        Args:
            image_path (str): The path to the image file.

        Returns:
            Literal["image/jpeg", "image/png"]: The mime type of the image.
        """
        valid_mime_types = {"image/jpeg", "image/png"}
        file_type = mimetypes.guess_type(image_path)[0]
        
        if file_type not in valid_mime_types:
            raise ValueError(f"Invalid file type: {file_type}. Only JPG, JPEG, and PNG are allowed.")
        
        return file_type
