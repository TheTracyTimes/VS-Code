"""
Demo script for music symbol recognition system.
"""

import argparse
import cv2
import numpy as np
from pathlib import Path

from music_recognition import MusicRecognitionSystem


def visualize_detections(image_path: str, system: MusicRecognitionSystem):
    """
    Visualize detected symbols on the image.

    Args:
        image_path: Path to input image
        system: MusicRecognitionSystem instance
    """
    import matplotlib.pyplot as plt

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    preprocessed = system.preprocessor.preprocess(image_path)

    processed, staff_positions, bboxes = system.staff_detector.process_image(preprocessed)

    detections = system.symbol_detector.detect_symbols(processed, bboxes)

    detections = system.symbol_detector.non_max_suppression(detections, iou_threshold=0.3)

    vis_image = image.copy()
    for det in detections:
        x, y, w, h = det['bbox']
        symbol = det['symbol']
        confidence = det['confidence']

        cv2.rectangle(vis_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        label = f"{symbol}: {confidence:.2f}"
        cv2.putText(vis_image, label, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 255, 0), 1)

    for staff_group in staff_positions:
        for line_y in staff_group:
            cv2.line(vis_image, (0, line_y), (vis_image.shape[1], line_y), (255, 0, 0), 1)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f'Detections ({len(detections)} symbols)')
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description='Demo: Handwritten Music Recognition')
    parser.add_argument('--image', type=str, required=True,
                        help='Path to input image')
    parser.add_argument('--model_path', type=str, default=None,
                        help='Path to trained model checkpoint (optional)')
    parser.add_argument('--output_dir', type=str, default='./output',
                        help='Directory to save output files')
    parser.add_argument('--visualize', action='store_true',
                        help='Visualize detections')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use (cpu or cuda)')
    parser.add_argument('--confidence', type=float, default=0.6,
                        help='Confidence threshold for detections')

    args = parser.parse_args()

    print("="*60)
    print("Handwritten Music Recognition - Demo")
    print("="*60)

    if not Path(args.image).exists():
        print(f"Error: Image file not found: {args.image}")
        return

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nInitializing recognition system...")
    print(f"Device: {args.device}")
    print(f"Confidence threshold: {args.confidence}")

    system = MusicRecognitionSystem(
        model_path=args.model_path,
        device=args.device,
        confidence_threshold=args.confidence
    )

    print(f"\nProcessing image: {args.image}")

    try:
        score = system.recognize(args.image)

        print("\n" + "="*60)
        print("Recognition Results")
        print("="*60)
        print(f"Time signature: {score.time_signature[0]}/{score.time_signature[1]}")
        print(f"Clef: {score.clef}")
        print(f"Number of measures: {len(score.measures)}")

        for i, measure in enumerate(score.measures, 1):
            print(f"\nMeasure {i}: {len(measure)} symbols")
            for symbol in measure:
                if symbol['type'] == 'note':
                    print(f"  - Note: {symbol['pitch']}, duration: {symbol['duration']}")
                else:
                    print(f"  - Rest: duration {symbol['duration']}")

        image_name = Path(args.image).stem

        musicxml_path = output_dir / f"{image_name}.musicxml"
        system.export_score(score, str(musicxml_path), format='musicxml')
        print(f"\nMusicXML exported to: {musicxml_path}")

        abc_path = output_dir / f"{image_name}.abc"
        system.export_score(score, str(abc_path), format='abc')
        print(f"ABC notation exported to: {abc_path}")

        try:
            midi_path = output_dir / f"{image_name}.mid"
            system.export_score(score, str(midi_path), format='midi')
            print(f"MIDI exported to: {midi_path}")
        except ImportError:
            print("Note: MIDI export requires music21 library (pip install music21)")

        if args.visualize:
            print("\nVisualizing detections...")
            visualize_detections(args.image, system)

        print("\n" + "="*60)
        print("Processing completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
