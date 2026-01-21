"""
Symbol detection and recognition pipeline.
"""

import torch
import cv2
import numpy as np
from typing import List, Tuple, Dict
from .cnn_classifier import MusicSymbolCNN


class SymbolDetector:
    """Detects and classifies music symbols in score images."""

    def __init__(self, model: MusicSymbolCNN, device: str = 'cpu', confidence_threshold: float = 0.5):
        """
        Initialize symbol detector.

        Args:
            model: Trained CNN model for symbol classification
            device: Device to run inference on ('cpu' or 'cuda')
            confidence_threshold: Minimum confidence for a detection
        """
        self.model = model
        self.device = device
        self.confidence_threshold = confidence_threshold
        self.model.to(device)
        self.model.eval()

    def preprocess_symbol(self, symbol_image: np.ndarray, target_size: Tuple[int, int] = (64, 64)) -> torch.Tensor:
        """
        Preprocess a symbol image for model input.

        Args:
            symbol_image: Symbol image as numpy array
            target_size: Target size for the symbol

        Returns:
            Preprocessed tensor
        """
        if len(symbol_image.shape) == 3:
            symbol_image = cv2.cvtColor(symbol_image, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(symbol_image, target_size, interpolation=cv2.INTER_AREA)

        normalized = resized.astype(np.float32) / 255.0

        tensor = torch.from_numpy(normalized).unsqueeze(0).unsqueeze(0)

        return tensor.to(self.device)

    def detect_symbols(self, image: np.ndarray, bounding_boxes: List[Tuple[int, int, int, int]]) -> List[Dict]:
        """
        Detect and classify symbols from bounding boxes.

        Args:
            image: Input image
            bounding_boxes: List of bounding boxes (x, y, w, h)

        Returns:
            List of detected symbols with metadata
        """
        detections = []

        for bbox in bounding_boxes:
            x, y, w, h = bbox

            if image.dtype == np.float32 or image.dtype == np.float64:
                symbol_img = (image[y:y+h, x:x+w] * 255).astype(np.uint8)
            else:
                symbol_img = image[y:y+h, x:x+w]

            if symbol_img.size == 0:
                continue

            symbol_tensor = self.preprocess_symbol(symbol_img)

            with torch.no_grad():
                predictions, probs = self.model.predict(symbol_tensor)

            pred_idx = predictions.item()
            confidence = probs[0, pred_idx].item()

            if confidence >= self.confidence_threshold:
                symbol_name = MusicSymbolCNN.get_class_name(pred_idx)

                if symbol_name != 'background':
                    detections.append({
                        'symbol': symbol_name,
                        'confidence': confidence,
                        'bbox': bbox,
                        'position': (x + w // 2, y + h // 2)
                    })

        detections.sort(key=lambda d: d['position'][0])

        return detections

    def batch_detect(self, images: List[np.ndarray], all_bboxes: List[List[Tuple[int, int, int, int]]]) -> List[List[Dict]]:
        """
        Detect symbols in multiple images.

        Args:
            images: List of input images
            all_bboxes: List of bounding box lists for each image

        Returns:
            List of detection lists for each image
        """
        all_detections = []

        for image, bboxes in zip(images, all_bboxes):
            detections = self.detect_symbols(image, bboxes)
            all_detections.append(detections)

        return all_detections

    def non_max_suppression(self, detections: List[Dict], iou_threshold: float = 0.5) -> List[Dict]:
        """
        Apply non-maximum suppression to remove overlapping detections.

        Args:
            detections: List of detected symbols
            iou_threshold: IoU threshold for suppression

        Returns:
            Filtered list of detections
        """
        if not detections:
            return []

        detections.sort(key=lambda d: d['confidence'], reverse=True)

        kept = []

        while detections:
            best = detections.pop(0)
            kept.append(best)

            x1, y1, w1, h1 = best['bbox']

            filtered = []
            for det in detections:
                x2, y2, w2, h2 = det['bbox']

                xi1 = max(x1, x2)
                yi1 = max(y1, y2)
                xi2 = min(x1 + w1, x2 + w2)
                yi2 = min(y1 + h1, y2 + h2)

                inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
                box1_area = w1 * h1
                box2_area = w2 * h2
                union_area = box1_area + box2_area - inter_area

                iou = inter_area / union_area if union_area > 0 else 0

                if iou < iou_threshold:
                    filtered.append(det)

            detections = filtered

        return kept
