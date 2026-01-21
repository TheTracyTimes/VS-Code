"""
CNN-based classifier for music symbol recognition.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List


class ResidualBlock(nn.Module):
    """Residual block with skip connections."""

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super(ResidualBlock, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class MusicSymbolCNN(nn.Module):
    """
    CNN architecture for classifying handwritten music symbols.

    Supports recognition of various music notation symbols including:
    - Clefs (treble, bass, alto)
    - Note heads (whole, half, quarter, eighth, sixteenth)
    - Rests (whole, half, quarter, eighth, sixteenth)
    - Accidentals (sharp, flat, natural)
    - Time signatures
    - Barlines
    """

    # Symbol classes
    SYMBOL_CLASSES = [
        'treble_clef', 'bass_clef', 'alto_clef',
        'whole_note', 'half_note', 'quarter_note', 'eighth_note', 'sixteenth_note',
        'whole_rest', 'half_rest', 'quarter_rest', 'eighth_rest', 'sixteenth_rest',
        'sharp', 'flat', 'natural',
        'time_2_4', 'time_3_4', 'time_4_4', 'time_6_8',
        'barline', 'double_barline',
        'dot', 'beam', 'stem',
        'background'
    ]

    def __init__(self, num_classes: int = None, input_channels: int = 1, dropout: float = 0.5):
        """
        Initialize the CNN classifier.

        Args:
            num_classes: Number of symbol classes to recognize. Defaults to len(SYMBOL_CLASSES).
            input_channels: Number of input channels (1 for grayscale, 3 for RGB)
            dropout: Dropout probability for regularization
        """
        super(MusicSymbolCNN, self).__init__()

        if num_classes is None:
            num_classes = len(self.SYMBOL_CLASSES)

        self.num_classes = num_classes

        self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(64, 64, num_blocks=2)
        self.layer2 = self._make_layer(64, 128, num_blocks=2, stride=2)
        self.layer3 = self._make_layer(128, 256, num_blocks=2, stride=2)
        self.layer4 = self._make_layer(256, 512, num_blocks=2, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, in_channels: int, out_channels: int, num_blocks: int, stride: int = 1):
        """Create a layer with multiple residual blocks."""
        layers = []
        layers.append(ResidualBlock(in_channels, out_channels, stride))
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch_size, channels, height, width)

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.dropout(x)
        x = self.fc(x)

        return x

    def predict(self, x):
        """
        Make predictions with softmax probabilities.

        Args:
            x: Input tensor

        Returns:
            Tuple of (predicted class indices, probabilities)
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
            predictions = torch.argmax(probs, dim=1)
        return predictions, probs

    @classmethod
    def get_class_name(cls, class_idx: int) -> str:
        """
        Get the name of a class from its index.

        Args:
            class_idx: Index of the class

        Returns:
            Name of the class
        """
        if 0 <= class_idx < len(cls.SYMBOL_CLASSES):
            return cls.SYMBOL_CLASSES[class_idx]
        return "unknown"

    @classmethod
    def get_class_index(cls, class_name: str) -> int:
        """
        Get the index of a class from its name.

        Args:
            class_name: Name of the class

        Returns:
            Index of the class, or -1 if not found
        """
        try:
            return cls.SYMBOL_CLASSES.index(class_name)
        except ValueError:
            return -1


class LightweightMusicCNN(nn.Module):
    """Lightweight CNN for faster inference on resource-constrained devices."""

    def __init__(self, num_classes: int = 26, input_channels: int = 1):
        super(LightweightMusicCNN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
