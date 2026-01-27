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

        A musical staff consists of EXACTLY 5 horizontal lines.
        This method groups detected lines into staff systems of 5 lines each.

        Args:
            image: Binary input image

        Returns:
            List of staff groups, each containing exactly 5 line positions
        """
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (image * 255).astype(np.uint8)

        # Project horizontally to find line positions
        horizontal_projection = np.sum(image, axis=1)

        # Find peaks (staff lines)
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

        # Group lines into staves (5 lines per staff)
        staff_groups = []
        current_group = []

        # Calculate expected spacing between lines in a staff
        # Lines should be roughly evenly spaced within a staff
        max_line_spacing = self.staff_space_height * 2.5  # Allow some variation

        for i, pos in enumerate(line_positions):
            if not current_group:
                # Start new staff
                current_group.append(pos)
            else:
                spacing = pos - current_group[-1]

                # Check if this line belongs to current staff
                if spacing < max_line_spacing and len(current_group) < 5:
                    current_group.append(pos)
                else:
                    # Current staff is complete or spacing is too large
                    # Validate and save if it has exactly 5 lines
                    if len(current_group) == 5:
                        staff_groups.append(current_group)
                    elif len(current_group) == 4:
                        # Sometimes detection misses one line - add interpolated line
                        avg_spacing = (current_group[-1] - current_group[0]) / 4
                        # Add a 5th line at the expected position
                        current_group.append(int(current_group[-1] + avg_spacing))
                        staff_groups.append(current_group)

                    # Start new staff
                    current_group = [pos]

        # Handle last group
        if len(current_group) == 5:
            staff_groups.append(current_group)
        elif len(current_group) == 4:
            # Add interpolated 5th line
            avg_spacing = (current_group[-1] - current_group[0]) / 4
            current_group.append(int(current_group[-1] + avg_spacing))
            staff_groups.append(current_group)

        # Validate all staves have exactly 5 lines with consistent spacing
        validated_groups = []
        for group in staff_groups:
            if len(group) == 5:
                # Check spacing consistency
                spacings = [group[i+1] - group[i] for i in range(4)]
                avg_spacing = sum(spacings) / len(spacings)

                # All spacings should be within 50% of average
                if all(abs(s - avg_spacing) < avg_spacing * 0.5 for s in spacings):
                    validated_groups.append(group)

        return validated_groups

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
