#!/usr/bin/env python3
"""
Training script for music symbol recognition CNN.

Usage:
    python train_model.py --data training_data/ --epochs 50 --batch-size 32
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import argparse
from pathlib import Path
import json
from tqdm import tqdm
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cnn_classifier import MusicSymbolCNN
from training.dataset import MusicSymbolDataset
from training.augmentation import get_train_transforms, get_val_transforms


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(dataloader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)

        # Zero gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass
        loss.backward()
        optimizer.step()

        # Statistics
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        # Update progress bar
        pbar.set_postfix({
            'loss': f'{running_loss/len(pbar):.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })

    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total

    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate the model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        pbar = tqdm(dataloader, desc="Validating")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            pbar.set_postfix({
                'loss': f'{running_loss/len(pbar):.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })

    val_loss = running_loss / len(dataloader)
    val_acc = 100. * correct / total

    return val_loss, val_acc


def main():
    parser = argparse.ArgumentParser(description='Train music symbol recognition model')
    parser.add_argument('--data', type=str, required=True, help='Path to training data directory')
    parser.add_argument('--output', type=str, default='models/music_symbol_model.pth',
                        help='Output path for trained model')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--val-split', type=float, default=0.2, help='Validation split ratio')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to train on (cuda/cpu)')
    parser.add_argument('--resume', type=str, default=None, help='Resume from checkpoint')

    args = parser.parse_args()

    print("=" * 70)
    print("Music Symbol Recognition - Model Training")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Data directory: {args.data}")
    print(f"  Output model: {args.output}")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Device: {args.device}")
    print()

    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load dataset
    print("Loading dataset...")
    train_dataset = MusicSymbolDataset(
        args.data,
        transform=get_train_transforms(),
        train=True,
        val_split=args.val_split
    )

    val_dataset = MusicSymbolDataset(
        args.data,
        transform=get_val_transforms(),
        train=False,
        val_split=args.val_split
    )

    print(f"  Training samples: {len(train_dataset)}")
    print(f"  Validation samples: {len(val_dataset)}")
    print(f"  Number of classes: {train_dataset.num_classes}")
    print(f"  Classes: {train_dataset.class_names}")

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True if args.device == 'cuda' else False
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True if args.device == 'cuda' else False
    )

    # Initialize model
    print("\nInitializing model...")
    model = MusicSymbolCNN(num_classes=train_dataset.num_classes)
    model = model.to(args.device)

    # Print model info
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Total parameters: {total_params:,}")
    print(f"  Trainable parameters: {trainable_params:,}")

    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )

    # Resume from checkpoint if specified
    start_epoch = 0
    best_val_acc = 0.0

    if args.resume:
        print(f"\nResuming from checkpoint: {args.resume}")
        checkpoint = torch.load(args.resume, map_location=args.device)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        best_val_acc = checkpoint.get('best_val_acc', 0.0)
        print(f"  Resuming from epoch {start_epoch}")
        print(f"  Best validation accuracy: {best_val_acc:.2f}%")

    # Training loop
    print("\n" + "=" * 70)
    print("Starting training...")
    print("=" * 70 + "\n")

    training_history = []

    for epoch in range(start_epoch, args.epochs):
        print(f"\nEpoch {epoch+1}/{args.epochs}")
        print("-" * 70)

        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, args.device)

        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, args.device)

        # Learning rate scheduling
        scheduler.step(val_loss)

        # Print epoch summary
        print(f"\nEpoch {epoch+1} Summary:")
        print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")

        # Save history
        training_history.append({
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc,
            'lr': optimizer.param_groups[0]['lr']
        })

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"  🎉 New best validation accuracy: {best_val_acc:.2f}%")

            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'train_acc': train_acc,
                'val_loss': val_loss,
                'val_acc': val_acc,
                'best_val_acc': best_val_acc,
                'class_names': train_dataset.class_names,
                'num_classes': train_dataset.num_classes
            }

            torch.save(checkpoint, args.output)
            print(f"  Model saved to: {args.output}")

        # Save checkpoint every 10 epochs
        if (epoch + 1) % 10 == 0:
            checkpoint_path = output_path.parent / f"checkpoint_epoch_{epoch+1}.pth"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc
            }, checkpoint_path)
            print(f"  Checkpoint saved to: {checkpoint_path}")

    # Save training history
    history_path = output_path.parent / "training_history.json"
    with open(history_path, 'w') as f:
        json.dump(training_history, f, indent=2)

    print("\n" + "=" * 70)
    print("Training completed!")
    print("=" * 70)
    print(f"\nBest validation accuracy: {best_val_acc:.2f}%")
    print(f"Model saved to: {args.output}")
    print(f"Training history saved to: {history_path}")


if __name__ == "__main__":
    main()
