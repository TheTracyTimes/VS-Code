"""
Automatic part generation system for creating derived instrumental parts.

This module provides utilities to:
1. Generate Flute 2 based on all 2nd parts (Alto Sax 2, Trumpet 2, Clarinet 2, Trombone 2)
   - Converts to concert pitch and adjusts to proper flute range
2. Generate Flute 3 based on all 3rd parts (Alto Sax 3, Trumpet 3, Clarinet 3, Tenor Sax)
   - Converts to concert pitch and adjusts to proper flute range
3. Create equivalent parts with octave transpositions
4. Copy parts with appropriate transpositions
"""

from typing import List, Dict, Optional, Tuple
from .postprocessing import MusicScore
from .instruments import InstrumentConfig, BandInstruments
from .transposition import Transposer, transpose_score_octaves, ScoreTransposer, Note


class PartMerger:
    """Merges multiple parts to create a single derived part."""

    # Instrument ranges (in MIDI note numbers for easy comparison)
    FLUTE_RANGE = (60, 84)  # C4 to C7
    BARITONE_SAX_RANGE = (38, 69)  # D2 to A4 (concert pitch)

    @staticmethod
    def get_midi_range(pitch_low: str, pitch_high: str) -> Tuple[int, int]:
        """
        Get MIDI range from pitch strings.

        Args:
            pitch_low: Lowest pitch (e.g., 'C4')
            pitch_high: Highest pitch (e.g., 'C7')

        Returns:
            Tuple of (low_midi, high_midi)
        """
        low = Note.from_string(pitch_low).to_midi_number()
        high = Note.from_string(pitch_high).to_midi_number()
        return (low, high)

    @staticmethod
    def transpose_to_range(measure: List[Dict], target_range: Tuple[int, int]) -> List[Dict]:
        """
        Transpose a measure to fit within a target range by adjusting octaves.

        Args:
            measure: List of note dictionaries
            target_range: Tuple of (low_midi, high_midi)

        Returns:
            Transposed measure that fits within the target range
        """
        if not measure:
            return measure

        # Calculate average pitch of the measure
        pitches = []
        for note_data in measure:
            if note_data.get('type') != 'rest' and 'pitch' in note_data:
                try:
                    note = Note.from_string(note_data['pitch'])
                    pitches.append(note.to_midi_number())
                except:
                    continue

        if not pitches:
            return measure  # No notes to transpose

        avg_pitch = sum(pitches) / len(pitches)
        target_center = (target_range[0] + target_range[1]) / 2

        # Calculate how many octaves to shift
        octave_shift = round((target_center - avg_pitch) / 12)

        # Don't shift if already in reasonable range
        if abs(octave_shift) == 0:
            return measure

        # Transpose the measure
        from .transposition import transpose_measure_octaves
        return transpose_measure_octaves(measure, octave_shift)

    @staticmethod
    def adjust_score_to_range(score: MusicScore, target_range: Tuple[int, int]) -> MusicScore:
        """
        Adjust an entire score to fit within a target instrument range.

        Args:
            score: MusicScore to adjust
            target_range: Tuple of (low_midi, high_midi)

        Returns:
            Adjusted MusicScore
        """
        adjusted_score = MusicScore()
        adjusted_score.time_signature = score.time_signature
        adjusted_score.key_signature = score.key_signature
        adjusted_score.clef = score.clef
        adjusted_score.tempo = score.tempo

        for measure in score.measures:
            adjusted_measure = PartMerger.transpose_to_range(measure, target_range)
            adjusted_score.measures.append(adjusted_measure)

        return adjusted_score

    @staticmethod
    def count_notes_in_measure(measure: List[Dict]) -> int:
        """
        Count the number of actual notes (not rests) in a measure.

        Args:
            measure: List of note dictionaries

        Returns:
            Number of notes
        """
        return sum(1 for note in measure if note.get('type') != 'rest')

    @staticmethod
    def measure_activity_score(measure: List[Dict]) -> float:
        """
        Calculate an activity score for a measure.
        Higher score = more musical activity.

        Args:
            measure: List of note dictionaries

        Returns:
            Activity score
        """
        if not measure:
            return 0.0

        note_count = PartMerger.count_notes_in_measure(measure)
        total_items = len(measure)

        # Activity is ratio of notes to total items
        activity = note_count / total_items if total_items > 0 else 0.0

        return activity

    @staticmethod
    def select_best_measure(measures: List[List[Dict]]) -> List[Dict]:
        """
        Select the measure with the most musical activity from a list of measures.

        Args:
            measures: List of measure data from different parts

        Returns:
            The measure with the highest activity score
        """
        if not measures:
            return []

        if len(measures) == 1:
            return measures[0]

        # Score each measure
        scores = [PartMerger.measure_activity_score(m) for m in measures]

        # Return the measure with the highest score
        best_idx = scores.index(max(scores))
        return measures[best_idx]

    @staticmethod
    def merge_parts_by_activity(parts: Dict[str, MusicScore]) -> MusicScore:
        """
        Merge multiple parts by selecting the most active measure at each position.

        Args:
            parts: Dictionary of part name to MusicScore

        Returns:
            Merged MusicScore
        """
        if not parts:
            raise ValueError("No parts provided for merging")

        # Get a reference score for metadata
        reference_score = list(parts.values())[0]

        # Create merged score
        merged = MusicScore()
        merged.time_signature = reference_score.time_signature
        merged.key_signature = reference_score.key_signature
        merged.clef = reference_score.clef
        merged.tempo = reference_score.tempo

        # Get the maximum number of measures
        max_measures = max(len(score.measures) for score in parts.values())

        # For each measure position, select the best
        for measure_idx in range(max_measures):
            candidate_measures = []

            for score in parts.values():
                if measure_idx < len(score.measures):
                    candidate_measures.append(score.measures[measure_idx])

            # Select the best measure
            best_measure = PartMerger.select_best_measure(candidate_measures)
            merged.measures.append(best_measure)

        return merged


class PartGenerator:
    """Generates derived instrumental parts from existing parts."""

    def __init__(self, multipart_score: 'MultiPartScore'):
        """
        Initialize part generator.

        Args:
            multipart_score: MultiPartScore containing all parts
        """
        self.multipart_score = multipart_score

    def generate_flute_2(self) -> Optional[MusicScore]:
        """
        Generate Flute 2 part based on all 2nd parts.

        Looks at: 2nd Alto Sax, 2nd Trumpet, 2nd Clarinet, 2nd Trombone.
        - Converts all parts to concert pitch (proper key for flute)
        - Selects the most active melody at each measure
        - Adjusts to proper flute range (C4-C7)

        Returns:
            Generated Flute 2 MusicScore in concert pitch and proper range
        """
        # Define which parts to look for
        second_part_names = [
            "2nd Bb Clarinet", "2nd B♭ Clarinet",
            "2nd Bb Trumpet", "2nd B♭ Trumpet",
            "2nd Eb Alto Sax", "2nd E♭ Alto Saxophone",
            "2nd C Trombone", "2nd Trombone"
        ]

        # Collect all available 2nd parts
        available_parts = {}
        for part_name, (score, instrument) in self.multipart_score.parts.items():
            for target_name in second_part_names:
                if target_name.lower() in part_name.lower():
                    # Convert to concert pitch
                    transposer = Transposer(instrument)
                    concert_score = self._transpose_to_concert(score, transposer)
                    available_parts[part_name] = concert_score
                    break

        if not available_parts:
            print("Warning: No 2nd parts found for Flute 2 generation")
            return None

        # Merge parts by selecting most active measures
        merged = PartMerger.merge_parts_by_activity(available_parts)

        # Adjust to proper flute range
        adjusted = PartMerger.adjust_score_to_range(merged, PartMerger.FLUTE_RANGE)

        # Set appropriate clef for flute
        adjusted.clef = 'G'

        return adjusted

    def generate_flute_3(self) -> Optional[MusicScore]:
        """
        Generate Flute 3 part based on all 3rd parts.

        Looks at: 3rd Alto Sax, 3rd Trumpet, 3rd Clarinet, Tenor Sax.
        - Converts all parts to concert pitch (proper key for flute)
        - Selects the most active melody at each measure
        - Adjusts to proper flute range (C4-C7)

        Returns:
            Generated Flute 3 MusicScore in concert pitch and proper range
        """
        # Define which parts to look for
        third_part_names = [
            "3rd Bb Clarinet", "3rd B♭ Clarinet",
            "3rd Bb Trumpet", "3rd B♭ Trumpet",
            "3rd Eb Alto Sax", "3rd E♭ Alto Saxophone",
            "Bb Tenor Sax", "B♭ Tenor Saxophone", "Tenor Sax"
        ]

        # Collect all available 3rd parts
        available_parts = {}
        for part_name, (score, instrument) in self.multipart_score.parts.items():
            for target_name in third_part_names:
                if target_name.lower() in part_name.lower():
                    # Convert to concert pitch
                    transposer = Transposer(instrument)
                    concert_score = self._transpose_to_concert(score, transposer)
                    available_parts[part_name] = concert_score
                    break

        if not available_parts:
            print("Warning: No 3rd parts found for Flute 3 generation")
            return None

        # Merge parts by selecting most active measures
        merged = PartMerger.merge_parts_by_activity(available_parts)

        # Adjust to proper flute range
        adjusted = PartMerger.adjust_score_to_range(merged, PartMerger.FLUTE_RANGE)

        # Set appropriate clef for flute
        adjusted.clef = 'G'

        return adjusted

    def generate_baritone_sax(self) -> Optional[MusicScore]:
        """
        Generate Eb Baritone Saxophone part based on low brass parts.

        Looks at: Baritone B.C., Baritone T.C., Tuba.
        - Converts all parts to concert pitch
        - Selects the most active melody at each measure
        - Adjusts to proper baritone sax range (D2-A4 concert pitch)

        Returns:
            Generated Baritone Sax MusicScore in concert pitch and proper range
        """
        # Define which parts to look for
        low_brass_names = [
            "Baritone", "Euphonium", "Euph",
            "Tuba",
            "Bass Clarinet", "B. Cl."
        ]

        # Collect all available low brass parts
        available_parts = {}
        for part_name, (score, instrument) in self.multipart_score.parts.items():
            for target_name in low_brass_names:
                if target_name.lower() in part_name.lower():
                    # Convert to concert pitch
                    transposer = Transposer(instrument)
                    concert_score = self._transpose_to_concert(score, transposer)
                    available_parts[part_name] = concert_score
                    break

        if not available_parts:
            print("Warning: No low brass parts found for Baritone Sax generation")
            return None

        # Merge parts by selecting most active measures
        merged = PartMerger.merge_parts_by_activity(available_parts)

        # Adjust to proper baritone sax range
        adjusted = PartMerger.adjust_score_to_range(merged, PartMerger.BARITONE_SAX_RANGE)

        # Set appropriate clef for baritone sax (treble)
        adjusted.clef = 'G'

        return adjusted

    def _transpose_to_concert(self, score: MusicScore, transposer: Transposer) -> MusicScore:
        """
        Transpose a score to concert pitch.

        Args:
            score: Score to transpose
            transposer: Transposer for the instrument

        Returns:
            Score in concert pitch
        """
        concert_score = MusicScore()
        concert_score.time_signature = score.time_signature
        concert_score.key_signature = score.key_signature
        concert_score.clef = score.clef
        concert_score.tempo = score.tempo

        for measure in score.measures:
            concert_measure = transposer.transpose_measure(measure, from_concert=False)
            concert_score.measures.append(concert_measure)

        return concert_score

    def copy_part_with_octave_shift(self, source_part_name: str, octave_shift: int) -> Optional[MusicScore]:
        """
        Copy a part and shift it by octaves.

        Args:
            source_part_name: Name of the source part
            octave_shift: Number of octaves to shift (positive = up, negative = down)

        Returns:
            Copied and transposed MusicScore, or None if source not found
        """
        # Find the source part
        source_score = None
        source_instrument = None

        for part_name, (score, instrument) in self.multipart_score.parts.items():
            if source_part_name.lower() in part_name.lower():
                source_score = score
                source_instrument = instrument
                break

        if source_score is None:
            print(f"Warning: Source part '{source_part_name}' not found")
            return None

        # Convert to concert pitch first
        transposer = Transposer(source_instrument)
        concert_score = self._transpose_to_concert(source_score, transposer)

        # Apply octave shift
        shifted_score = transpose_score_octaves(concert_score, octave_shift)

        return shifted_score

    def generate_all_derived_parts(self) -> Dict[str, MusicScore]:
        """
        Generate all derived parts based on the user's requirements.

        Returns:
            Dictionary of part name to generated MusicScore (in concert pitch)
        """
        derived_parts = {}

        # Generate Flute 2
        flute_2 = self.generate_flute_2()
        if flute_2:
            derived_parts['Flute 2'] = flute_2
            # Flute 2 = Oboe (same part, different instrument)
            derived_parts['Oboe'] = flute_2

        # Generate Flute 3
        flute_3 = self.generate_flute_3()
        if flute_3:
            derived_parts['Flute 3'] = flute_3
            # Viola = Flute 3 one octave down (using treble clef)
            viola = transpose_score_octaves(flute_3, -1)
            viola.clef = 'G'  # Treble clef
            derived_parts['Viola'] = viola

        # Violin = C Flute 1 octave down
        violin = self.copy_part_with_octave_shift('C Flute', -1)
        if violin:
            derived_parts['Violin'] = violin

        # Tuba = Baritone B.C. octave down
        tuba = self.copy_part_with_octave_shift('Baritone', -1)
        if tuba:
            derived_parts['Tuba'] = tuba

        # 3rd Alto Sax = Alto Clarinet (copy with transposition)
        alto_sax_3 = None
        for part_name, (score, instrument) in self.multipart_score.parts.items():
            if '3rd' in part_name and 'alto sax' in part_name.lower():
                alto_sax_3 = score
                break

        if alto_sax_3:
            # Both are Eb instruments, so just copy
            derived_parts['Alto Clarinet'] = alto_sax_3

        # Trombone 1 = Cello (copy)
        cello = self.copy_part_with_octave_shift('1st Trombone', 0)
        if cello:
            derived_parts['Cello'] = cello

        # Trombone 2 = Bassoon (copy)
        bassoon = self.copy_part_with_octave_shift('2nd Trombone', 0)
        if bassoon:
            derived_parts['Bassoon'] = bassoon

        # 1st Clarinet/Trumpet = Soprano Sax
        # Try to find 1st Clarinet first, then 1st Trumpet
        soprano_sax = self.copy_part_with_octave_shift('1st Clarinet', 0)
        if soprano_sax is None:
            soprano_sax = self.copy_part_with_octave_shift('1st Trumpet', 0)
        if soprano_sax:
            derived_parts['Soprano Sax'] = soprano_sax

        # Generate Eb Baritone Sax from low brass parts
        baritone_sax = self.generate_baritone_sax()
        if baritone_sax:
            derived_parts['Baritone Sax'] = baritone_sax

        return derived_parts


class AutoScoreBuilder:
    """
    Automatically builds complete orchestral scores with all derived parts.
    """

    @staticmethod
    def build_complete_score(multipart_score: 'MultiPartScore') -> 'MultiPartScore':
        """
        Build a complete score with all original and derived parts.

        Args:
            multipart_score: Original MultiPartScore

        Returns:
            New MultiPartScore with all original and derived parts
        """
        from .multipart_score import MultiPartScore

        # Create new score
        complete_score = MultiPartScore(
            title=multipart_score.title,
            composer=multipart_score.composer
        )

        # Copy all original parts
        for part_name, (score, instrument) in multipart_score.parts.items():
            complete_score.add_part(part_name, score, instrument)

        # Generate derived parts
        generator = PartGenerator(multipart_score)
        derived_parts = generator.generate_all_derived_parts()

        # Add derived parts (in concert pitch, so use non-transposing instruments)
        for part_name, score in derived_parts.items():
            # Map to appropriate instrument
            instrument = AutoScoreBuilder._get_instrument_for_part(part_name)
            if instrument:
                complete_score.add_part(part_name, score, instrument)

        return complete_score

    @staticmethod
    def _get_instrument_for_part(part_name: str) -> Optional[InstrumentConfig]:
        """Get the appropriate instrument configuration for a derived part."""
        part_name_lower = part_name.lower()

        if 'flute 2' in part_name_lower:
            return BandInstruments.C_FLUTE_2
        elif 'flute 3' in part_name_lower:
            return BandInstruments.C_FLUTE_3
        elif 'oboe' in part_name_lower:
            return BandInstruments.OBOE
        elif 'viola' in part_name_lower:
            return BandInstruments.VIOLA
        elif 'violin' in part_name_lower:
            return BandInstruments.VIOLIN
        elif 'cello' in part_name_lower:
            return BandInstruments.CELLO
        elif 'bassoon' in part_name_lower:
            return BandInstruments.BASSOON
        elif 'tuba' in part_name_lower:
            return BandInstruments.C_TUBA
        elif 'alto clarinet' in part_name_lower:
            return BandInstruments.Eb_ALTO_CLARINET
        elif 'soprano sax' in part_name_lower:
            return BandInstruments.Bb_SOPRANO_SAX
        elif 'baritone sax' in part_name_lower or 'bari sax' in part_name_lower:
            return BandInstruments.Eb_BARITONE_SAX
        else:
            return None
