# Usage Guide - Handwritten Music Recognition System

This guide provides detailed instructions for using the handwritten music recognition system.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Training Your Own Model](#training-your-own-model)
4. [Using the System](#using-the-system)
5. [Evaluation](#evaluation)
6. [Dataset Preparation](#dataset-preparation)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster training)

### Setup

```bash
# Clone or navigate to the repository
cd VS-Code

# Install dependencies
pip install -r requirements.txt

# For MIDI export support (optional)
pip install music21
```

## Quick Start

### Demo with Pre-trained Model

```bash
# Run demo on a sample image
python demo.py --image path/to/music_score.jpg --visualize

# Specify output directory
python demo.py --image score.jpg --output_dir ./results --visualize
```

### Python API Usage

```python
from music_recognition import MusicRecognitionSystem

# Initialize system
system = MusicRecognitionSystem(
    model_path='checkpoints/best_model.pth',  # Optional
    device='cuda',  # or 'cpu'
    confidence_threshold=0.6
)

# Recognize music from image
score = system.recognize('handwritten_music.jpg')

# Export to different formats
system.export_score(score, 'output.musicxml', format='musicxml')
system.export_score(score, 'output.mid', format='midi')
system.export_score(score, 'output.abc', format='abc')

# Access score data
print(f"Time signature: {score.time_signature}")
print(f"Clef: {score.clef}")
print(f"Measures: {len(score.measures)}")
```

## Training Your Own Model

### Using Synthetic Data (for testing)

```bash
# Quick test with synthetic data
python train.py --synthetic --epochs 10 --batch_size 32
```

### Using Real Dataset

#### 1. Prepare Your Dataset

Organize your data in the following structure:

```
data/
├── train/
│   ├── treble_clef/
│   │   ├── img001.png
│   │   ├── img002.png
│   │   └── ...
│   ├── quarter_note/
│   │   ├── img001.png
│   │   └── ...
│   └── ... (other symbol classes)
└── val/
    ├── treble_clef/
    ├── quarter_note/
    └── ...
```

#### 2. Train the Model

```bash
# Standard training
python train.py \
    --data_path ./data \
    --epochs 100 \
    --batch_size 32 \
    --lr 0.001 \
    --device cuda

# Lightweight model (faster, less accurate)
python train.py \
    --data_path ./data \
    --model_type lightweight \
    --epochs 50 \
    --batch_size 64
```

#### 3. Monitor Training

Checkpoints are saved to `checkpoints/` directory:
- `best_model.pth` - Best performing model
- `checkpoint_epoch_N.pth` - Periodic checkpoints
- `training_history.json` - Training metrics

## Using the System

### Command Line Interface

```bash
# Basic usage
python demo.py --image score.jpg

# With custom model
python demo.py \
    --image score.jpg \
    --model_path checkpoints/best_model.pth \
    --output_dir ./output \
    --visualize

# Adjust confidence threshold
python demo.py \
    --image score.jpg \
    --confidence 0.7 \
    --device cuda
```

### Batch Processing

```python
from music_recognition import MusicRecognitionSystem
from pathlib import Path

system = MusicRecognitionSystem(model_path='checkpoints/best_model.pth')

# Process multiple images
image_paths = list(Path('images/').glob('*.jpg'))
scores = system.batch_recognize(image_paths)

# Export all results
for i, score in enumerate(scores):
    system.export_score(score, f'output_{i}.musicxml', format='musicxml')
```

### Working with Individual Components

#### Preprocessing Only

```python
from music_recognition.preprocessing import ImagePreprocessor, StaffDetector

preprocessor = ImagePreprocessor()
staff_detector = StaffDetector()

# Preprocess image
preprocessed = preprocessor.preprocess('score.jpg')

# Detect staff lines
processed, staff_positions, bboxes = staff_detector.process_image(preprocessed)
```

#### Model Inference Only

```python
from music_recognition.models import MusicSymbolCNN, SymbolDetector
import torch

# Load model
model = MusicSymbolCNN(num_classes=26)
model.load_state_dict(torch.load('checkpoints/best_model.pth'))

detector = SymbolDetector(model, device='cpu')

# Detect symbols
detections = detector.detect_symbols(image, bboxes)
```

## Evaluation

### Evaluate Trained Model

```bash
# Basic evaluation
python evaluate.py \
    --model_path checkpoints/best_model.pth \
    --data_path ./data

# With confusion matrix visualization
python evaluate.py \
    --model_path checkpoints/best_model.pth \
    --data_path ./data \
    --save_cm confusion_matrix.png

# Evaluate lightweight model
python evaluate.py \
    --model_path checkpoints/best_model.pth \
    --model_type lightweight \
    --data_path ./data
```

### Metrics Reported

- Overall accuracy
- Per-class precision, recall, F1-score
- Confusion matrix
- Most common classification errors

## Dataset Preparation

### Supported Datasets

The system works with standard OMR datasets:

1. **HOMUS** (Handwritten Online Musical Symbols)
2. **CVC-MUSCIMA** (handwritten music score images)
3. **Custom datasets** in the required format

### Creating Custom Dataset

1. Collect images of individual music symbols
2. Organize into class directories
3. Recommended image format: PNG or JPG
4. Recommended size: 64x64 to 128x128 pixels
5. Split into train/val sets (80/20 typical)

### Supported Symbol Classes

```python
from music_recognition.models import MusicSymbolCNN

# View all supported classes
print(MusicSymbolCNN.SYMBOL_CLASSES)
```

Default classes include:
- Clefs: treble, bass, alto
- Notes: whole, half, quarter, eighth, sixteenth
- Rests: whole, half, quarter, eighth, sixteenth
- Accidentals: sharp, flat, natural
- Time signatures: 2/4, 3/4, 4/4, 6/8
- Other: barlines, dots, beams, stems

## Advanced Usage

### Custom Model Architecture

```python
from music_recognition.models import MusicSymbolCNN
import torch.nn as nn

class CustomMusicCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Define your custom architecture
        pass

    def forward(self, x):
        # Define forward pass
        pass

# Use in training
model = CustomMusicCNN(num_classes=26)
```

### Custom Data Augmentation

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

custom_transform = A.Compose([
    A.Resize(64, 64),
    A.Rotate(limit=20, p=0.5),
    A.GaussNoise(p=0.3),
    A.RandomBrightnessContrast(p=0.3),
    A.Normalize(mean=[0.0], std=[1.0]),
    ToTensorV2()
])

# Use in dataset
from dataset import MusicSymbolDataset

dataset = MusicSymbolDataset(
    data_dir='./data',
    split='train',
    transform=custom_transform
)
```

### Export Format Customization

```python
from music_recognition.postprocessing import NotationConverter

converter = NotationConverter()
score = converter.symbols_to_score(detections, staff_positions)

# Customize score attributes
score.tempo = 140
score.time_signature = (3, 4)
score.key_signature = 2  # D major

# Export
converter.current_score = score
converter.export_musicxml('custom_output.xml')
```

## Troubleshooting

### Common Issues

#### 1. Model Not Loading

```python
# Ensure model architecture matches checkpoint
model = MusicSymbolCNN(num_classes=26)  # Must match training

# Load with error handling
try:
    checkpoint = torch.load('model.pth', map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
except Exception as e:
    print(f"Error loading model: {e}")
```

#### 2. Poor Recognition Accuracy

- Check image quality (clear, high contrast)
- Ensure proper preprocessing
- Adjust confidence threshold
- Retrain with more data
- Use appropriate model size

#### 3. Out of Memory Errors

```bash
# Reduce batch size
python train.py --batch_size 16

# Use lightweight model
python train.py --model_type lightweight

# Use CPU instead of GPU
python train.py --device cpu
```

#### 4. MIDI Export Issues

```bash
# Install music21
pip install music21

# Configure music21 (first time)
python -c "import music21; music21.configure.run()"
```

### Performance Optimization

```python
# Use GPU if available
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Enable GPU optimizations
torch.backends.cudnn.benchmark = True

# Use mixed precision training (PyTorch >= 1.6)
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
# Use in training loop
```

### Getting Help

For issues not covered here:

1. Check the README.md for overview
2. Review example code in demo.py
3. Examine model architecture in models/
4. Consult preprocessing code for image issues

## Best Practices

1. **Data Quality**: Use high-quality, clear images
2. **Data Augmentation**: Apply appropriate augmentations during training
3. **Validation**: Always use a separate validation set
4. **Checkpointing**: Save models regularly during training
5. **Testing**: Test on diverse handwriting styles
6. **Preprocessing**: Ensure consistent preprocessing between training and inference

## Next Steps

- Experiment with different architectures
- Collect more training data
- Fine-tune hyperparameters
- Integrate with music notation software
- Build a web interface
- Add support for more complex notations
