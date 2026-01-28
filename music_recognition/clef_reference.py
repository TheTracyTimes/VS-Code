"""
Clef Reference System for Proper Notation Placement

This module defines the correct placement of clefs, key signatures, and notes
for different clef types used in the generated instrument parts.
"""

from typing import Dict, Tuple, List


class ClefReference:
    """Reference data for proper clef, key signature, and note placement."""

    # Clef types
    TREBLE = 'G'
    BASS = 'F'
    ALTO = 'C'
    TENOR = 'C'

    # Key signature sharp order (same for all clefs)
    SHARP_ORDER = ['F', 'C', 'G', 'D', 'A', 'E', 'B']

    # Key signature flat order (same for all clefs)
    FLAT_ORDER = ['B', 'E', 'A', 'D', 'G', 'C', 'F']

    @staticmethod
    def get_clef_info(clef_type: str) -> Dict:
        """
        Get positioning information for a specific clef.

        Args:
            clef_type: 'G' (treble), 'F' (bass), or 'C' (alto/tenor)

        Returns:
            Dictionary with clef positioning information
        """
        if clef_type == 'G':
            return {
                'name': 'Treble Clef',
                'symbol': '𝄞',
                'middle_c_line': -1,  # Below staff (first ledger line)
                'key_sig_sharp_positions': [5, 3, 6, 4, 2, 5, 3],  # Line/space from bottom (1=bottom line)
                'key_sig_flat_positions': [3, 5, 3, 6, 4, 2, 4],
                'staff_center': 3,  # B4 on treble clef
            }
        elif clef_type == 'F':
            return {
                'name': 'Bass Clef',
                'symbol': '𝄢',
                'middle_c_line': 6,  # Above staff (first ledger line)
                'key_sig_sharp_positions': [4, 2, 5, 3, 1, 4, 2],  # Line/space from bottom
                'key_sig_flat_positions': [2, 4, 1, 3, 1, 3, 1],
                'staff_center': 2,  # D3 on bass clef
            }
        elif clef_type == 'C':
            return {
                'name': 'Alto/Tenor Clef',
                'symbol': '𝄡',
                'middle_c_line': 3,  # Middle line (alto) or 4th line (tenor)
                'key_sig_sharp_positions': [5, 3, 6, 4, 2, 5, 3],
                'key_sig_flat_positions': [3, 5, 3, 6, 4, 2, 4],
                'staff_center': 3,  # C4 on alto clef
            }
        else:
            # Default to treble
            return ClefReference.get_clef_info('G')

    @staticmethod
    def get_key_signature_positions(clef_type: str, key: str) -> List[Tuple[str, int]]:
        """
        Get the positions for sharps or flats in a key signature.

        Args:
            clef_type: 'G' (treble), 'F' (bass), or 'C' (alto)
            key: Key signature (e.g., "G major", "Bb major", "2#", "3b")

        Returns:
            List of (accidental, position) tuples
        """
        clef_info = ClefReference.get_clef_info(clef_type)

        # Parse key to determine number of sharps or flats
        if '#' in key:
            # Sharp key
            num_sharps = int(key.split('#')[0]) if key[0].isdigit() else 1
            positions = []
            for i in range(num_sharps):
                note = ClefReference.SHARP_ORDER[i]
                position = clef_info['key_sig_sharp_positions'][i]
                positions.append(('♯', note, position))
            return positions
        elif 'b' in key.lower():
            # Flat key
            num_flats = int(key.split('b')[0]) if key[0].isdigit() else 1
            positions = []
            for i in range(num_flats):
                note = ClefReference.FLAT_ORDER[i]
                position = clef_info['key_sig_flat_positions'][i]
                positions.append(('♭', note, position))
            return positions
        else:
            # C major / A minor (no sharps or flats)
            return []

    @staticmethod
    def get_note_position_on_staff(pitch: str, clef_type: str) -> int:
        """
        Calculate the vertical position of a note on the staff for a given clef.

        Args:
            pitch: Note pitch (e.g., "C4", "G5", "F#3")
            clef_type: 'G' (treble), 'F' (bass), or 'C' (alto)

        Returns:
            Staff position (0 = bottom line, 4 = top line, negative = below, positive > 4 = above)
        """
        # Parse pitch
        note_name = pitch[0].upper()
        octave = int(pitch[-1])
        accidental = pitch[1:-1] if len(pitch) > 2 else ''

        # Note values relative to C (0 = C, 1 = D, 2 = E, etc.)
        note_values = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
        note_value = note_values.get(note_name, 0)

        # Calculate MIDI-like position (C4 = 60)
        position = octave * 7 + note_value

        clef_info = ClefReference.get_clef_info(clef_type)

        # Reference positions for each clef
        if clef_type == 'G':
            # Treble clef: bottom line (E4) = position 0
            # E4 = octave 4 * 7 + 2 = 30
            e4_position = 30
            staff_position = (position - e4_position)
        elif clef_type == 'F':
            # Bass clef: bottom line (G2) = position 0
            # G2 = octave 2 * 7 + 4 = 18
            g2_position = 18
            staff_position = (position - g2_position)
        else:  # Alto/Tenor clef
            # Alto clef: bottom line (F3) = position 0
            # F3 = octave 3 * 7 + 3 = 24
            f3_position = 24
            staff_position = (position - f3_position)

        return staff_position


# Quick reference for generated parts
GENERATED_PARTS_CLEFS = {
    'Viola': 'G',        # Treble clef (sometimes alto, but we use treble)
    'Violin': 'G',       # Treble clef
    'Flute 2': 'G',      # Treble clef
    'Flute 3': 'G',      # Treble clef
    'Oboe': 'G',         # Treble clef
    'Alto Clarinet': 'G', # Treble clef
    'Baritone Sax': 'G',  # Treble clef
    'Cello': 'F',        # Bass clef (can use tenor clef for high passages)
    'Bassoon': 'F',      # Bass clef (can use tenor clef for high passages)
    'Tuba': 'F',         # Bass clef
}


# Key signature reference (circle of fifths)
KEY_SIGNATURES = {
    # Major keys with sharps
    'C major': 0,
    'G major': 1,   # F#
    'D major': 2,   # F#, C#
    'A major': 3,   # F#, C#, G#
    'E major': 4,   # F#, C#, G#, D#
    'B major': 5,   # F#, C#, G#, D#, A#
    'F# major': 6,  # F#, C#, G#, D#, A#, E#
    'C# major': 7,  # F#, C#, G#, D#, A#, E#, B#

    # Major keys with flats
    'F major': 1,   # Bb
    'Bb major': 2,  # Bb, Eb
    'Eb major': 3,  # Bb, Eb, Ab
    'Ab major': 4,  # Bb, Eb, Ab, Db
    'Db major': 5,  # Bb, Eb, Ab, Db, Gb
    'Gb major': 6,  # Bb, Eb, Ab, Db, Gb, Cb
    'Cb major': 7,  # Bb, Eb, Ab, Db, Gb, Cb, Fb
}


def get_transposed_key_signature(original_key: str, semitones: int) -> str:
    """
    Transpose a key signature by a given number of semitones.

    Args:
        original_key: Original key (e.g., "C major")
        semitones: Number of semitones to transpose (positive = up, negative = down)

    Returns:
        Transposed key signature
    """
    # Circle of fifths mapping (0 = C, 1 = G, 2 = D, etc.)
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

    # Get current key position
    original_tonic = original_key.split()[0]
    if original_tonic in keys:
        current_pos = keys.index(original_tonic)
    else:
        return original_key  # Can't transpose unknown key

    # Calculate new position (each position in circle of fifths = 7 semitones)
    # But semitones don't map directly to circle of fifths
    # Simplified: use chromatic transposition
    chromatic = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    current_chromatic = chromatic.index(original_tonic) if original_tonic in chromatic else 0

    new_chromatic = (current_chromatic + semitones) % 12
    new_tonic = chromatic[new_chromatic]

    return f"{new_tonic} major"


class TimeSignature:
    """
    Helper class for time signature representation and drawing.
    """

    # Common time signatures
    COMMON_TIME = 'C'       # 4/4 in common time notation
    CUT_TIME = 'CUT'        # 2/2 in cut time notation (also called alla breve)

    # Unicode symbols
    COMMON_TIME_SYMBOL = '𝄴'  # Unicode for common time (C)
    CUT_TIME_SYMBOL = '𝄵'     # Unicode for cut time (¢)

    @staticmethod
    def parse_time_signature(time_sig: str) -> dict:
        """
        Parse a time signature string.

        Args:
            time_sig: Time signature string (e.g., "4/4", "3/4", "6/8", "C", "CUT")

        Returns:
            Dictionary with parsed time signature information
        """
        if not time_sig:
            return {'type': 'fraction', 'numerator': 4, 'denominator': 4}

        time_sig = time_sig.strip().upper()

        # Check for special symbols
        if time_sig == 'C' or time_sig == 'COMMON':
            return {
                'type': 'symbol',
                'symbol': TimeSignature.COMMON_TIME_SYMBOL,
                'numerator': 4,
                'denominator': 4
            }
        elif time_sig == 'CUT' or time_sig == 'CUT TIME' or time_sig == 'ALLA BREVE':
            return {
                'type': 'symbol',
                'symbol': TimeSignature.CUT_TIME_SYMBOL,
                'numerator': 2,
                'denominator': 2
            }
        elif '/' in time_sig:
            # Fraction time signature
            parts = time_sig.split('/')
            try:
                numerator = int(parts[0].strip())
                denominator = int(parts[1].strip())
                return {
                    'type': 'fraction',
                    'numerator': numerator,
                    'denominator': denominator
                }
            except (ValueError, IndexError):
                # Default to 4/4 if parsing fails
                return {'type': 'fraction', 'numerator': 4, 'denominator': 4}
        else:
            # Try to parse as just numerator (assume /4)
            try:
                numerator = int(time_sig)
                return {
                    'type': 'fraction',
                    'numerator': numerator,
                    'denominator': 4
                }
            except ValueError:
                # Default to 4/4
                return {'type': 'fraction', 'numerator': 4, 'denominator': 4}

    @staticmethod
    def get_width(time_sig_info: dict) -> float:
        """
        Get the approximate width needed to draw a time signature.

        Args:
            time_sig_info: Parsed time signature information

        Returns:
            Width in points
        """
        if time_sig_info['type'] == 'symbol':
            return 20  # Symbol is fairly compact
        else:
            # Fraction needs more space
            return 25


if __name__ == '__main__':
    # Test clef reference
    print("Clef Reference System")
    print("=" * 60)

    for clef in ['G', 'F', 'C']:
        info = ClefReference.get_clef_info(clef)
        print(f"\n{info['name']} ({clef}):")
        print(f"  Symbol: {info['symbol']}")
        print(f"  Middle C Line: {info['middle_c_line']}")

        # Test key signature positions
        print(f"\n  D Major (2 sharps) positions:")
        positions = ClefReference.get_key_signature_positions(clef, '2#')
        for acc, note, pos in positions:
            print(f"    {acc} on {note}: position {pos}")

    print("\n" + "=" * 60)
    print("\nGenerated Parts Clef Assignments:")
    for part, clef in GENERATED_PARTS_CLEFS.items():
        clef_name = ClefReference.get_clef_info(clef)['name']
        print(f"  {part:20} → {clef_name}")
