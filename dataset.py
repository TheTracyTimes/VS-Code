"""
Dataset utilities for loading and preparing music symbol data.
"""

import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from typing import Tuple, Optional, Callable
import albumentations as A
from albumentations.pytorch import ToTensorV2


class MusicSymbolDataset(Dataset):
    """
    Dataset for music symbol classification.

    Expected directory structure:
        data/
            train/
                treble_clef/
                    img1.png
                    img2.png
                quarter_note/
                    img1.png
                    img2.png
                ...
            val/
                treble_clef/
                    img1.png
                ...
    """

    def __init__(
        self,
        data_dir: str,
        split: str = 'train',
        transform: Optional[Callable] = None,
        target_size: Tuple[int, int] = (64, 64)
    ):
        """
        Initialize dataset.

        Args:
            data_dir: Root directory containing train/val splits
            split: 'train' or 'val'
            transform: Optional transforms to apply
            target_size: Target image size (width, height)
        """
        self.data_dir = Path(data_dir) / split
        self.transform = transform
        self.target_size = target_size

        if not self.data_dir.exists():
            raise ValueError(f"Data directory {self.data_dir} does not exist")

        self.classes = sorted([d.name for d in self.data_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}

        self.samples = []
        for class_name in self.classes:
            class_dir = self.data_dir / class_name
            for img_path in class_dir.glob('*.png'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))
            for img_path in class_dir.glob('*.jpg'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))

        print(f"Loaded {len(self.samples)} samples from {len(self.classes)} classes")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Get a sample from the dataset.

        Args:
            idx: Index of the sample

        Returns:
            Tuple of (image tensor, class label)
        """
        img_path, label = self.samples[idx]

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            raise ValueError(f"Could not load image: {img_path}")

        image = cv2.resize(image, self.target_size, interpolation=cv2.INTER_AREA)

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        else:
            image = image.astype(np.float32) / 255.0
            image = torch.from_numpy(image).unsqueeze(0)

        return image, label


def get_training_augmentation(target_size: Tuple[int, int] = (64, 64)):
    """
    Get training data augmentation pipeline.

    Args:
        target_size: Target image size

    Returns:
        Albumentations transform pipeline
    """
    return A.Compose([
        A.Resize(target_size[1], target_size[0]),
        A.OneOf([
            A.GaussNoise(var_limit=(10.0, 50.0), p=1.0),
            A.GaussianBlur(blur_limit=(3, 5), p=1.0),
        ], p=0.3),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.3),
        A.Rotate(limit=15, border_mode=cv2.BORDER_CONSTANT, value=0, p=0.5),
        A.ShiftScaleRotate(
            shift_limit=0.1,
            scale_limit=0.1,
            rotate_limit=0,
            border_mode=cv2.BORDER_CONSTANT,
            value=0,
            p=0.3
        ),
        A.ElasticTransform(
            alpha=1,
            sigma=50,
            alpha_affine=50,
            border_mode=cv2.BORDER_CONSTANT,
            value=0,
            p=0.2
        ),
        A.Normalize(mean=[0.0], std=[1.0]),
        ToTensorV2()
    ])


def get_validation_augmentation(target_size: Tuple[int, int] = (64, 64)):
    """
    Get validation data augmentation pipeline.

    Args:
        target_size: Target image size

    Returns:
        Albumentations transform pipeline
    """
    return A.Compose([
        A.Resize(target_size[1], target_size[0]),
        A.Normalize(mean=[0.0], std=[1.0]),
        ToTensorV2()
    ])


def create_dataloaders(
    data_dir: str,
    batch_size: int = 32,
    num_workers: int = 4,
    target_size: Tuple[int, int] = (64, 64)
) -> Tuple[DataLoader, DataLoader]:
    """
    Create training and validation dataloaders.

    Args:
        data_dir: Root directory containing train/val splits
        batch_size: Batch size for dataloaders
        num_workers: Number of worker processes
        target_size: Target image size

    Returns:
        Tuple of (train_loader, val_loader)
    """
    train_dataset = MusicSymbolDataset(
        data_dir=data_dir,
        split='train',
        transform=get_training_augmentation(target_size),
        target_size=target_size
    )

    val_dataset = MusicSymbolDataset(
        data_dir=data_dir,
        split='val',
        transform=get_validation_augmentation(target_size),
        target_size=target_size
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    return train_loader, val_loader


class SyntheticMusicDataset(Dataset):
    """
    Synthetic dataset generator for testing without real data.
    Generates simple geometric shapes to represent music symbols.
    """

    def __init__(
        self,
        num_samples: int = 1000,
        num_classes: int = 10,
        image_size: Tuple[int, int] = (64, 64)
    ):
        """
        Initialize synthetic dataset.

        Args:
            num_samples: Number of synthetic samples to generate
            num_classes: Number of classes
            image_size: Size of generated images
        """
        self.num_samples = num_samples
        self.num_classes = num_classes
        self.image_size = image_size

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """Generate a synthetic sample."""
        label = idx % self.num_classes

        image = np.zeros(self.image_size, dtype=np.uint8)

        if label % 4 == 0:
            cv2.circle(image, (32, 32), 20, 255, -1)
        elif label % 4 == 1:
            cv2.rectangle(image, (15, 15), (50, 50), 255, -1)
        elif label % 4 == 2:
            pts = np.array([[32, 10], [50, 50], [14, 50]], np.int32)
            cv2.fillPoly(image, [pts], 255)
        else:
            cv2.ellipse(image, (32, 32), (25, 15), 0, 0, 360, 255, -1)

        image = image.astype(np.float32) / 255.0
        image = torch.from_numpy(image).unsqueeze(0)

        return image, label
