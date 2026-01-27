"""
Digital Music Export for Clean Notation

Exports digitized music to standard formats:
1. MusicXML - for opening in MuseScore, Finale, Sibelius, Dorico
2. MIDI - for audio playback in any music software

No interactive viewer - just clean file exports for use in professional software.
"""

import os
import json
from typing import List, Dict, Optional
from pathlib import Path
import xml.etree.ElementTree as ET


class MusicXMLExporter:
    """Export music scores to MusicXML format for notation display."""
    
    def __init__(self):
        self.version = "3.1"
    
    def export_score_to_musicxml(self, score, part_name: str, output_path: str):
        """
        Export a MusicScore to MusicXML format.
        
        Args:
            score: MusicScore object
            part_name: Name of the part
            output_path: Path to save MusicXML file
        """
        # Create root element
        root = ET.Element('score-partwise', version=self.version)
        
        # Add work title
        work = ET.SubElement(root, 'work')
        work_title = ET.SubElement(work, 'work-title')
        work_title.text = getattr(score, 'title', 'Untitled')
        
        # Add part list
        part_list = ET.SubElement(root, 'part-list')
        score_part = ET.SubElement(part_list, 'score-part', id='P1')
        part_name_elem = ET.SubElement(score_part, 'part-name')
        part_name_elem.text = part_name
        
        # Add part data
        part = ET.SubElement(root, 'part', id='P1')
        
        # Add measures
        for i, measure in enumerate(score.measures, 1):
            measure_elem = ET.SubElement(part, 'measure', number=str(i))
            
            # Add attributes for first measure
            if i == 1:
                attributes = ET.SubElement(measure_elem, 'attributes')
                
                # Add divisions (for note duration)
                divisions = ET.SubElement(attributes, 'divisions')
                divisions.text = '4'  # Quarter note = 4 divisions
                
                # Add key signature
                key = ET.SubElement(attributes, 'key')
                fifths = ET.SubElement(key, 'fifths')
                fifths.text = str(self._get_key_fifths(score.key_signature))
                
                # Add time signature
                time = ET.SubElement(attributes, 'time')
                beats = ET.SubElement(time, 'beats')
                beats.text = str(score.time_signature[0])
                beat_type = ET.SubElement(time, 'beat-type')
                beat_type.text = str(score.time_signature[1])
                
                # Add clef
                clef = ET.SubElement(attributes, 'clef')
                sign = ET.SubElement(clef, 'sign')
                sign.text = 'G' if score.clef in ['treble', 'G'] else 'F'
                line = ET.SubElement(clef, 'line')
                line.text = '2' if score.clef in ['treble', 'G'] else '4'
            
            # Add notes (simplified - assumes measure has notes attribute)
            if hasattr(measure, 'notes'):
                for note in measure.notes:
                    note_elem = ET.SubElement(measure_elem, 'note')
                    
                    # Add pitch or rest
                    if note.is_rest:
                        ET.SubElement(note_elem, 'rest')
                    else:
                        pitch = ET.SubElement(note_elem, 'pitch')
                        step = ET.SubElement(pitch, 'step')
                        step.text = note.pitch[0]  # C, D, E, etc.
                        octave = ET.SubElement(pitch, 'octave')
                        octave.text = str(note.octave)
                        
                        if len(note.pitch) > 1:  # Has accidental
                            alter = ET.SubElement(pitch, 'alter')
                            alter.text = '1' if '#' in note.pitch else '-1'
                    
                    # Add duration
                    duration = ET.SubElement(note_elem, 'duration')
                    duration.text = str(note.duration * 4)  # Convert to divisions
                    
                    # Add note type
                    note_type = ET.SubElement(note_elem, 'type')
                    note_type.text = self._get_note_type(note.duration)
        
        # Write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    def _get_key_fifths(self, key_sig: str) -> int:
        """Convert key signature to fifths value (-7 to 7)."""
        key_map = {
            'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
            'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7
        }
        return key_map.get(key_sig, 0)
    
    def _get_note_type(self, duration: float) -> str:
        """Convert duration to note type."""
        if duration >= 4:
            return 'whole'
        elif duration >= 2:
            return 'half'
        elif duration >= 1:
            return 'quarter'
        elif duration >= 0.5:
            return 'eighth'
        elif duration >= 0.25:
            return '16th'
        else:
            return '32nd'


class MIDIGenerator:
    """Generate MIDI files for audio playback."""
    
    def __init__(self):
        self.ticks_per_beat = 480
    
    def export_score_to_midi(self, score, instrument_name: str, output_path: str):
        """
        Export a MusicScore to MIDI format for audio playback.
        
        Args:
            score: MusicScore object
            instrument_name: Name of the instrument
            output_path: Path to save MIDI file
        """
        try:
            import mido
            from mido import MidiFile, MidiTrack, Message, MetaMessage
        except ImportError:
            print("⚠️  mido not installed. Install with: pip install mido")
            return
        
        # Create MIDI file
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        # Add track name
        track.append(MetaMessage('track_name', name=instrument_name, time=0))
        
        # Add tempo (if available)
        tempo = getattr(score, 'tempo', 120)
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo), time=0))
        
        # Add time signature
        track.append(MetaMessage('time_signature',
                                numerator=score.time_signature[0],
                                denominator=score.time_signature[1],
                                time=0))
        
        # Add notes from measures
        current_time = 0
        for measure in score.measures:
            if hasattr(measure, 'notes'):
                for note in measure.notes:
                    if not note.is_rest:
                        # Note on
                        midi_note = self._pitch_to_midi(note.pitch, note.octave)
                        velocity = 64  # Medium velocity
                        track.append(Message('note_on',
                                           note=midi_note,
                                           velocity=velocity,
                                           time=current_time))
                        current_time = 0
                        
                        # Note duration
                        duration_ticks = int(note.duration * self.ticks_per_beat)
                        
                        # Note off
                        track.append(Message('note_off',
                                           note=midi_note,
                                           velocity=0,
                                           time=duration_ticks))
                    else:
                        # Rest - just advance time
                        current_time += int(note.duration * self.ticks_per_beat)
        
        # Save MIDI file
        mid.save(output_path)
    
    def _pitch_to_midi(self, pitch: str, octave: int) -> int:
        """Convert pitch name to MIDI note number."""
        note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        
        base_note = note_map.get(pitch[0], 0)
        
        # Handle accidentals
        if '#' in pitch:
            base_note += 1
        elif 'b' in pitch:
            base_note -= 1
        
        # MIDI note = base + (octave * 12) + 12 (middle C = 60)
        return base_note + (octave * 12) + 12


class DigitalMusicExporter:
    """Export digitized music to MusicXML and MIDI formats."""

    def __init__(self):
        self.musicxml_exporter = MusicXMLExporter()
        self.midi_generator = MIDIGenerator()
    
    def export_digital_music(self,
                            scores: Dict[str, tuple],
                            output_dir: str,
                            song_title: str = "Song"):
        """
        Export digitized music to MusicXML and MIDI formats.

        Args:
            scores: Dictionary of part_name -> (MusicScore, InstrumentConfig)
            output_dir: Directory to save the digital files
            song_title: Title of the song

        Returns:
            Path to the output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        musicxml_dir = output_path / 'musicxml'
        midi_dir = output_path / 'midi'
        musicxml_dir.mkdir(exist_ok=True)
        midi_dir.mkdir(exist_ok=True)

        # Export each part to MusicXML and MIDI
        part_files = {}
        for part_name, (score, instrument) in scores.items():
            safe_name = part_name.replace(' ', '_').replace('/', '_')

            # Export MusicXML
            musicxml_path = musicxml_dir / f"{safe_name}.musicxml"
            self.musicxml_exporter.export_score_to_musicxml(
                score, part_name, str(musicxml_path)
            )

            # Export MIDI
            midi_path = midi_dir / f"{safe_name}.mid"
            self.midi_generator.export_score_to_midi(
                score, part_name, str(midi_path)
            )

            part_files[part_name] = {
                'musicxml': f'musicxml/{safe_name}.musicxml',
                'midi': f'midi/{safe_name}.mid',
                'instrument': instrument.name
            }

        # Create index.json with part information (for reference)
        index_data = {
            'title': song_title,
            'parts': part_files
        }

        with open(output_path / 'index.json', 'w') as f:
            json.dump(index_data, f, indent=2)

        print(f"✅ Digital music exported: {song_title}")
        print(f"   - {len(part_files)} parts exported")
        print(f"   - MusicXML files: {musicxml_dir}")
        print(f"   - MIDI files: {midi_dir}")
        print(f"   - Open .musicxml files in MuseScore, Finale, etc.")

        return str(output_dir)
    
def create_digital_book_from_multipart_score(multipart_score,
                                             output_dir: str,
                                             song_title: str = "Song"):
    """
    Export digitized music to MusicXML and MIDI from a MultiPartScore.

    Creates clean, digitized notation files that can be opened in:
    - MuseScore, Finale, Sibelius, Dorico (MusicXML)
    - Any MIDI player or DAW (MIDI files)

    Args:
        multipart_score: MultiPartScore object with all parts
        output_dir: Directory to save the digital files
        song_title: Title of the song

    Returns:
        Path to the output directory
    """
    exporter = DigitalMusicExporter()
    return exporter.export_digital_music(
        multipart_score.parts,
        output_dir,
        song_title
    )
