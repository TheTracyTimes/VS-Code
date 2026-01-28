"""
Dataset loader for music symbol images.

Expected directory structure:
training_data/
├── treble_clef/
│   ├── img001.png
│   ├── img002.png
│   └── ...
├── bass_clef/
│   ├── img001.png
│   └── ...
├── quarter_note/
│   └── ...
└── ...
"""

import torch
from torch.utils.data import Dataset
from PIL import Image
import os
from pathlib import Path
from typing import Optional, Callable, List, Tuple
import numpy as np


class MusicSymbolDataset(Dataset):
    """Dataset for music symbol images organized by class folders."""

    def __init__(
        self,
        root_dir: str,
        transform: Optional[Callable] = None,
        train: bool = True,
        val_split: float = 0.2,
        seed: int = 42
    ):
        """
        Initialize the dataset.

        Args:
            root_dir: Root directory containing class folders
            transform: Optional transform to apply to images
            train: If True, use training split; if False, use validation split
            val_split: Fraction of data to use for validation
            seed: Random seed for train/val split
        """
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.train = train
        self.val_split = val_split

        # Find all class directories
        self.class_names = sorted([d.name for d in self.root_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.class_names)}
        self.num_classes = len(self.class_names)

        # Load all image paths and labels
        self.samples = []
        for class_name in self.class_names:
            class_dir = self.root_dir / class_name
            class_idx = self.class_to_idx[class_name]

            # Find all image files
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp']:
                for img_path in class_dir.glob(ext):
                    self.samples.append((str(img_path), class_idx))

        if len(self.samples) == 0:
            raise ValueError(f"No images found in {root_dir}. Check directory structure.")

        # Split into train/val
        np.random.seed(seed)
        indices = np.random.permutation(len(self.samples))
        split_idx = int(len(self.samples) * (1 - val_split))

        if train:
            self.samples = [self.samples[i] for i in indices[:split_idx]]
        else:
            self.samples = [self.samples[i] for i in indices[split_idx:]]

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Get a sample from the dataset.

        Returns:
            tuple: (image, label) where image is a tensor and label is an integer
        """
        img_path, label = self.samples[idx]

        # Load image
        image = Image.open(img_path).convert('L')  # Convert to grayscale

        # Apply transforms
        if self.transform:
            image = self.transform(image)
        else:
            # Default: convert to tensor
            image = torch.from_numpy(np.array(image)).float().unsqueeze(0) / 255.0

        return image, label

    def get_class_distribution(self) -> dict:
        """Get the distribution of classes in the dataset."""
        distribution = {cls: 0 for cls in self.class_names}
        for _, label in self.samples:
            class_name = self.class_names[label]
            distribution[class_name] += 1
        return distribution


class SimpleDataset(Dataset):
    """Simple dataset that loads images and labels from lists."""

    def __init__(
        self,
        image_paths: List[str],
        labels: List[int],
        transform: Optional[Callable] = None
    ):
        """
        Initialize dataset with explicit paths and labels.

        Args:
            image_paths: List of paths to image files
            labels: List of integer labels
            transform: Optional transform to apply
        """
        assert len(image_paths) == len(labels), "Paths and labels must have same length"

        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path = self.image_paths[idx]
        label = self.labels[idx]

        # Load image
        image = Image.open(img_path).convert('L')

        # Apply transforms
        if self.transform:
            image = self.transform(image)
        else:
            image = torch.from_numpy(np.array(image)).float().unsqueeze(0) / 255.0

        return image, label


def create_sample_dataset(output_dir: str = "sample_training_data", samples_per_class: int = 10):
    """
    Create a sample dataset structure with placeholder images for testing.

    Args:
        output_dir: Directory to create sample data in
        samples_per_class: Number of sample images per class
    """
    from PIL import ImageDraw

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Symbol classes
    classes = [
        'treble_clef', 'bass_clef', 'alto_clef',
        'whole_note', 'half_note', 'quarter_note', 'eighth_note',
        'whole_rest', 'half_rest', 'quarter_rest', 'eighth_rest',
        'sharp', 'flat', 'natural',
        'time_4_4', 'time_3_4', 'time_2_4',
        'barline'
    ]

    print(f"Creating sample dataset in: {output_dir}")
    print(f"Classes: {len(classes)}")
    print(f"Samples per class: {samples_per_class}")

    for class_name in classes:
        class_dir = output_path / class_name
        class_dir.mkdir(exist_ok=True)

        for i in range(samples_per_class):
            # Create a simple placeholder image
            img = Image.new('L', (64, 64), color=255)
            draw = ImageDraw.Draw(img)

            # Draw something simple (just for placeholder)
            draw.rectangle([10, 10, 54, 54], outline=0, width=2)
            draw.text((20, 25), class_name[:4], fill=0)

            # Save
            img_path = class_dir / f"{class_name}_{i:03d}.png"
            img.save(img_path)

    print(f"✓ Sample dataset created: {output_dir}")
    print(f"  Total images: {len(classes) * samples_per_class}")
    print("\nTo use this dataset:")
    print(f"  python train_model.py --data {output_dir} --epochs 10")


if __name__ == "__main__":
    # Create sample dataset for testing
    create_sample_dataset()
