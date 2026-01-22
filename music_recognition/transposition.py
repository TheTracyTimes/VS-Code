"""
Music transposition utilities for converting between concert pitch and transposed parts.
"""

from typing import Tuple, List, Dict
from .instruments import TransposeInterval, InstrumentConfig


class Note:
    """Represents a musical note with pitch and octave."""

    CHROMATIC_SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ENHARMONIC_MAP = {
        'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb',
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
    }

    def __init__(self, pitch: str, octave: int):
        """
        Initialize a note.

        Args:
            pitch: Note name (C, C#, Db, etc.)
            octave: Octave number (4 = middle C octave)
        """
        self.pitch = pitch.upper()
        self.octave = octave

    @classmethod
    def from_string(cls, note_str: str) -> 'Note':
        """
        Create note from string representation.

        Args:
            note_str: Note as string (e.g., 'C4', 'F#5', 'Bb3')

        Returns:
            Note object
        """
        if len(note_str) < 2:
            raise ValueError(f"Invalid note string: {note_str}")

        if note_str[1] in ['#', 'b']:
            pitch = note_str[:2]
            octave = int(note_str[2:])
        else:
            pitch = note_str[0]
            octave = int(note_str[1:])

        return cls(pitch, octave)

    def to_string(self) -> str:
        """Convert note to string representation."""
        return f"{self.pitch}{self.octave}"

    def to_midi_number(self) -> int:
        """
        Convert note to MIDI note number.

        Returns:
            MIDI note number (0-127)
        """
        # Normalize pitch
        pitch = self.pitch.replace('b', '#')
        if pitch == 'Cb':
            pitch = 'B'
        elif pitch == 'E#':
            pitch = 'F'
        elif pitch == 'B#':
            pitch = 'C'
        elif pitch == 'Fb':
            pitch = 'E'

        # Handle enharmonic equivalents
        if pitch not in self.CHROMATIC_SCALE:
            # Try to find in enharmonic map
            for key, value in self.ENHARMONIC_MAP.items():
                if pitch == key:
                    pitch = value
                    break

        if pitch not in self.CHROMATIC_SCALE:
            # Default to C if still not found
            pitch = 'C'

        pitch_class = self.CHROMATIC_SCALE.index(pitch)
        midi_number = (self.octave + 1) * 12 + pitch_class

        return midi_number

    @classmethod
    def from_midi_number(cls, midi_number: int, use_sharps: bool = True) -> 'Note':
        """
        Create note from MIDI note number.

        Args:
            midi_number: MIDI note number (0-127)
            use_sharps: Use sharps instead of flats for black keys

        Returns:
            Note object
        """
        octave = (midi_number // 12) - 1
        pitch_class = midi_number % 12

        if use_sharps:
            pitch = cls.CHROMATIC_SCALE[pitch_class]
        else:
            # Use flats for black keys
            pitch = cls.CHROMATIC_SCALE[pitch_class]
            if '#' in pitch:
                pitch = cls.ENHARMONIC_MAP.get(pitch, pitch)

        return cls(pitch, octave)

    def transpose_semitones(self, semitones: int, use_sharps: bool = True) -> 'Note':
        """
        Transpose note by semitones.

        Args:
            semitones: Number of semitones to transpose (positive = up, negative = down)
            use_sharps: Use sharps instead of flats

        Returns:
            Transposed note
        """
        midi = self.to_midi_number()
        new_midi = midi + semitones
        return Note.from_midi_number(new_midi, use_sharps)

    def transpose_interval(self, interval: TransposeInterval, use_sharps: bool = True) -> 'Note':
        """
        Transpose note by a standard interval.

        Args:
            interval: Transposition interval
            use_sharps: Use sharps instead of flats

        Returns:
            Transposed note
        """
        semitones, octaves = interval.value
        midi = self.to_midi_number()
        new_midi = midi + semitones + (octaves * 12)
        return Note.from_midi_number(new_midi, use_sharps)

    def __repr__(self) -> str:
        return f"Note({self.to_string()})"

    def __str__(self) -> str:
        return self.to_string()


class Transposer:
    """Handles transposition between concert pitch and instrument transpositions."""

    def __init__(self, instrument: InstrumentConfig):
        """
        Initialize transposer for an instrument.

        Args:
            instrument: Instrument configuration
        """
        self.instrument = instrument
        self.interval = instrument.transposition

    def concert_to_written(self, concert_pitch: str) -> str:
        """
        Convert concert pitch to written pitch for the instrument.

        Args:
            concert_pitch: Note in concert pitch (e.g., 'C4')

        Returns:
            Written pitch for the instrument
        """
        if self.interval == TransposeInterval.NONE:
            return concert_pitch

        note = Note.from_string(concert_pitch)

        # For transposing instruments, written pitch is HIGHER than concert pitch
        # e.g., Bb clarinet reads a C but sounds a Bb (concert pitch is 2 semitones down)
        # So to go from concert to written, we transpose UP
        semitones, octaves = self.interval.value
        transposed = note.transpose_semitones(-semitones - (octaves * 12))

        return transposed.to_string()

    def written_to_concert(self, written_pitch: str) -> str:
        """
        Convert written pitch to concert pitch.

        Args:
            written_pitch: Written pitch for the instrument

        Returns:
            Concert pitch
        """
        if self.interval == TransposeInterval.NONE:
            return written_pitch

        note = Note.from_string(written_pitch)

        # Apply the transposition interval
        semitones, octaves = self.interval.value
        transposed = note.transpose_semitones(semitones + (octaves * 12))

        return transposed.to_string()

    def transpose_note_data(self, note_data: Dict, from_concert: bool = True) -> Dict:
        """
        Transpose note data dictionary.

        Args:
            note_data: Dictionary with note information
            from_concert: If True, convert from concert to written; else written to concert

        Returns:
            Transposed note data
        """
        if note_data['type'] == 'rest':
            return note_data.copy()

        transposed = note_data.copy()

        if 'pitch' in note_data:
            if from_concert:
                transposed['pitch'] = self.concert_to_written(note_data['pitch'])
            else:
                transposed['pitch'] = self.written_to_concert(note_data['pitch'])

        return transposed

    def transpose_measure(self, measure: List[Dict], from_concert: bool = True) -> List[Dict]:
        """
        Transpose all notes in a measure.

        Args:
            measure: List of note dictionaries
            from_concert: If True, convert from concert to written

        Returns:
            Transposed measure
        """
        return [self.transpose_note_data(note, from_concert) for note in measure]


class ScoreTransposer:
    """Handles transposition for entire scores with multiple parts."""

    @staticmethod
    def transpose_score_to_concert(parts: Dict[str, 'MusicScore'],
                                   instruments: Dict[str, InstrumentConfig]) -> Dict[str, 'MusicScore']:
        """
        Transpose all parts to concert pitch.

        Args:
            parts: Dictionary of part name to MusicScore
            instruments: Dictionary of part name to InstrumentConfig

        Returns:
            Dictionary of transposed scores in concert pitch
        """
        from .postprocessing import MusicScore

        concert_parts = {}

        for part_name, score in parts.items():
            if part_name not in instruments:
                concert_parts[part_name] = score
                continue

            instrument = instruments[part_name]
            transposer = Transposer(instrument)

            # Create new score in concert pitch
            concert_score = MusicScore()
            concert_score.time_signature = score.time_signature
            concert_score.key_signature = score.key_signature
            concert_score.clef = score.clef
            concert_score.tempo = score.tempo

            # Transpose each measure
            for measure in score.measures:
                concert_measure = transposer.transpose_measure(measure, from_concert=False)
                concert_score.measures.append(concert_measure)

            concert_parts[part_name] = concert_score

        return concert_parts

    @staticmethod
    def concert_to_transposed_parts(concert_score: 'MusicScore',
                                    instruments: List[InstrumentConfig]) -> Dict[str, 'MusicScore']:
        """
        Create transposed parts from a concert pitch score.

        Args:
            concert_score: Score in concert pitch
            instruments: List of instruments to create parts for

        Returns:
            Dictionary of instrument name to transposed MusicScore
        """
        from .postprocessing import MusicScore

        transposed_parts = {}

        for instrument in instruments:
            transposer = Transposer(instrument)

            # Create new transposed score
            part_score = MusicScore()
            part_score.time_signature = concert_score.time_signature
            part_score.key_signature = concert_score.key_signature
            part_score.clef = instrument.clef.value
            part_score.tempo = concert_score.tempo

            # Transpose each measure
            for measure in concert_score.measures:
                transposed_measure = transposer.transpose_measure(measure, from_concert=True)
                part_score.measures.append(transposed_measure)

            transposed_parts[instrument.name] = part_score

        return transposed_parts


def transpose_pitch_string(pitch: str, semitones: int) -> str:
    """
    Utility function to transpose a pitch string by semitones.

    Args:
        pitch: Pitch string (e.g., 'C4', 'F#5')
        semitones: Number of semitones to transpose

    Returns:
        Transposed pitch string
    """
    note = Note.from_string(pitch)
    transposed = note.transpose_semitones(semitones)
    return transposed.to_string()
