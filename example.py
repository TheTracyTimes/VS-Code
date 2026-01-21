"""
Simple example demonstrating the music recognition system.
"""

import numpy as np
import cv2
from music_recognition import MusicRecognitionSystem


def create_sample_music_image():
    """
    Create a simple synthetic music score image for demonstration.
    This creates a basic staff with a few simple symbols.
    """
    width, height = 800, 200
    image = np.ones((height, width), dtype=np.uint8) * 255

    staff_start_y = 50
    staff_line_spacing = 15

    for i in range(5):
        y = staff_start_y + i * staff_line_spacing
        cv2.line(image, (50, y), (width - 50, y), 0, 2)

    cv2.circle(image, (150, staff_start_y + 2 * staff_line_spacing), 12, 0, 2)

    cv2.circle(image, (250, staff_start_y + staff_line_spacing), 12, 0, 2)
    cv2.line(image, (262, staff_start_y + staff_line_spacing),
             (262, staff_start_y - 20), 0, 2)

    cv2.circle(image, (350, staff_start_y + 3 * staff_line_spacing), 12, 0, -1)
    cv2.line(image, (362, staff_start_y + 3 * staff_line_spacing),
             (362, staff_start_y), 0, 2)

    barline_x = 450
    cv2.line(image, (barline_x, staff_start_y),
             (barline_x, staff_start_y + 4 * staff_line_spacing), 0, 3)

    cv2.imwrite('sample_music.png', image)
    print("Created sample music image: sample_music.png")

    return 'sample_music.png'


def example_basic_usage():
    """Demonstrate basic usage of the system."""
    print("="*60)
    print("Example 1: Basic Usage")
    print("="*60)

    image_path = create_sample_music_image()

    print("\nInitializing Music Recognition System...")
    system = MusicRecognitionSystem(
        model_path=None,
        device='cpu',
        confidence_threshold=0.5
    )

    print("\nNote: This example uses an untrained model for demonstration.")
    print("For actual recognition, train a model first using train.py")

    print(f"\nProcessing image: {image_path}")

    try:
        score = system.recognize(image_path)

        print("\nRecognition completed!")
        print(f"Time signature: {score.time_signature[0]}/{score.time_signature[1]}")
        print(f"Clef: {score.clef}")
        print(f"Number of measures: {len(score.measures)}")

        system.export_score(score, 'example_output.musicxml', format='musicxml')
        print("\nExported to: example_output.musicxml")

        system.export_score(score, 'example_output.abc', format='abc')
        print("Exported to: example_output.abc")

    except Exception as e:
        print(f"Error: {e}")


def example_preprocessing():
    """Demonstrate preprocessing steps."""
    print("\n" + "="*60)
    print("Example 2: Preprocessing Steps")
    print("="*60)

    from music_recognition.preprocessing import ImagePreprocessor, StaffDetector

    image_path = 'sample_music.png'

    preprocessor = ImagePreprocessor()
    staff_detector = StaffDetector()

    print("\nStep 1: Load and preprocess image")
    preprocessed = preprocessor.preprocess(image_path)
    print(f"Preprocessed image shape: {preprocessed.shape}")

    print("\nStep 2: Detect staff lines")
    processed, staff_positions, bboxes = staff_detector.process_image(preprocessed)
    print(f"Found {len(staff_positions)} staff groups")
    print(f"Detected {len(bboxes)} potential symbol regions")

    if staff_positions:
        print(f"First staff has {len(staff_positions[0])} lines")


def example_model_info():
    """Display model information."""
    print("\n" + "="*60)
    print("Example 3: Model Information")
    print("="*60)

    from music_recognition.models import MusicSymbolCNN

    model = MusicSymbolCNN()

    print(f"\nModel: MusicSymbolCNN")
    print(f"Number of classes: {len(MusicSymbolCNN.SYMBOL_CLASSES)}")
    print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")

    print("\nSupported symbol classes:")
    for i, symbol in enumerate(MusicSymbolCNN.SYMBOL_CLASSES):
        print(f"  {i:2d}. {symbol}")


def example_custom_score():
    """Create a custom music score."""
    print("\n" + "="*60)
    print("Example 4: Creating Custom Score")
    print("="*60)

    from music_recognition.postprocessing import MusicScore, NotationConverter

    score = MusicScore()
    score.time_signature = (3, 4)
    score.clef = 'treble'
    score.tempo = 120

    measure1 = [
        {'type': 'note', 'pitch': 'C4', 'duration': 1.0, 'position': (100, 100)},
        {'type': 'note', 'pitch': 'E4', 'duration': 1.0, 'position': (150, 90)},
        {'type': 'note', 'pitch': 'G4', 'duration': 1.0, 'position': (200, 80)},
    ]

    measure2 = [
        {'type': 'note', 'pitch': 'A4', 'duration': 2.0, 'position': (250, 75)},
        {'type': 'rest', 'duration': 1.0, 'position': (300, 90)},
    ]

    score.add_measure(measure1)
    score.add_measure(measure2)

    print(f"\nCreated score with {len(score.measures)} measures")
    print(f"Time signature: {score.time_signature[0]}/{score.time_signature[1]}")

    converter = NotationConverter()
    converter.current_score = score

    converter.export_musicxml('custom_score.musicxml')
    print("Exported to: custom_score.musicxml")

    converter.export_abc('custom_score.abc')
    print("Exported to: custom_score.abc")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" Handwritten Music Recognition System - Examples")
    print("="*70)

    example_basic_usage()

    example_preprocessing()

    example_model_info()

    example_custom_score()

    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)
    print("\nNext steps:")
    print("1. Prepare your dataset (see USAGE_GUIDE.md)")
    print("2. Train the model: python train.py --data_path ./data")
    print("3. Test on your images: python demo.py --image your_score.jpg")
    print("\nFor more information, see README.md and USAGE_GUIDE.md")


if __name__ == '__main__':
    main()
