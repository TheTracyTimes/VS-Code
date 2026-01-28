"""
Data augmentation transforms for music symbol images.
"""

import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random


class RandomRotation:
    """Randomly rotate image by small angle."""

    def __init__(self, degrees=10):
        self.degrees = degrees

    def __call__(self, img):
        angle = random.uniform(-self.degrees, self.degrees)
        return img.rotate(angle, fillcolor=255)


class RandomShear:
    """Apply random shear transformation."""

    def __init__(self, shear=0.2):
        self.shear = shear

    def __call__(self, img):
        shear_factor = random.uniform(-self.shear, self.shear)
        width, height = img.size
        # Apply shear transformation
        return img.transform(
            (width, height),
            Image.AFFINE,
            (1, shear_factor, 0, 0, 1, 0),
            fillcolor=255
        )


class RandomThickness:
    """Randomly vary line thickness."""

    def __init__(self, strength=0.5):
        self.strength = strength

    def __call__(self, img):
        # Convert to numpy
        img_array = np.array(img)

        # Random dilation/erosion
        if random.random() < 0.5:
            # Thicken (dilate)
            kernel_size = random.choice([2, 3])
            img_pil = Image.fromarray(img_array)
            img_pil = img_pil.filter(ImageFilter.MinFilter(kernel_size))
            return img_pil
        else:
            # Thin (erode)
            kernel_size = random.choice([2, 3])
            img_pil = Image.fromarray(img_array)
            img_pil = img_pil.filter(ImageFilter.MaxFilter(kernel_size))
            return img_pil


class AddGaussianNoise:
    """Add Gaussian noise to image."""

    def __init__(self, mean=0, std=0.05):
        self.mean = mean
        self.std = std

    def __call__(self, tensor):
        """Expects a tensor input."""
        noise = torch.randn(tensor.size()) * self.std + self.mean
        return torch.clamp(tensor + noise, 0, 1)


class RandomContrast:
    """Randomly adjust image contrast."""

    def __init__(self, contrast_range=(0.8, 1.2)):
        self.contrast_range = contrast_range

    def __call__(self, img):
        factor = random.uniform(*self.contrast_range)
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)


class RandomBrightness:
    """Randomly adjust image brightness."""

    def __init__(self, brightness_range=(0.9, 1.1)):
        self.brightness_range = brightness_range

    def __call__(self, img):
        factor = random.uniform(*self.brightness_range)
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)


def get_train_transforms(input_size=64):
    """
    Get training augmentation pipeline.

    Args:
        input_size: Size to resize images to

    Returns:
        torchvision.transforms.Compose object
    """
    return transforms.Compose([
        transforms.Resize((input_size, input_size)),
        RandomRotation(degrees=15),  # Slight rotation
        RandomShear(shear=0.15),  # Slight shear
        RandomContrast(contrast_range=(0.7, 1.3)),
        RandomBrightness(brightness_range=(0.8, 1.2)),
        transforms.RandomAffine(
            degrees=0,
            translate=(0.1, 0.1),  # Slight translation
            scale=(0.9, 1.1),  # Slight scaling
            fill=255
        ),
        transforms.ToTensor(),  # Convert to tensor [0, 1]
        AddGaussianNoise(mean=0, std=0.02),  # Add slight noise
        transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize to [-1, 1]
    ])


def get_val_transforms(input_size=64):
    """
    Get validation/test transforms (no augmentation).

    Args:
        input_size: Size to resize images to

    Returns:
        torchvision.transforms.Compose object
    """
    return transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])


def get_inference_transforms(input_size=64):
    """
    Get transforms for inference on real images.

    Args:
        input_size: Size to resize images to

    Returns:
        torchvision.transforms.Compose object
    """
    return transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])


# Test augmentation
if __name__ == "__main__":
    from PIL import Image, ImageDraw
    import matplotlib.pyplot as plt

    # Create a simple test image
    img = Image.new('L', (64, 64), color=255)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 54, 54], outline=0, width=3)
    draw.ellipse([20, 20, 44, 44], fill=0)

    # Apply augmentations
    transform = get_train_transforms()

    # Show original and augmented versions
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')

    for i in range(1, 5):
        aug_tensor = transform(img)
        # Denormalize for display
        aug_img = (aug_tensor[0] * 0.5 + 0.5).numpy()
        axes[0, i].imshow(aug_img, cmap='gray')
        axes[0, i].set_title(f'Augmented {i}')
        axes[0, i].axis('off')

    # Second row
    for i in range(5):
        aug_tensor = transform(img)
        aug_img = (aug_tensor[0] * 0.5 + 0.5).numpy()
        axes[1, i].imshow(aug_img, cmap='gray')
        axes[1, i].set_title(f'Augmented {i+5}')
        axes[1, i].axis('off')

    plt.tight_layout()
    plt.savefig('augmentation_examples.png', dpi=150, bbox_inches='tight')
    print("Augmentation examples saved to: augmentation_examples.png")
