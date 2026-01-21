"""
Staff line detection and removal for music scores.
"""

import cv2
import numpy as np
from typing import List, Tuple


class StaffDetector:
    """Detects and processes staff lines in music notation."""

    def __init__(self, staff_line_thickness: int = 2, staff_space_height: int = 10):
        """
        Initialize staff detector.

        Args:
            staff_line_thickness: Expected thickness of staff lines in pixels
            staff_space_height: Expected height between staff lines in pixels
        """
        self.staff_line_thickness = staff_line_thickness
        self.staff_space_height = staff_space_height

    def detect_horizontal_lines(self, image: np.ndarray, min_line_length: int = 100) -> np.ndarray:
        """
        Detect horizontal lines using morphological operations.

        Args:
            image: Binary input image
            min_line_length: Minimum length for a line to be considered

        Returns:
            Image with detected horizontal lines
        """
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (min_line_length, 1)
        )

        detected_lines = cv2.morphologyEx(
            image,
            cv2.MORPH_OPEN,
            horizontal_kernel,
            iterations=1
        )

        return detected_lines

    def find_staff_positions(self, image: np.ndarray) -> List[List[int]]:
        """
        Find vertical positions of staff lines.

        Args:
            image: Binary input image

        Returns:
            List of staff groups, each containing 5 line positions
        """
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)

        horizontal_projection = np.sum(image, axis=1)

        threshold = np.max(horizontal_projection) * 0.3
        line_positions = []

        in_line = False
        line_start = 0

        for i, val in enumerate(horizontal_projection):
            if val > threshold and not in_line:
                in_line = True
                line_start = i
            elif val <= threshold and in_line:
                in_line = False
                line_center = (line_start + i) // 2
                line_positions.append(line_center)

        staff_groups = []
        current_group = []

        for i, pos in enumerate(line_positions):
            if not current_group:
                current_group.append(pos)
            else:
                if pos - current_group[-1] < self.staff_space_height * 3:
                    current_group.append(pos)
                else:
                    if len(current_group) >= 4:
                        staff_groups.append(current_group)
                    current_group = [pos]

        if len(current_group) >= 4:
            staff_groups.append(current_group)

        return staff_groups

    def remove_staff_lines(self, image: np.ndarray, staff_positions: List[List[int]]) -> np.ndarray:
        """
        Remove staff lines from the image.

        Args:
            image: Binary input image
            staff_positions: List of staff line positions

        Returns:
            Image with staff lines removed
        """
        result = image.copy()

        if result.dtype == np.float32 or result.dtype == np.float64:
            result = (result * 255).astype(np.uint8)

        thickness = self.staff_line_thickness + 1

        for staff_group in staff_positions:
            for line_y in staff_group:
                y_start = max(0, line_y - thickness)
                y_end = min(result.shape[0], line_y + thickness)
                result[y_start:y_end, :] = 0

        return result

    def extract_symbols(self, image: np.ndarray) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
        """
        Extract individual symbols from the image.

        Args:
            image: Binary image with staff lines removed

        Returns:
            Tuple of (processed image, list of bounding boxes)
        """
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)

        contours, _ = cv2.findContours(
            image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        bounding_boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w > 5 and h > 5:
                bounding_boxes.append((x, y, w, h))

        bounding_boxes.sort(key=lambda box: (box[1], box[0]))

        return image, bounding_boxes

    def process_image(self, image: np.ndarray) -> Tuple[np.ndarray, List[List[int]], List[Tuple[int, int, int, int]]]:
        """
        Complete staff processing pipeline.

        Args:
            image: Binary input image

        Returns:
            Tuple of (processed image, staff positions, symbol bounding boxes)
        """
        staff_lines = self.detect_horizontal_lines(image)

        staff_positions = self.find_staff_positions(staff_lines)

        image_no_staff = self.remove_staff_lines(image, staff_positions)

        processed, bboxes = self.extract_symbols(image_no_staff)

        return processed, staff_positions, bboxes
