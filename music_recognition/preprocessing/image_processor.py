"""
Image preprocessing for handwritten music notation.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class ImagePreprocessor:
    """Handles preprocessing of music score images."""

    def __init__(self, target_size: Tuple[int, int] = (512, 512)):
        """
        Initialize the image preprocessor.

        Args:
            target_size: Target dimensions for resizing images (width, height)
        """
        self.target_size = target_size

    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image from file.

        Args:
            image_path: Path to the image file

        Returns:
            Loaded image as numpy array
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        return image

    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale.

        Args:
            image: Input image

        Returns:
            Grayscale image
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def binarize(self, image: np.ndarray, method: str = 'adaptive') -> np.ndarray:
        """
        Binarize the image using thresholding.

        Args:
            image: Grayscale input image
            method: Binarization method ('adaptive', 'otsu', 'simple')

        Returns:
            Binary image
        """
        if method == 'adaptive':
            binary = cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
        elif method == 'otsu':
            _, binary = cv2.threshold(
                image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )
        else:  # simple
            _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

        return binary

    def denoise(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Apply denoising to the image.

        Args:
            image: Input image
            kernel_size: Size of the morphological kernel

        Returns:
            Denoised image
        """
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        denoised = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        denoised = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
        return denoised

    def deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Correct skew in the image.

        Args:
            image: Binary input image

        Returns:
            Deskewed image
        """
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        if abs(angle) < 0.5:
            return image

        h, w = image.shape
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

        return rotated

    def resize(self, image: np.ndarray, size: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """
        Resize image to target size.

        Args:
            image: Input image
            size: Target size (width, height). Uses self.target_size if None.

        Returns:
            Resized image
        """
        if size is None:
            size = self.target_size
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def normalize(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize pixel values to [0, 1] range.

        Args:
            image: Input image

        Returns:
            Normalized image
        """
        return image.astype(np.float32) / 255.0

    def preprocess(self, image_path: str, apply_deskew: bool = True) -> np.ndarray:
        """
        Complete preprocessing pipeline.

        Args:
            image_path: Path to input image
            apply_deskew: Whether to apply deskewing

        Returns:
            Preprocessed image ready for model input
        """
        image = self.load_image(image_path)
        gray = self.convert_to_grayscale(image)
        binary = self.binarize(gray, method='adaptive')
        denoised = self.denoise(binary)

        if apply_deskew:
            denoised = self.deskew(denoised)

        normalized = self.normalize(denoised)

        return normalized

    def preprocess_array(self, image: np.ndarray, apply_deskew: bool = True) -> np.ndarray:
        """
        Preprocess a numpy array image.

        Args:
            image: Input image as numpy array
            apply_deskew: Whether to apply deskewing

        Returns:
            Preprocessed image
        """
        gray = self.convert_to_grayscale(image)
        binary = self.binarize(gray, method='adaptive')
        denoised = self.denoise(binary)

        if apply_deskew:
            denoised = self.deskew(denoised)

        normalized = self.normalize(denoised)

        return normalized
