# Music Symbol Recognition - Training Guide

This guide explains how to train the AI model to recognize handwritten music notation symbols.

## Table of Contents

1. [Overview](#overview)
2. [Preparing Training Data](#preparing-training-data)
3. [Training the Model](#training-the-model)
4. [Evaluating Performance](#evaluating-performance)
5. [Using the Trained Model](#using-the-trained-model)
6. [Tips for Better Accuracy](#tips-for-better-accuracy)

---

## Overview

The music recognition system uses a Convolutional Neural Network (CNN) to identify handwritten music symbols. The model needs to be trained on labeled examples before it can accurately recognize notation.

### What the Model Recognizes:

- **Clefs**: Treble, Bass, Alto
- **Notes**: Whole, Half, Quarter, Eighth, Sixteenth
- **Rests**: Whole, Half, Quarter, Eighth, Sixteenth
- **Accidentals**: Sharp, Flat, Natural
- **Time Signatures**: 2/4, 3/4, 4/4, 6/8, etc.
- **Other**: Barlines, dots, beams, stems

### Training Requirements:

- **Minimum**: 100 images per symbol class (~2,500 total images)
- **Recommended**: 500+ images per class (~12,500+ total images)
- **Ideal**: 1,000+ images per class (~25,000+ total images)

More training data = better accuracy!

---

## Preparing Training Data

### Step 1: Collect Symbol Images

You need images of each symbol type. These should be:

- **Grayscale** or color (converted to grayscale automatically)
- **64x64 pixels or larger** (resized automatically)
- **Clear and well-lit** photos or scans
- **One symbol per image** (cropped)

### Step 2: Organize into Folders

Create a directory structure like this:

```
training_data/
├── treble_clef/
│   ├── treble_001.png
│   ├── treble_002.png
│   ├── treble_003.png
│   └── ...
├── bass_clef/
│   ├── bass_001.png
│   ├── bass_002.png
│   └── ...
├── quarter_note/
│   ├── quarter_001.png
│   ├── quarter_002.png
│   └── ...
├── eighth_note/
│   └── ...
├── sharp/
│   └── ...
├── flat/
│   └── ...
└── ... (more symbol classes)
```

**Important**: Folder names must match the symbol types you want to recognize.

### Step 3: Create Sample Dataset (For Testing)

To test the training pipeline with placeholder data:

```bash
cd music_recognition/training
python3 dataset.py
```

This creates `sample_training_data/` with placeholder images. **Replace these with real handwritten symbols for actual training!**

---

## Training the Model

### Basic Training Command

```bash
cd ~/GitHub/VS-Code

python3 music_recognition/training/train_model.py \
  --data training_data/ \
  --output models/music_symbol_model.pth \
  --epochs 50 \
  --batch-size 32
```

### Training Parameters:

| Parameter | Description | Default | Recommended |
|-----------|-------------|---------|-------------|
| `--data` | Path to training data directory | Required | `training_data/` |
| `--output` | Path to save trained model | `models/music_symbol_model.pth` | Keep default |
| `--epochs` | Number of training epochs | `50` | 50-100 for real data |
| `--batch-size` | Batch size for training | `32` | 32 (adjust based on RAM) |
| `--lr` | Learning rate | `0.001` | 0.001-0.0001 |
| `--val-split` | Validation split ratio | `0.2` | 0.2 (20% for validation) |
| `--device` | Device to train on | Auto-detect | `cpu` or `cuda` |

### Advanced Training Options:

**Resume from checkpoint:**
```bash
python3 music_recognition/training/train_model.py \
  --data training_data/ \
  --resume models/checkpoint_epoch_20.pth \
  --epochs 100
```

**Adjust learning rate:**
```bash
python3 music_recognition/training/train_model.py \
  --data training_data/ \
  --lr 0.0001 \
  --epochs 100
```

**Use GPU (if available):**
```bash
python3 music_recognition/training/train_model.py \
  --data training_data/ \
  --device cuda \
  --batch-size 64
```

### Training Output

During training, you'll see:

```
======================================================================
Music Symbol Recognition - Model Training
======================================================================

Configuration:
  Data directory: training_data/
  Output model: models/music_symbol_model.pth
  Epochs: 50
  Batch size: 32
  Learning rate: 0.001
  Device: cpu

Loading dataset...
  Training samples: 8000
  Validation samples: 2000
  Number of classes: 18

Initializing model...
  Total parameters: 2,456,789
  Trainable parameters: 2,456,789

======================================================================
Starting training...
======================================================================

Epoch 1/50
----------------------------------------------------------------------
Training: 100%|████████████| 250/250 [01:23<00:00, loss: 2.4531, acc: 34.21%]
Validating: 100%|██████████| 63/63 [00:12<00:00, loss: 2.1234, acc: 42.15%]

Epoch 1 Summary:
  Train Loss: 2.4531 | Train Acc: 34.21%
  Val Loss:   2.1234 | Val Acc:   42.15%
  🎉 New best validation accuracy: 42.15%
  Model saved to: models/music_symbol_model.pth

...

Epoch 50/50
----------------------------------------------------------------------
Training: 100%|████████████| 250/250 [01:20<00:00, loss: 0.0423, acc: 98.75%]
Validating: 100%|██████████| 63/63 [00:11<00:00, loss: 0.1245, acc: 96.32%]

Epoch 50 Summary:
  Train Loss: 0.0423 | Train Acc: 98.75%
  Val Loss:   0.1245 | Val Acc:   96.32%

======================================================================
Training completed!
======================================================================

Best validation accuracy: 96.32%
Model saved to: models/music_symbol_model.pth
Training history saved to: models/training_history.json
```

### What to Look For:

✅ **Good Signs:**
- Validation accuracy increasing over time
- Train/validation accuracy close together (< 5% gap)
- Final validation accuracy > 90%

⚠️ **Warning Signs:**
- Validation accuracy plateaus early (need more data or longer training)
- Large gap between train/val accuracy (overfitting - need more data augmentation)
- Very low accuracy (< 50%) even after many epochs (check data quality)

---

## Evaluating Performance

After training, evaluate your model on test data:

```bash
python3 music_recognition/training/evaluate.py \
  --model models/music_symbol_model.pth \
  --data test_data/ \
  --output-dir evaluation_results/
```

This generates:

1. **Classification Report** (`classification_report.txt`)
   - Per-class precision, recall, F1-score
   - Overall accuracy

2. **Confusion Matrix** (`confusion_matrix.png`)
   - Visual heatmap showing prediction accuracy
   - Identifies which symbols are confused with each other

3. **Per-Class Accuracy** (`per_class_accuracy.png`)
   - Bar chart showing accuracy for each symbol type
   - Highlights worst-performing classes

### Example Output:

```
======================================================================
Model Evaluation
======================================================================

Model: models/music_symbol_model.pth
Test data: test_data/
Device: cpu

Loading model...
Model loaded successfully
Number of classes: 18

Loading test dataset...
Test samples: 2000

Evaluating model...
100%|████████████████████████████████| 63/63 [00:15<00:00]

======================================================================
Overall Accuracy: 94.25%
======================================================================

Classification Report:
----------------------------------------------------------------------
                precision    recall  f1-score   support

   treble_clef       0.97      0.98      0.98       120
     bass_clef       0.96      0.95      0.96       115
   quarter_note       0.94      0.93      0.94       130
    eighth_note       0.92      0.91      0.91       125
         sharp       0.95      0.94      0.95       110
          flat       0.93      0.92      0.93       108
...

Worst performing classes:
----------------------------------------------------------------------
  sixteenth_note: 87.25%
  natural: 89.12%
  dot: 90.45%
  eighth_rest: 91.23%
  beam: 92.10%

Evaluation results saved to: evaluation_results/
```

---

## Using the Trained Model

### Option 1: Update the Server (Automatic)

Once you have a trained model, update the book processor to use it:

1. Place your trained model in `music_recognition/models/`:
   ```bash
   cp models/music_symbol_model.pth music_recognition/models/
   ```

2. Update `music_recognition/book_processor.py` (around line 100):
   ```python
   self.music_recognizer = MusicRecognitionSystem(
       model_path="music_recognition/models/music_symbol_model.pth",
       device='cpu',
       confidence_threshold=0.7
   )
   ```

3. Restart the server:
   ```bash
   python3 web_app/server.py
   ```

Now when you upload handwritten PDFs, the system will use your trained model!

### Option 2: Use Directly in Python

```python
from music_recognition import MusicRecognitionSystem

# Load trained model
recognizer = MusicRecognitionSystem(
    model_path="models/music_symbol_model.pth",
    device='cpu'
)

# Recognize notation from image
score = recognizer.recognize("page_image.png")

# Export to MusicXML
recognizer.export_score(score, "output.musicxml", format='musicxml')

# Export to MIDI
recognizer.export_score(score, "output.mid", format='midi')
```

---

## Tips for Better Accuracy

### 1. **More Training Data**
- Aim for 500+ examples per symbol class
- Include variation: different handwriting styles, pen types, paper textures

### 2. **Balanced Dataset**
- Each class should have similar number of samples
- Underrepresented classes will have lower accuracy

### 3. **High-Quality Images**
- Clear, well-lit scans or photos
- Consistent background (white paper)
- Proper contrast (dark symbols on light background)

### 4. **Data Augmentation** (Already Built-In)
The training script automatically applies:
- Random rotation (±15°)
- Random shear transformations
- Brightness/contrast adjustments
- Gaussian noise
- Translation and scaling

### 5. **Longer Training**
- If validation accuracy still improving, train for more epochs
- Use `--epochs 100` or `--epochs 200`

### 6. **Fine-Tuning**
- Start with pre-trained model
- Train additional epochs on your specific handwriting style

### 7. **Clean Labeling**
- Double-check folder organization
- Remove mislabeled or unclear images
- Ensure one symbol per image (properly cropped)

---

## Troubleshooting

### "No images found in directory"
- Check folder structure matches expected format
- Ensure image files are `.png`, `.jpg`, or `.jpeg`
- Verify folders contain actual image files

### Low Training Accuracy (< 50%)
- Check if images are loading correctly
- Verify labels match folder names
- Ensure enough training data per class (100+ minimum)

### Overfitting (Train >> Val Accuracy)
- Increase validation split: `--val-split 0.3`
- Add more training data
- Train for fewer epochs

### Out of Memory Errors
- Reduce batch size: `--batch-size 16` or `--batch-size 8`
- Use smaller images (default is 64x64, already small)

### Slow Training
- Use GPU if available: `--device cuda`
- Reduce number of workers in dataloader
- Use smaller batch size

---

## Next Steps

1. **Collect Real Training Data**: Replace sample data with actual handwritten music symbols
2. **Train Initial Model**: Start with 50 epochs and see results
3. **Evaluate Performance**: Check which symbols need more training data
4. **Iterate**: Add more data for weak classes, retrain
5. **Integrate**: Update server to use trained model
6. **Test**: Upload real handwritten PDFs and verify recognition quality

**Happy Training! 🎵**

---

## Quick Reference

### Create Sample Dataset
```bash
python3 music_recognition/training/dataset.py
```

### Train Model
```bash
python3 music_recognition/training/train_model.py \
  --data training_data/ \
  --epochs 50 \
  --batch-size 32
```

### Evaluate Model
```bash
python3 music_recognition/training/evaluate.py \
  --model models/music_symbol_model.pth \
  --data test_data/
```

### Test Augmentation
```bash
python3 music_recognition/training/augmentation.py
```
