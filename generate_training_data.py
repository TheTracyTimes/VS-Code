#!/usr/bin/env python3
"""
Generate realistic handwritten-style music notation training data.

Creates synthetic training images with variations to simulate handwriting:
- Random rotation and skew
- Variable line thickness
- Position jitter
- Noise and imperfections
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from pathlib import Path
import math


class MusicSymbolGenerator:
    """Generate synthetic handwritten music symbols."""

    def __init__(self, image_size=64):
        self.image_size = image_size
        self.center = image_size // 2

    def add_handwriting_variations(self, img):
        """Add variations to simulate handwriting."""
        # Random rotation (-15 to 15 degrees)
        angle = random.uniform(-15, 15)
        img = img.rotate(angle, fillcolor=255, expand=False)

        # Random slight scale
        scale = random.uniform(0.85, 1.15)
        new_size = int(self.image_size * scale)
        img = img.resize((new_size, new_size), Image.Resampling.LANCZOS)

        # Crop or pad back to original size
        if new_size > self.image_size:
            left = (new_size - self.image_size) // 2
            img = img.crop((left, left, left + self.image_size, left + self.image_size))
        else:
            new_img = Image.new('L', (self.image_size, self.image_size), 255)
            paste_pos = (self.image_size - new_size) // 2
            new_img.paste(img, (paste_pos, paste_pos))
            img = new_img

        # Random translation
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        img = Image.fromarray(np.roll(np.roll(np.array(img), offset_x, axis=1), offset_y, axis=0))

        # Add slight blur to simulate pen thickness variation
        if random.random() > 0.5:
            img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 0.8)))

        # Add noise
        arr = np.array(img).astype(float)
        noise = np.random.normal(0, 3, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)

        return Image.fromarray(arr)

    def draw_treble_clef(self):
        """Draw a treble (G) clef."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Treble clef shape (simplified)
        # Start with the curl at top
        x, y = self.center + 2, 15

        # Main spiral
        points = []
        for t in np.linspace(0, 2*np.pi, 20):
            r = 8 + t * 2
            px = x + r * np.cos(t)
            py = y + r * np.sin(t)
            points.append((px, py))

        # Draw spiral
        if len(points) > 1:
            draw.line(points, fill=0, width=2)

        # Vertical stem
        draw.line([(self.center + 2, 15), (self.center + 2, 50)], fill=0, width=2)

        # Bottom curl
        draw.ellipse([self.center - 8, 45, self.center + 12, 58], outline=0, width=2)

        # Cross line (on 4th line of staff)
        draw.ellipse([self.center - 10, 30, self.center + 14, 38], outline=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_bass_clef(self):
        """Draw a bass (F) clef."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Bass clef shape
        # Large C-curve
        draw.arc([15, 20, 40, 45], 270, 90, fill=0, width=3)

        # Two dots (on F line and above)
        draw.ellipse([42, 25, 47, 30], fill=0)
        draw.ellipse([42, 35, 47, 40], fill=0)

        return self.add_handwriting_variations(img)

    def draw_alto_clef(self):
        """Draw an alto (C) clef."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Alto clef shape (simplified)
        # Two vertical lines
        draw.rectangle([25, 15, 28, 50], fill=0)
        draw.rectangle([30, 15, 33, 50], fill=0)

        # C curves on both sides
        draw.arc([15, 25, 25, 40], 270, 90, fill=0, width=2)
        draw.arc([33, 25, 43, 40], 90, 270, fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_note_head(self, filled=True):
        """Draw a note head (oval)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Oval note head, tilted
        x, y = self.center - 8, self.center - 5
        w, h = 16, 11

        # Create tilted oval
        temp_img = Image.new('L', (self.image_size, self.image_size), 255)
        temp_draw = ImageDraw.Draw(temp_img)

        if filled:
            temp_draw.ellipse([x, y, x+w, y+h], fill=0)
        else:
            temp_draw.ellipse([x, y, x+w, y+h], outline=0, width=2)

        # Rotate slightly for tilt
        img = temp_img.rotate(20, center=(self.center, self.center), fillcolor=255)

        return self.add_handwriting_variations(img)

    def draw_quarter_note(self):
        """Draw a quarter note."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Note head (filled oval, tilted)
        x, y = self.center - 6, self.center + 5
        w, h = 12, 9

        # Tilted ellipse for note head
        temp_img = Image.new('L', (self.image_size, self.image_size), 255)
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.ellipse([x, y, x+w, y+h], fill=0)
        rotated = temp_img.rotate(25, center=(self.center, self.center + 8), fillcolor=255)
        img.paste(rotated, (0, 0), rotated)

        # Stem going up
        stem_x = self.center + 6
        draw.line([(stem_x, self.center + 5), (stem_x, self.center - 20)], fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_half_note(self):
        """Draw a half note."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Note head (hollow oval)
        x, y = self.center - 6, self.center + 5
        w, h = 12, 9

        temp_img = Image.new('L', (self.image_size, self.image_size), 255)
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.ellipse([x, y, x+w, y+h], outline=0, width=2)
        rotated = temp_img.rotate(25, center=(self.center, self.center + 8), fillcolor=255)
        img.paste(rotated, (0, 0), rotated)

        # Stem
        stem_x = self.center + 6
        draw.line([(stem_x, self.center + 5), (stem_x, self.center - 20)], fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_whole_note(self):
        """Draw a whole note."""
        return self.draw_note_head(filled=False)

    def draw_eighth_note(self):
        """Draw an eighth note."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Note head (filled)
        x, y = self.center - 6, self.center + 8
        w, h = 12, 9

        temp_img = Image.new('L', (self.image_size, self.image_size), 255)
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.ellipse([x, y, x+w, y+h], fill=0)
        rotated = temp_img.rotate(25, center=(self.center, self.center + 10), fillcolor=255)
        img.paste(rotated, (0, 0), rotated)

        # Stem
        stem_x = self.center + 6
        draw.line([(stem_x, self.center + 8), (stem_x, self.center - 18)], fill=0, width=2)

        # Flag
        flag_points = [
            (stem_x, self.center - 18),
            (stem_x + 8, self.center - 12),
            (stem_x + 5, self.center - 8),
            (stem_x, self.center - 10)
        ]
        draw.polygon(flag_points, fill=0)

        return self.add_handwriting_variations(img)

    def draw_whole_rest(self):
        """Draw a whole rest (hangs from line)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Rectangle hanging from middle
        draw.rectangle([self.center - 8, self.center - 3, self.center + 8, self.center + 3], fill=0)

        return self.add_handwriting_variations(img)

    def draw_half_rest(self):
        """Draw a half rest (sits on line)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Rectangle sitting on middle
        draw.rectangle([self.center - 8, self.center - 2, self.center + 8, self.center + 4], fill=0)

        return self.add_handwriting_variations(img)

    def draw_quarter_rest(self):
        """Draw a quarter rest."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Stylized Z shape with curves
        points = [
            (self.center - 5, self.center - 12),
            (self.center + 5, self.center - 8),
            (self.center - 3, self.center),
            (self.center + 7, self.center + 12)
        ]

        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=0, width=3)

        # Add blob at top
        draw.ellipse([self.center - 7, self.center - 15, self.center - 2, self.center - 10], fill=0)

        return self.add_handwriting_variations(img)

    def draw_eighth_rest(self):
        """Draw an eighth rest."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Hook shape
        draw.arc([self.center - 5, self.center - 8, self.center + 5, self.center + 2], 180, 360, fill=0, width=2)
        draw.ellipse([self.center - 3, self.center - 2, self.center + 3, self.center + 4], fill=0)

        return self.add_handwriting_variations(img)

    def draw_sharp(self):
        """Draw a sharp (#)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Two vertical lines
        draw.line([(self.center - 6, 18), (self.center - 6, 46)], fill=0, width=2)
        draw.line([(self.center + 6, 18), (self.center + 6, 46)], fill=0, width=2)

        # Two horizontal lines (slanted)
        draw.line([(self.center - 10, 25), (self.center + 10, 22)], fill=0, width=2)
        draw.line([(self.center - 10, 38), (self.center + 10, 35)], fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_flat(self):
        """Draw a flat (♭)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Vertical line
        draw.line([(self.center - 5, 10), (self.center - 5, 50)], fill=0, width=2)

        # Curved part (half circle on right)
        draw.arc([self.center - 5, 32, self.center + 10, 48], 270, 90, fill=0, width=2)
        draw.line([(self.center - 5, 40), (self.center + 5, 44)], fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_natural(self):
        """Draw a natural (♮)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Two vertical lines
        draw.line([(self.center - 5, 15), (self.center - 5, 42)], fill=0, width=2)
        draw.line([(self.center + 5, 22), (self.center + 5, 49)], fill=0, width=2)

        # Two horizontal connectors (slanted)
        draw.line([(self.center - 5, 25), (self.center + 5, 27)], fill=0, width=2)
        draw.line([(self.center - 5, 37), (self.center + 5, 39)], fill=0, width=2)

        return self.add_handwriting_variations(img)

    def draw_time_signature(self, top, bottom):
        """Draw a time signature (e.g., 4/4)."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Draw numbers (simple representation)
        # Top number
        self._draw_number(draw, top, self.center, self.center - 10)

        # Bottom number
        self._draw_number(draw, bottom, self.center, self.center + 10)

        return self.add_handwriting_variations(img)

    def _draw_number(self, draw, num, x, y):
        """Draw a simple number."""
        # Simplified number drawing
        if num == 2:
            points = [(x-6, y-6), (x+6, y-6), (x+6, y), (x-6, y+6), (x+6, y+6)]
            draw.line(points, fill=0, width=2)
        elif num == 3:
            draw.arc([x-6, y-6, x+6, y], 270, 90, fill=0, width=2)
            draw.arc([x-6, y, x+6, y+6], 270, 90, fill=0, width=2)
        elif num == 4:
            draw.line([(x-4, y-6), (x-4, y), (x+4, y), (x+4, y-6), (x+4, y+6)], fill=0, width=2)
        elif num == 6:
            draw.arc([x-6, y-6, x+6, y+6], 0, 360, fill=0, width=2)
            draw.line([(x-2, y-6), (x-2, y)], fill=0, width=2)
        elif num == 8:
            draw.ellipse([x-5, y-8, x+5, y-1], outline=0, width=2)
            draw.ellipse([x-5, y+1, x+5, y+8], outline=0, width=2)

    def draw_barline(self):
        """Draw a barline."""
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)

        # Single vertical line
        draw.line([(self.center, 15), (self.center, 49)], fill=0, width=2)

        return self.add_handwriting_variations(img)


def generate_dataset(output_dir="training_data", samples_per_class=500):
    """
    Generate a complete training dataset with realistic music symbols.

    Args:
        output_dir: Directory to save images
        samples_per_class: Number of images to generate per symbol class
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generator = MusicSymbolGenerator()

    # Define all symbol classes and their generation functions
    symbols = {
        'treble_clef': generator.draw_treble_clef,
        'bass_clef': generator.draw_bass_clef,
        'alto_clef': generator.draw_alto_clef,
        'whole_note': generator.draw_whole_note,
        'half_note': generator.draw_half_note,
        'quarter_note': generator.draw_quarter_note,
        'eighth_note': generator.draw_eighth_note,
        'whole_rest': generator.draw_whole_rest,
        'half_rest': generator.draw_half_rest,
        'quarter_rest': generator.draw_quarter_rest,
        'eighth_rest': generator.draw_eighth_rest,
        'sharp': generator.draw_sharp,
        'flat': generator.draw_flat,
        'natural': generator.draw_natural,
        'time_4_4': lambda: generator.draw_time_signature(4, 4),
        'time_3_4': lambda: generator.draw_time_signature(3, 4),
        'time_2_4': lambda: generator.draw_time_signature(2, 4),
        'time_6_8': lambda: generator.draw_time_signature(6, 8),
        'barline': generator.draw_barline,
    }

    print(f"Generating training dataset...")
    print(f"Output directory: {output_dir}")
    print(f"Symbol classes: {len(symbols)}")
    print(f"Samples per class: {samples_per_class}")
    print(f"Total images: {len(symbols) * samples_per_class}")
    print()

    total_generated = 0

    for class_name, draw_func in symbols.items():
        class_dir = output_path / class_name
        class_dir.mkdir(exist_ok=True)

        print(f"Generating {class_name}...", end=" ", flush=True)

        for i in range(samples_per_class):
            img = draw_func()
            img_path = class_dir / f"{class_name}_{i:04d}.png"
            img.save(img_path)
            total_generated += 1

            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"{i+1}", end=" ", flush=True)

        print(f"✓ ({samples_per_class} images)")

    print()
    print(f"✓ Dataset generation complete!")
    print(f"  Total images generated: {total_generated}")
    print(f"  Location: {output_dir}/")
    print()
    print("Next steps:")
    print(f"  1. Review samples: ls {output_dir}/quarter_note/")
    print(f"  2. Train model: python music_recognition/training/train_model.py --data {output_dir} --epochs 50")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate music symbol training data")
    parser.add_argument("--output", default="training_data", help="Output directory")
    parser.add_argument("--samples", type=int, default=500, help="Samples per class")
    parser.add_argument("--preview", action="store_true", help="Generate only 5 samples per class for preview")

    args = parser.parse_args()

    if args.preview:
        print("Preview mode: generating 5 samples per class")
        generate_dataset(args.output, samples_per_class=5)
    else:
        generate_dataset(args.output, samples_per_class=args.samples)
