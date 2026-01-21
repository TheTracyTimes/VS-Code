"""
Convert detected symbols to standard music notation formats.
"""

from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom


class MusicScore:
    """Represents a complete music score."""

    def __init__(self):
        """Initialize an empty music score."""
        self.measures = []
        self.time_signature = (4, 4)
        self.key_signature = 0
        self.clef = 'treble'
        self.tempo = 120

    def add_measure(self, notes: List[Dict]):
        """Add a measure to the score."""
        self.measures.append(notes)

    def to_dict(self) -> Dict:
        """Convert score to dictionary representation."""
        return {
            'time_signature': self.time_signature,
            'key_signature': self.key_signature,
            'clef': self.clef,
            'tempo': self.tempo,
            'measures': self.measures
        }


class NotationConverter:
    """Converts detected symbols to music notation formats."""

    NOTE_DURATIONS = {
        'whole_note': 4.0,
        'half_note': 2.0,
        'quarter_note': 1.0,
        'eighth_note': 0.5,
        'sixteenth_note': 0.25,
    }

    REST_DURATIONS = {
        'whole_rest': 4.0,
        'half_rest': 2.0,
        'quarter_rest': 1.0,
        'eighth_rest': 0.5,
        'sixteenth_rest': 0.25,
    }

    def __init__(self):
        """Initialize the notation converter."""
        self.current_score = MusicScore()

    def symbols_to_score(self, detections: List[Dict], staff_positions: List[List[int]]) -> MusicScore:
        """
        Convert detected symbols to a music score.

        Args:
            detections: List of detected symbols
            staff_positions: Positions of staff lines

        Returns:
            MusicScore object
        """
        score = MusicScore()

        for det in detections:
            symbol = det['symbol']

            if symbol.endswith('_clef'):
                score.clef = symbol.replace('_clef', '')

            elif symbol.startswith('time_'):
                parts = symbol.replace('time_', '').split('_')
                if len(parts) == 2:
                    score.time_signature = (int(parts[0]), int(parts[1]))

        current_measure = []
        for det in detections:
            symbol = det['symbol']
            bbox = det['bbox']
            y_center = bbox[1] + bbox[3] // 2

            if 'note' in symbol and symbol in self.NOTE_DURATIONS:
                pitch = self._estimate_pitch(y_center, staff_positions)
                note = {
                    'type': 'note',
                    'pitch': pitch,
                    'duration': self.NOTE_DURATIONS[symbol],
                    'position': det['position']
                }
                current_measure.append(note)

            elif 'rest' in symbol and symbol in self.REST_DURATIONS:
                rest = {
                    'type': 'rest',
                    'duration': self.REST_DURATIONS[symbol],
                    'position': det['position']
                }
                current_measure.append(rest)

            elif symbol in ['barline', 'double_barline']:
                if current_measure:
                    score.add_measure(current_measure)
                    current_measure = []

        if current_measure:
            score.add_measure(current_measure)

        self.current_score = score
        return score

    def _estimate_pitch(self, y_position: int, staff_positions: List[List[int]]) -> str:
        """
        Estimate musical pitch from vertical position.

        Args:
            y_position: Vertical position in pixels
            staff_positions: Staff line positions

        Returns:
            Pitch as string (e.g., 'C4', 'G5')
        """
        if not staff_positions or not staff_positions[0]:
            return 'C4'

        staff = staff_positions[0]
        if len(staff) < 5:
            return 'C4'

        staff_space = (staff[-1] - staff[0]) / 4 if len(staff) > 1 else 10

        treble_pitches = ['F5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4']

        line_positions = []
        for i in range(len(staff)):
            line_positions.append(staff[i])
            if i < len(staff) - 1:
                space_pos = (staff[i] + staff[i + 1]) / 2
                line_positions.append(space_pos)

        closest_idx = 0
        min_dist = abs(y_position - line_positions[0])

        for i, pos in enumerate(line_positions):
            dist = abs(y_position - pos)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        if closest_idx < len(treble_pitches):
            return treble_pitches[closest_idx]

        return 'C4'

    def export_musicxml(self, output_path: str):
        """
        Export score to MusicXML format.

        Args:
            output_path: Path to save the MusicXML file
        """
        score_partwise = ET.Element('score-partwise', version='3.1')

        part_list = ET.SubElement(score_partwise, 'part-list')
        score_part = ET.SubElement(part_list, 'score-part', id='P1')
        part_name = ET.SubElement(score_part, 'part-name')
        part_name.text = 'Music'

        part = ET.SubElement(score_partwise, 'part', id='P1')

        for measure_num, measure_notes in enumerate(self.current_score.measures, 1):
            measure = ET.SubElement(part, 'measure', number=str(measure_num))

            if measure_num == 1:
                attributes = ET.SubElement(measure, 'attributes')

                divisions = ET.SubElement(attributes, 'divisions')
                divisions.text = '1'

                time_elem = ET.SubElement(attributes, 'time')
                beats = ET.SubElement(time_elem, 'beats')
                beats.text = str(self.current_score.time_signature[0])
                beat_type = ET.SubElement(time_elem, 'beat-type')
                beat_type.text = str(self.current_score.time_signature[1])

                clef = ET.SubElement(attributes, 'clef')
                sign = ET.SubElement(clef, 'sign')
                sign.text = 'G' if self.current_score.clef == 'treble' else 'F'
                line = ET.SubElement(clef, 'line')
                line.text = '2' if self.current_score.clef == 'treble' else '4'

            for note_data in measure_notes:
                note = ET.SubElement(measure, 'note')

                if note_data['type'] == 'rest':
                    ET.SubElement(note, 'rest')
                else:
                    pitch_elem = ET.SubElement(note, 'pitch')
                    pitch_str = note_data['pitch']
                    step = ET.SubElement(pitch_elem, 'step')
                    step.text = pitch_str[0]
                    octave = ET.SubElement(pitch_elem, 'octave')
                    octave.text = pitch_str[-1]

                duration = ET.SubElement(note, 'duration')
                duration.text = str(int(note_data['duration']))

                type_elem = ET.SubElement(note, 'type')
                duration_val = note_data['duration']
                if duration_val >= 4:
                    type_elem.text = 'whole'
                elif duration_val >= 2:
                    type_elem.text = 'half'
                elif duration_val >= 1:
                    type_elem.text = 'quarter'
                elif duration_val >= 0.5:
                    type_elem.text = 'eighth'
                else:
                    type_elem.text = '16th'

        xml_str = ET.tostring(score_partwise, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ')

        with open(output_path, 'w') as f:
            f.write(pretty_xml)

    def export_abc(self, output_path: str):
        """
        Export score to ABC notation format.

        Args:
            output_path: Path to save the ABC file
        """
        abc_lines = []

        abc_lines.append('X:1')
        abc_lines.append('T:Untitled')
        abc_lines.append('M:{}/{}'.format(*self.current_score.time_signature))
        abc_lines.append('L:1/4')
        abc_lines.append('K:C')

        note_map = {
            'C4': 'C', 'D4': 'D', 'E4': 'E', 'F4': 'F', 'G4': 'G', 'A4': 'A', 'B4': 'B',
            'C5': 'c', 'D5': 'd', 'E5': 'e', 'F5': 'f', 'G5': 'g', 'A5': 'a', 'B5': 'b',
        }

        duration_map = {
            4.0: '4',
            2.0: '2',
            1.0: '',
            0.5: '/2',
            0.25: '/4',
        }

        for measure_notes in self.current_score.measures:
            measure_abc = []
            for note_data in measure_notes:
                if note_data['type'] == 'rest':
                    duration = note_data['duration']
                    dur_str = duration_map.get(duration, '')
                    measure_abc.append('z' + dur_str)
                else:
                    pitch = note_data['pitch']
                    abc_note = note_map.get(pitch, 'C')
                    duration = note_data['duration']
                    dur_str = duration_map.get(duration, '')
                    measure_abc.append(abc_note + dur_str)

            abc_lines.append(' '.join(measure_abc) + ' |')

        with open(output_path, 'w') as f:
            f.write('\n'.join(abc_lines))

    def export_midi(self, output_path: str):
        """
        Export score to MIDI format.

        Args:
            output_path: Path to save the MIDI file
        """
        try:
            from music21 import stream, note, meter, tempo, clef

            s = stream.Score()
            p = stream.Part()

            p.append(clef.TrebleClef() if self.current_score.clef == 'treble' else clef.BassClef())
            p.append(meter.TimeSignature('{}/{}'.format(*self.current_score.time_signature)))
            p.append(tempo.MetronomeMark(number=self.current_score.tempo))

            pitch_map = {
                'C4': 'C4', 'D4': 'D4', 'E4': 'E4', 'F4': 'F4',
                'G4': 'G4', 'A4': 'A4', 'B4': 'B4',
                'C5': 'C5', 'D5': 'D5', 'E5': 'E5', 'F5': 'F5',
                'G5': 'G5', 'A5': 'A5', 'B5': 'B5',
            }

            for measure_notes in self.current_score.measures:
                for note_data in measure_notes:
                    if note_data['type'] == 'rest':
                        r = note.Rest()
                        r.quarterLength = note_data['duration']
                        p.append(r)
                    else:
                        pitch_str = pitch_map.get(note_data['pitch'], 'C4')
                        n = note.Note(pitch_str)
                        n.quarterLength = note_data['duration']
                        p.append(n)

            s.append(p)
            s.write('midi', fp=output_path)

        except ImportError:
            raise ImportError("music21 library required for MIDI export. Install with: pip install music21")
