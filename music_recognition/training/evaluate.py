#!/usr/bin/env python3
"""
Evaluate a trained music symbol recognition model.

Usage:
    python evaluate.py --model models/music_symbol_model.pth --data test_data/
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
import sys
import os
from pathlib import Path
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cnn_classifier import MusicSymbolCNN
from training.dataset import MusicSymbolDataset
from training.augmentation import get_val_transforms


def evaluate_model(model, dataloader, device, class_names):
    """Evaluate model and return predictions and labels."""
    model.eval()

    all_predictions = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        pbar = tqdm(dataloader, desc="Evaluating")
        for images, labels in pbar:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)

            _, predicted = outputs.max(1)

            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    return np.array(all_predictions), np.array(all_labels), np.array(all_probs)


def plot_confusion_matrix(y_true, y_pred, class_names, output_path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)

    # Normalize
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Accuracy'}
    )
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix (Normalized)')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Confusion matrix saved to: {output_path}")


def plot_per_class_accuracy(y_true, y_pred, class_names, output_path):
    """Plot per-class accuracy bar chart."""
    cm = confusion_matrix(y_true, y_pred)
    per_class_acc = cm.diagonal() / cm.sum(axis=1)

    # Sort by accuracy
    sorted_indices = np.argsort(per_class_acc)
    sorted_classes = [class_names[i] for i in sorted_indices]
    sorted_acc = per_class_acc[sorted_indices]

    # Plot
    plt.figure(figsize=(12, 8))
    colors = ['red' if acc < 0.7 else 'orange' if acc < 0.9 else 'green' for acc in sorted_acc]
    plt.barh(range(len(sorted_classes)), sorted_acc * 100, color=colors)
    plt.yticks(range(len(sorted_classes)), sorted_classes)
    plt.xlabel('Accuracy (%)')
    plt.title('Per-Class Accuracy')
    plt.axvline(x=70, color='red', linestyle='--', label='70% threshold')
    plt.axvline(x=90, color='orange', linestyle='--', label='90% threshold')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Per-class accuracy plot saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained model')
    parser.add_argument('--model', type=str, required=True, help='Path to trained model')
    parser.add_argument('--data', type=str, required=True, help='Path to test data')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--output-dir', type=str, default='evaluation_results',
                        help='Output directory for results')

    args = parser.parse_args()

    print("=" * 70)
    print("Model Evaluation")
    print("=" * 70)
    print(f"\nModel: {args.model}")
    print(f"Test data: {args.data}")
    print(f"Device: {args.device}\n")

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load checkpoint
    print("Loading model...")
    checkpoint = torch.load(args.model, map_location=args.device)

    class_names = checkpoint.get('class_names', None)
    num_classes = checkpoint.get('num_classes', len(MusicSymbolCNN.SYMBOL_CLASSES))

    # Initialize model
    model = MusicSymbolCNN(num_classes=num_classes)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(args.device)
    model.eval()

    print(f"Model loaded successfully")
    print(f"Number of classes: {num_classes}")

    # Load test dataset
    print("\nLoading test dataset...")
    test_dataset = MusicSymbolDataset(
        args.data,
        transform=get_val_transforms(),
        train=False,
        val_split=0.0  # Use all data for testing
    )

    if class_names is None:
        class_names = test_dataset.class_names

    print(f"Test samples: {len(test_dataset)}")

    test_loader = DataLoader(
        test_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=4
    )

    # Evaluate
    print("\nEvaluating model...")
    predictions, labels, probs = evaluate_model(model, test_loader, args.device, class_names)

    # Calculate overall accuracy
    accuracy = (predictions == labels).mean() * 100
    print(f"\n{'=' * 70}")
    print(f"Overall Accuracy: {accuracy:.2f}%")
    print(f"{'=' * 70}\n")

    # Print classification report
    print("Classification Report:")
    print("-" * 70)
    report = classification_report(labels, predictions, target_names=class_names)
    print(report)

    # Save report
    report_path = output_dir / "classification_report.txt"
    with open(report_path, 'w') as f:
        f.write(f"Overall Accuracy: {accuracy:.2f}%\n\n")
        f.write(report)
    print(f"Classification report saved to: {report_path}")

    # Plot confusion matrix
    cm_path = output_dir / "confusion_matrix.png"
    plot_confusion_matrix(labels, predictions, class_names, cm_path)

    # Plot per-class accuracy
    acc_path = output_dir / "per_class_accuracy.png"
    plot_per_class_accuracy(labels, predictions, class_names, acc_path)

    # Find worst performing classes
    cm = confusion_matrix(labels, predictions)
    per_class_acc = cm.diagonal() / cm.sum(axis=1)
    worst_indices = np.argsort(per_class_acc)[:5]

    print("\nWorst performing classes:")
    print("-" * 70)
    for idx in worst_indices:
        print(f"  {class_names[idx]}: {per_class_acc[idx]*100:.2f}%")

    print(f"\nEvaluation results saved to: {output_dir}")


if __name__ == "__main__":
    main()
