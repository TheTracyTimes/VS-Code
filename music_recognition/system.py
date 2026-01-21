"""
Main music recognition system that integrates all components.
"""

import torch
import numpy as np
from pathlib import Path
from typing import Optional, Union

from .preprocessing import ImagePreprocessor, StaffDetector
from .models import MusicSymbolCNN, SymbolDetector
from .postprocessing import NotationConverter, MusicScore


class MusicRecognitionSystem:
    """
    Complete system for recognizing handwritten music notation.

    This class integrates preprocessing, symbol detection, and notation conversion
    to provide an end-to-end solution for optical music recognition.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        device: str = 'cpu',
        confidence_threshold: float = 0.6
    ):
        """
        Initialize the music recognition system.

        Args:
            model_path: Path to trained model weights. If None, creates untrained model.
            device: Device to run inference on ('cpu' or 'cuda')
            confidence_threshold: Minimum confidence for symbol detection
        """
        self.device = device
        self.preprocessor = ImagePreprocessor(target_size=(512, 512))
        self.staff_detector = StaffDetector()

        self.model = MusicSymbolCNN(num_classes=len(MusicSymbolCNN.SYMBOL_CLASSES))

        if model_path and Path(model_path).exists():
            self.load_model(model_path)

        self.symbol_detector = SymbolDetector(
            self.model,
            device=device,
            confidence_threshold=confidence_threshold
        )

        self.notation_converter = NotationConverter()

    def load_model(self, model_path: str):
        """
        Load model weights from file.

        Args:
            model_path: Path to model checkpoint
        """
        checkpoint = torch.load(model_path, map_location=self.device)

        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            self.model.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.model.load_state_dict(checkpoint)

        self.model.to(self.device)
        self.model.eval()
        print(f"Model loaded from {model_path}")

    def recognize(self, image_path: str) -> MusicScore:
        """
        Recognize music notation from an image file.

        Args:
            image_path: Path to the image file

        Returns:
            MusicScore object containing the recognized notation
        """
        preprocessed = self.preprocessor.preprocess(image_path)

        processed, staff_positions, bboxes = self.staff_detector.process_image(preprocessed)

        detections = self.symbol_detector.detect_symbols(processed, bboxes)

        detections = self.symbol_detector.non_max_suppression(detections, iou_threshold=0.3)

        score = self.notation_converter.symbols_to_score(detections, staff_positions)

        return score

    def recognize_array(self, image: np.ndarray) -> MusicScore:
        """
        Recognize music notation from an image array.

        Args:
            image: Image as numpy array

        Returns:
            MusicScore object containing the recognized notation
        """
        preprocessed = self.preprocessor.preprocess_array(image)

        processed, staff_positions, bboxes = self.staff_detector.process_image(preprocessed)

        detections = self.symbol_detector.detect_symbols(processed, bboxes)

        detections = self.symbol_detector.non_max_suppression(detections, iou_threshold=0.3)

        score = self.notation_converter.symbols_to_score(detections, staff_positions)

        return score

    def batch_recognize(self, image_paths: list) -> list:
        """
        Recognize music notation from multiple images.

        Args:
            image_paths: List of image file paths

        Returns:
            List of MusicScore objects
        """
        scores = []
        for path in image_paths:
            score = self.recognize(path)
            scores.append(score)
        return scores

    def export_score(
        self,
        score: MusicScore,
        output_path: str,
        format: str = 'musicxml'
    ):
        """
        Export a music score to a file.

        Args:
            score: MusicScore object to export
            output_path: Path to save the file
            format: Export format ('musicxml', 'midi', or 'abc')
        """
        self.notation_converter.current_score = score

        if format.lower() == 'musicxml':
            self.notation_converter.export_musicxml(output_path)
        elif format.lower() == 'midi':
            self.notation_converter.export_midi(output_path)
        elif format.lower() == 'abc':
            self.notation_converter.export_abc(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

        print(f"Score exported to {output_path}")


class RecognitionResult:
    """Container for recognition results with export capabilities."""

    def __init__(self, score: MusicScore, system: MusicRecognitionSystem):
        """
        Initialize recognition result.

        Args:
            score: MusicScore object
            system: MusicRecognitionSystem instance for exporting
        """
        self.score = score
        self.system = system

    def export_musicxml(self, output_path: str):
        """Export to MusicXML format."""
        self.system.export_score(self.score, output_path, format='musicxml')

    def export_midi(self, output_path: str):
        """Export to MIDI format."""
        self.system.export_score(self.score, output_path, format='midi')

    def export_abc(self, output_path: str):
        """Export to ABC notation format."""
        self.system.export_score(self.score, output_path, format='abc')

    def to_dict(self):
        """Get dictionary representation of the score."""
        return self.score.to_dict()
