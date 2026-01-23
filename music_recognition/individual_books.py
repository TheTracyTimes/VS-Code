"""
Individual part book generation for creating separate books for each instrument.

This module handles:
1. Splitting combined parts into individual books
2. Exporting each instrument as a standalone PDF part book
3. Formatting titles cleanly in Times New Roman
4. Creating professional individual part books from combined sheets
"""

from typing import Dict, List, Tuple, Optional
from pathlib import Path
from .multipart_score import MultiPartScore
from .postprocessing import MusicScore
from .instruments import InstrumentConfig, BandInstruments
from .title_extraction import PartSplitter, TitleExtractor
from .pdf_export import export_score_to_pdf
import os


class IndividualBookGenerator:
    """Generates individual part books from combined or multi-instrument scores."""

    def __init__(self):
        """Initialize individual book generator."""
        self.title_extractor = TitleExtractor()

    def split_combined_parts(self, multipart_score: MultiPartScore,
                            split_combined: bool = True) -> Dict[str, Tuple[MusicScore, InstrumentConfig]]:
        """
        Process combined parts in a MultiPartScore - either split them or keep them together.

        Args:
            multipart_score: MultiPartScore with potentially combined parts
            split_combined: If True, split combined parts into individual books.
                          If False, keep combined parts together in one book.

        Returns:
            Dictionary of part name to (score, instrument) tuples

        Example (split_combined=True):
            Input part: "Bb Clarinet/Trumpet 1/Soprano Sax"
            Output: 3 separate parts:
                - "1st Bb Clarinet"
                - "1st Bb Trumpet"
                - "Bb Soprano Sax"

        Example (split_combined=False):
            Input part: "Bb Clarinet/Trumpet 1/Soprano Sax"
            Output: 1 combined part:
                - "Bb Clarinet/Trumpet 1/Soprano Sax" (kept together)
        """
        individual_parts = {}

        for part_name, (score, instrument) in multipart_score.parts.items():
            # Check if this is a combined part (contains '/')
            if '/' in part_name and split_combined:
                # Split into individual parts
                sub_parts = self._split_part(part_name, score, instrument)
                individual_parts.update(sub_parts)
            else:
                # Keep as-is (either already individual, or user wants combined)
                individual_parts[part_name] = (score, instrument)

        return individual_parts

    def _split_part(self, combined_name: str, score: MusicScore,
                   original_instrument: InstrumentConfig) -> Dict[str, Tuple[MusicScore, InstrumentConfig]]:
        """
        Split a combined part name into individual instruments.

        Args:
            combined_name: Combined part name (e.g., "Bb Clarinet/Trumpet 1/Soprano Sax")
            score: MusicScore for this part
            original_instrument: Original instrument config

        Returns:
            Dictionary of individual parts
        """
        # Parse individual names
        individual_names = PartSplitter.parse_combined_part_name(combined_name)

        individual_parts = {}

        for name in individual_names:
            # Map to appropriate instrument
            instrument = self._map_to_instrument(name, original_instrument)

            if instrument:
                # Create copy of score
                score_copy = self._copy_score(score)
                individual_parts[name] = (score_copy, instrument)

        return individual_parts

    def _map_to_instrument(self, part_name: str, fallback_instrument: InstrumentConfig) -> InstrumentConfig:
        """
        Map a part name to its instrument configuration.

        Args:
            part_name: Part name (e.g., "1st Bb Clarinet")
            fallback_instrument: Fallback instrument if mapping fails

        Returns:
            InstrumentConfig for the part
        """
        name_lower = part_name.lower()

        # Check for specific instruments
        if 'soprano sax' in name_lower:
            return BandInstruments.Bb_SOPRANO_SAX
        elif 'alto sax' in name_lower:
            if '1' in part_name or '1st' in name_lower or 'first' in name_lower:
                return BandInstruments.Eb_ALTO_SAX_1
            elif '2' in part_name or '2nd' in name_lower or 'second' in name_lower:
                return BandInstruments.Eb_ALTO_SAX_2
            elif '3' in part_name or '3rd' in name_lower or 'third' in name_lower:
                return BandInstruments.Eb_ALTO_SAX_3
            else:
                return BandInstruments.Eb_ALTO_SAX_1
        elif 'tenor sax' in name_lower:
            return BandInstruments.Bb_TENOR_SAX
        elif 'bari' in name_lower and 'sax' in name_lower:
            return BandInstruments.Eb_BARITONE_SAX
        elif 'clarinet' in name_lower and 'bass' not in name_lower and 'alto' not in name_lower:
            if '1' in part_name or '1st' in name_lower or 'first' in name_lower:
                return BandInstruments.Bb_CLARINET_1
            elif '2' in part_name or '2nd' in name_lower or 'second' in name_lower:
                return BandInstruments.Bb_CLARINET_2
            elif '3' in part_name or '3rd' in name_lower or 'third' in name_lower:
                return BandInstruments.Bb_CLARINET_3
            else:
                return BandInstruments.Bb_CLARINET_1
        elif 'bass clarinet' in name_lower:
            return BandInstruments.Bb_BASS_CLARINET
        elif 'alto clarinet' in name_lower:
            return BandInstruments.Eb_ALTO_CLARINET
        elif 'trumpet' in name_lower:
            if '1' in part_name or '1st' in name_lower or 'first' in name_lower:
                return BandInstruments.Bb_TRUMPET_1
            elif '2' in part_name or '2nd' in name_lower or 'second' in name_lower:
                return BandInstruments.Bb_TRUMPET_2
            elif '3' in part_name or '3rd' in name_lower or 'third' in name_lower:
                return BandInstruments.Bb_TRUMPET_3
            else:
                return BandInstruments.Bb_TRUMPET_1
        elif 'trombone' in name_lower:
            if '1' in part_name or '1st' in name_lower or 'first' in name_lower:
                return BandInstruments.C_TROMBONE_1
            elif '2' in part_name or '2nd' in name_lower or 'second' in name_lower:
                return BandInstruments.C_TROMBONE_2
            elif '3' in part_name or '3rd' in name_lower or 'third' in name_lower:
                return BandInstruments.C_TROMBONE_3
            else:
                return BandInstruments.C_TROMBONE_1
        elif 'baritone' in name_lower and ('t.c.' in name_lower or 'treble' in name_lower):
            return BandInstruments.Bb_BARITONE_TC
        elif 'baritone' in name_lower or 'euphonium' in name_lower:
            return BandInstruments.C_EUPHONIUM_BC
        elif 'horn' in name_lower:
            if '1' in part_name or '1st' in name_lower:
                return BandInstruments.F_FRENCH_HORN_1
            elif '2' in part_name or '2nd' in name_lower:
                return BandInstruments.F_FRENCH_HORN_2
            else:
                return BandInstruments.F_FRENCH_HORN_1
        elif 'flute' in name_lower:
            if '2' in part_name or '2nd' in name_lower:
                return BandInstruments.C_FLUTE_2
            elif '3' in part_name or '3rd' in name_lower:
                return BandInstruments.C_FLUTE_3
            else:
                return BandInstruments.C_FLUTE
        elif 'tuba' in name_lower:
            return BandInstruments.C_TUBA

        # Fallback to original instrument
        return fallback_instrument

    def _copy_score(self, score: MusicScore) -> MusicScore:
        """Create a deep copy of a MusicScore."""
        new_score = MusicScore()
        new_score.time_signature = score.time_signature
        new_score.key_signature = score.key_signature
        new_score.clef = score.clef
        new_score.tempo = score.tempo

        # Deep copy measures
        for measure in score.measures:
            new_measure = [note.copy() for note in measure]
            new_score.measures.append(new_measure)

        return new_score

    def export_individual_books(self, multipart_score: MultiPartScore,
                               output_dir: str,
                               clean_titles: bool = True,
                               split_combined: bool = True) -> Dict[str, str]:
        """
        Export each instrument as a separate PDF book.

        Args:
            multipart_score: MultiPartScore containing all parts
            output_dir: Directory to save individual books
            clean_titles: Whether to clean titles (remove staff lines)
            split_combined: If True, split combined parts (e.g., "Clarinet/Trumpet") into separate books.
                          If False, keep combined parts together in one book.

        Returns:
            Dictionary mapping part names to PDF file paths

        Example (split_combined=True):
            From input "Bb Clarinet/Trumpet 1/Soprano Sax", creates:
            - output_dir/1st_Bb_Clarinet.pdf
            - output_dir/1st_Bb_Trumpet.pdf
            - output_dir/Bb_Soprano_Sax.pdf

        Example (split_combined=False):
            From input "Bb Clarinet/Trumpet 1/Soprano Sax", creates:
            - output_dir/Bb_Clarinet_Trumpet_1_Soprano_Sax.pdf (all three together)
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Process combined parts (split or keep together based on parameter)
        individual_parts = self.split_combined_parts(multipart_score, split_combined=split_combined)

        # Export each part as separate PDF
        exported_files = {}

        for part_name, (score, instrument) in individual_parts.items():
            # Create safe filename
            safe_name = part_name.replace('/', '_').replace(' ', '_').replace('♭', 'b').replace('♯', '#')
            output_path = os.path.join(output_dir, f"{safe_name}.pdf")

            # Create a single-part score for export
            single_part_score = MultiPartScore(title=part_name)
            single_part_score.add_part(part_name, score, instrument)

            # Export to PDF
            export_score_to_pdf(single_part_score, output_path)

            exported_files[part_name] = output_path
            print(f"  ✓ Created: {safe_name}.pdf")

        return exported_files


def create_individual_books_from_score(multipart_score: MultiPartScore,
                                       output_dir: str = 'output/individual_books',
                                       split_combined: bool = True) -> Dict[str, str]:
    """
    Create individual part books from a MultiPartScore.

    This is the main function to use for creating separate books.

    Args:
        multipart_score: MultiPartScore containing all parts (may have combined parts)
        output_dir: Directory to save individual books
        split_combined: If True (default), split combined parts like "Bb Clarinet/Trumpet 1/Soprano Sax"
                       into 3 separate books. If False, keep them together in 1 combined book.

    Returns:
        Dictionary mapping part names to PDF file paths

    Example (split_combined=True - default):
        >>> score = MultiPartScore(title="Band Arrangement")
        >>> # ... add parts including combined parts like "Bb Clarinet/Trumpet 1/Soprano Sax" ...
        >>> books = create_individual_books_from_score(score, split_combined=True)
        >>> # Results in 3 separate PDFs:
        >>> #   - 1st_Bb_Clarinet.pdf
        >>> #   - 1st_Bb_Trumpet.pdf
        >>> #   - Bb_Soprano_Sax.pdf

    Example (split_combined=False):
        >>> books = create_individual_books_from_score(score, split_combined=False)
        >>> # Results in 1 combined PDF:
        >>> #   - Bb_Clarinet_Trumpet_1_Soprano_Sax.pdf (all three instruments share this book)
    """
    generator = IndividualBookGenerator()
    return generator.export_individual_books(multipart_score, output_dir, split_combined=split_combined)
