"""
Song extraction and individual score generation.

This module provides utilities to:
1. Extract individual songs from multi-song books
2. Create separate full scores for each song
3. Generate conductor scores with all instruments for each song
"""

from typing import List, Dict, Tuple, Optional
from pathlib import Path
from .multipart_score import MultiPartScore
from .postprocessing import MusicScore
from .instruments import InstrumentConfig
from .pdf_export import export_score_to_pdf
import os


class SongExtractor:
    """Extracts individual songs from multi-part scores."""

    def __init__(self):
        """Initialize song extractor."""
        self.songs = []

    def detect_song_boundaries(self, score: MusicScore, title_measures: List[int] = None) -> List[Dict]:
        """
        Detect song boundaries in a score.

        Args:
            score: MusicScore to analyze
            title_measures: Optional list of measure numbers where song titles appear

        Returns:
            List of song dictionaries with 'title', 'start_measure', 'end_measure'
        """
        songs = []

        if title_measures:
            # Use provided measure numbers
            for i, start in enumerate(title_measures):
                end = title_measures[i + 1] - 1 if i + 1 < len(title_measures) else len(score.measures) - 1
                songs.append({
                    'title': f'Song {i + 1}',
                    'start_measure': start,
                    'end_measure': end
                })
        else:
            # Treat entire score as one song
            songs.append({
                'title': 'Complete Score',
                'start_measure': 0,
                'end_measure': len(score.measures) - 1
            })

        return songs

    def extract_song_from_score(self, score: MusicScore, start_measure: int,
                               end_measure: int) -> MusicScore:
        """
        Extract a specific range of measures from a score.

        Args:
            score: Source MusicScore
            start_measure: Starting measure index (0-based)
            end_measure: Ending measure index (inclusive)

        Returns:
            New MusicScore containing only the specified measures
        """
        extracted = MusicScore()
        extracted.time_signature = score.time_signature
        extracted.key_signature = score.key_signature
        extracted.clef = score.clef
        extracted.tempo = score.tempo

        # Copy the specified measure range
        for i in range(start_measure, min(end_measure + 1, len(score.measures))):
            measure = score.measures[i]
            # Deep copy the measure
            copied_measure = [note.copy() for note in measure]
            extracted.measures.append(copied_measure)

        return extracted

    def extract_songs_from_multipart(self, multipart_score: MultiPartScore,
                                    song_info: List[Dict]) -> Dict[str, MultiPartScore]:
        """
        Extract individual songs from a multi-part score.

        Args:
            multipart_score: MultiPartScore containing all parts with all songs
            song_info: List of song dictionaries with 'title', 'start_measure', 'end_measure'

        Returns:
            Dictionary mapping song title to MultiPartScore

        Example song_info:
            [
                {'title': 'March No. 1', 'start_measure': 0, 'end_measure': 32},
                {'title': 'Waltz', 'start_measure': 33, 'end_measure': 64},
                {'title': 'Finale', 'start_measure': 65, 'end_measure': 96}
            ]
        """
        song_scores = {}

        for song in song_info:
            title = song['title']
            start = song['start_measure']
            end = song['end_measure']

            # Create new MultiPartScore for this song
            song_score = MultiPartScore(
                title=title,
                composer=multipart_score.composer
            )

            # Extract this song from each part
            for part_name, (score, instrument) in multipart_score.parts.items():
                extracted_score = self.extract_song_from_score(score, start, end)
                song_score.add_part(part_name, extracted_score, instrument)

            song_scores[title] = song_score

        return song_scores


class IndividualSongScoreGenerator:
    """Generates individual full scores for each song."""

    def __init__(self):
        """Initialize individual song score generator."""
        self.extractor = SongExtractor()

    def create_song_scores(self, multipart_score: MultiPartScore,
                          song_info: List[Dict],
                          output_dir: str = 'output/song_scores') -> Dict[str, str]:
        """
        Create separate full score PDFs for each song.

        Args:
            multipart_score: MultiPartScore containing all parts with all songs
            song_info: List of song dictionaries defining each song
            output_dir: Directory to save song score PDFs

        Returns:
            Dictionary mapping song titles to PDF file paths

        Example:
            >>> song_info = [
            ...     {'title': 'March No. 1', 'start_measure': 0, 'end_measure': 32},
            ...     {'title': 'Waltz', 'start_measure': 33, 'end_measure': 64},
            ... ]
            >>> generator = IndividualSongScoreGenerator()
            >>> scores = generator.create_song_scores(multipart_score, song_info)
            >>> # Creates:
            >>> # output/song_scores/March_No_1_Score.pdf
            >>> # output/song_scores/Waltz_Score.pdf
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Extract songs
        song_scores = self.extractor.extract_songs_from_multipart(multipart_score, song_info)

        # Export each song as a full score
        exported_files = {}

        for song_title, song_score in song_scores.items():
            # Create safe filename
            safe_title = song_title.replace('/', '_').replace(' ', '_').replace('.', '')
            output_path = os.path.join(output_dir, f"{safe_title}_Score.pdf")

            # Export as full score with aligned barlines
            song_score.export_full_score_book(
                output_path,
                num_pages=20,  # Adjust based on song length
                measures_per_system=4,
                systems_per_page=3
            )

            exported_files[song_title] = output_path
            print(f"  ✓ Created score: {safe_title}_Score.pdf")

        return exported_files

    def create_song_parts_and_scores(self, multipart_score: MultiPartScore,
                                    song_info: List[Dict],
                                    parts_output_dir: str = 'output/song_parts',
                                    scores_output_dir: str = 'output/song_scores') -> Dict[str, Dict]:
        """
        Create both individual part books AND full scores for each song.

        Args:
            multipart_score: MultiPartScore containing all parts with all songs
            song_info: List of song dictionaries defining each song
            parts_output_dir: Directory for individual part books per song
            scores_output_dir: Directory for full scores per song

        Returns:
            Dictionary with 'parts' and 'scores' subdictionaries

        Creates directory structure:
            output/
                song_parts/
                    March_No_1/
                        Trombone_1.pdf
                        Flute_2.pdf
                        ...
                    Waltz/
                        Trombone_1.pdf
                        Flute_2.pdf
                        ...
                song_scores/
                    March_No_1_Score.pdf
                    Waltz_Score.pdf
                    ...
        """
        from .individual_books import create_individual_books_from_score

        # Extract songs
        song_scores_dict = self.extractor.extract_songs_from_multipart(multipart_score, song_info)

        results = {
            'parts': {},
            'scores': {}
        }

        for song_title, song_score in song_scores_dict.items():
            safe_title = song_title.replace('/', '_').replace(' ', '_').replace('.', '')

            # Create individual part books for this song
            song_parts_dir = os.path.join(parts_output_dir, safe_title)
            os.makedirs(song_parts_dir, exist_ok=True)

            print(f"\nProcessing song: {song_title}")
            print("  Creating individual part books...")
            part_files = create_individual_books_from_score(song_score, song_parts_dir)
            results['parts'][song_title] = part_files

            # Create full score for this song
            print("  Creating full score...")
            scores_dir = os.path.join(scores_output_dir)
            os.makedirs(scores_dir, exist_ok=True)

            score_path = os.path.join(scores_dir, f"{safe_title}_Score.pdf")
            song_score.export_full_score_book(
                score_path,
                num_pages=20,
                measures_per_system=4,
                systems_per_page=3
            )
            results['scores'][song_title] = score_path
            print(f"  ✓ Created: {safe_title}_Score.pdf")

        return results


def extract_songs_and_create_scores(multipart_score: MultiPartScore,
                                    song_info: List[Dict],
                                    output_base_dir: str = 'output/songs') -> Dict[str, Dict]:
    """
    Main function to extract songs and create all outputs.

    Args:
        multipart_score: MultiPartScore with all parts and all songs
        song_info: List of song definitions
        output_base_dir: Base directory for all outputs

    Returns:
        Dictionary with results

    Example:
        >>> # Define your songs
        >>> songs = [
        ...     {'title': 'March No. 1', 'start_measure': 0, 'end_measure': 32},
        ...     {'title': 'Beautiful Waltz', 'start_measure': 33, 'end_measure': 64},
        ...     {'title': 'Grand Finale', 'start_measure': 65, 'end_measure': 96}
        ... ]
        >>>
        >>> # Create all outputs
        >>> results = extract_songs_and_create_scores(complete_score, songs)
        >>>
        >>> # Results in:
        >>> # output/songs/
        >>> #     parts/           (individual part books per song)
        >>> #         March_No_1/
        >>> #             Trombone_1.pdf
        >>> #             Flute_2.pdf
        >>> #             ...
        >>> #         Beautiful_Waltz/
        >>> #             Trombone_1.pdf
        >>> #             ...
        >>> #     scores/          (full conductor scores)
        >>> #         March_No_1_Score.pdf
        >>> #         Beautiful_Waltz_Score.pdf
        >>> #         Grand_Finale_Score.pdf
    """
    generator = IndividualSongScoreGenerator()

    parts_dir = os.path.join(output_base_dir, 'parts')
    scores_dir = os.path.join(output_base_dir, 'scores')

    results = generator.create_song_parts_and_scores(
        multipart_score,
        song_info,
        parts_output_dir=parts_dir,
        scores_output_dir=scores_dir
    )

    print(f"\n{'='*70}")
    print("SONG EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Created {len(song_info)} songs:")
    for song in song_info:
        print(f"  • {song['title']}")
    print(f"\nOutputs saved to: {output_base_dir}/")
    print(f"{'='*70}\n")

    return results
