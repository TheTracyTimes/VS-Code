"""
Evaluation script for the music symbol recognition model.
"""

import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from music_recognition.models import MusicSymbolCNN, LightweightMusicCNN
from dataset import create_dataloaders, SyntheticMusicDataset


class Evaluator:
    """Evaluator for music symbol recognition models."""

    def __init__(self, model: nn.Module, test_loader: DataLoader, device: str = 'cpu'):
        """
        Initialize evaluator.

        Args:
            model: Trained PyTorch model
            test_loader: Test data loader
            device: Device to run evaluation on
        """
        self.model = model.to(device)
        self.test_loader = test_loader
        self.device = device
        self.model.eval()

    def evaluate(self) -> dict:
        """
        Evaluate the model on test set.

        Returns:
            Dictionary containing evaluation metrics
        """
        all_predictions = []
        all_labels = []
        all_probs = []

        criterion = nn.CrossEntropyLoss()
        total_loss = 0

        print("Evaluating model...")
        with torch.no_grad():
            for images, labels in tqdm(self.test_loader):
                images = images.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(images)
                loss = criterion(outputs, labels)
                total_loss += loss.item()

                probs = torch.softmax(outputs, dim=1)
                _, predictions = outputs.max(1)

                all_predictions.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())

        all_predictions = np.array(all_predictions)
        all_labels = np.array(all_labels)
        all_probs = np.array(all_probs)

        avg_loss = total_loss / len(self.test_loader)
        accuracy = 100. * np.sum(all_predictions == all_labels) / len(all_labels)

        results = {
            'loss': avg_loss,
            'accuracy': accuracy,
            'predictions': all_predictions,
            'labels': all_labels,
            'probabilities': all_probs
        }

        return results

    def print_classification_report(self, results: dict, class_names: list = None):
        """
        Print detailed classification report.

        Args:
            results: Results dictionary from evaluate()
            class_names: List of class names
        """
        if class_names is None:
            class_names = [str(i) for i in range(len(np.unique(results['labels'])))]

        print("\n" + "="*60)
        print("Classification Report")
        print("="*60)
        print(f"\nOverall Accuracy: {results['accuracy']:.2f}%")
        print(f"Average Loss: {results['loss']:.4f}\n")

        report = classification_report(
            results['labels'],
            results['predictions'],
            target_names=class_names,
            digits=3
        )
        print(report)

    def plot_confusion_matrix(self, results: dict, class_names: list = None, save_path: str = None):
        """
        Plot confusion matrix.

        Args:
            results: Results dictionary from evaluate()
            class_names: List of class names
            save_path: Optional path to save the plot
        """
        cm = confusion_matrix(results['labels'], results['predictions'])

        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=class_names if class_names else 'auto',
            yticklabels=class_names if class_names else 'auto'
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Confusion matrix saved to {save_path}")
        else:
            plt.show()

    def analyze_errors(self, results: dict, class_names: list = None, top_k: int = 10):
        """
        Analyze common errors.

        Args:
            results: Results dictionary from evaluate()
            class_names: List of class names
            top_k: Number of top errors to display
        """
        predictions = results['predictions']
        labels = results['labels']

        errors = predictions != labels
        error_indices = np.where(errors)[0]

        if len(error_indices) == 0:
            print("No errors found! Perfect classification.")
            return

        error_pairs = {}
        for idx in error_indices:
            true_label = labels[idx]
            pred_label = predictions[idx]
            pair = (true_label, pred_label)
            error_pairs[pair] = error_pairs.get(pair, 0) + 1

        sorted_errors = sorted(error_pairs.items(), key=lambda x: x[1], reverse=True)

        print("\n" + "="*60)
        print(f"Top {top_k} Most Common Errors")
        print("="*60)

        for i, ((true_label, pred_label), count) in enumerate(sorted_errors[:top_k], 1):
            true_name = class_names[true_label] if class_names else str(true_label)
            pred_name = class_names[pred_label] if class_names else str(pred_label)
            print(f"{i}. {true_name} → {pred_name}: {count} times")


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description='Evaluate music symbol recognition model')
    parser.add_argument('--model_path', type=str, required=True,
                        help='Path to trained model checkpoint')
    parser.add_argument('--data_path', type=str, default='./data',
                        help='Path to dataset directory')
    parser.add_argument('--synthetic', action='store_true',
                        help='Use synthetic data for testing')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size for evaluation')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to use for evaluation')
    parser.add_argument('--model_type', type=str, default='standard',
                        choices=['standard', 'lightweight'],
                        help='Model architecture used')
    parser.add_argument('--save_cm', type=str, default=None,
                        help='Path to save confusion matrix plot')

    args = parser.parse_args()

    print("="*60)
    print("Music Symbol Recognition - Evaluation")
    print("="*60)

    if args.synthetic:
        print("\nUsing synthetic dataset for testing")
        test_dataset = SyntheticMusicDataset(num_samples=200, num_classes=26)
        test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
        num_classes = 26
        class_names = [f"class_{i}" for i in range(num_classes)]
    else:
        print(f"\nLoading dataset from: {args.data_path}")
        _, test_loader = create_dataloaders(
            data_dir=args.data_path,
            batch_size=args.batch_size,
            num_workers=4
        )
        num_classes = len(test_loader.dataset.classes)
        class_names = test_loader.dataset.classes

    if args.model_type == 'lightweight':
        print(f"\nLoading Lightweight CNN model with {num_classes} classes")
        model = LightweightMusicCNN(num_classes=num_classes)
    else:
        print(f"\nLoading standard CNN model with {num_classes} classes")
        model = MusicSymbolCNN(num_classes=num_classes)

    print(f"Loading checkpoint from: {args.model_path}")
    checkpoint = torch.load(args.model_path, map_location=args.device)

    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)

    evaluator = Evaluator(model, test_loader, device=args.device)

    results = evaluator.evaluate()

    evaluator.print_classification_report(results, class_names)
    evaluator.analyze_errors(results, class_names, top_k=10)

    if args.save_cm:
        evaluator.plot_confusion_matrix(results, class_names, save_path=args.save_cm)


if __name__ == '__main__':
    main()
