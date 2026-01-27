"""
Digital Interactive Music Book Generator

Creates interactive digital books with:
1. Visual notation display (MusicXML format)
2. Audio playback (MIDI generation)
3. Web-based viewer with playback controls
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


class InteractiveBookGenerator:
    """Generate interactive web-based music books."""
    
    def __init__(self):
        self.musicxml_exporter = MusicXMLExporter()
        self.midi_generator = MIDIGenerator()
    
    def create_interactive_book(self,
                               scores: Dict[str, tuple],
                               output_dir: str,
                               book_title: str = "Music Book"):
        """
        Create an interactive digital book with notation and audio.
        
        Args:
            scores: Dictionary of part_name -> (MusicScore, InstrumentConfig)
            output_dir: Directory to save the interactive book
            book_title: Title of the book
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
        
        # Create index.json with part information
        index_data = {
            'title': book_title,
            'parts': part_files
        }
        
        with open(output_path / 'index.json', 'w') as f:
            json.dump(index_data, f, indent=2)
        
        # Create HTML viewer
        self._create_html_viewer(output_path, book_title)
        
        print(f"✅ Interactive book created: {output_dir}")
        print(f"   - {len(part_files)} parts exported")
        print(f"   - MusicXML files: {musicxml_dir}")
        print(f"   - MIDI files: {midi_dir}")
        print(f"   - Open index.html in a browser to view")
    
    def _create_html_viewer(self, output_path: Path, book_title: str):
        """Create HTML/JavaScript viewer for the interactive book."""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_title} - Interactive Music Book</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}
        
        .part-selector {{
            margin-bottom: 30px;
        }}
        
        select {{
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #667eea;
            border-radius: 8px;
            cursor: pointer;
        }}
        
        .player-controls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .control-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            margin-right: 10px;
            transition: all 0.3s;
        }}
        
        .control-btn:hover {{
            background: #764ba2;
            transform: translateY(-2px);
        }}
        
        .control-btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}
        
        .notation-display {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            min-height: 400px;
            background: white;
            margin-bottom: 20px;
        }}
        
        .info-panel {{
            background: #f0f2ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .download-links {{
            margin-top: 20px;
        }}
        
        .download-btn {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-right: 10px;
            margin-bottom: 10px;
        }}
        
        .download-btn:hover {{
            background: #218838;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 {book_title}</h1>
        <p class="subtitle">Interactive Digital Music Book with Audio Playback</p>
        
        <div class="part-selector">
            <label for="part-select"><strong>Select Part:</strong></label><br><br>
            <select id="part-select" onchange="loadPart()">
                <option value="">-- Choose an instrument --</option>
            </select>
        </div>
        
        <div class="player-controls">
            <button class="control-btn" id="play-btn" onclick="playAudio()" disabled>▶️ Play</button>
            <button class="control-btn" id="pause-btn" onclick="pauseAudio()" disabled>⏸️ Pause</button>
            <button class="control-btn" id="stop-btn" onclick="stopAudio()" disabled>⏹️ Stop</button>
        </div>
        
        <div class="notation-display" id="notation-display">
            <p style="text-align: center; color: #999; padding: 50px;">
                Select a part to view notation and play audio
            </p>
        </div>
        
        <div class="info-panel" id="info-panel" style="display: none;">
            <h3>Current Part Information</h3>
            <p id="part-info"></p>
            
            <div class="download-links">
                <strong>Download Files:</strong><br><br>
                <a href="#" id="download-musicxml" class="download-btn" download>📄 Download MusicXML</a>
                <a href="#" id="download-midi" class="download-btn" download>🎵 Download MIDI</a>
            </div>
        </div>
    </div>
    
    <script>
        let bookData = null;
        let currentPart = null;
        let audioContext = null;
        let currentSound = null;
        
        // Load book data
        async function loadBookData() {{
            const response = await fetch('index.json');
            bookData = await response.json();
            
            // Populate part selector
            const select = document.getElementById('part-select');
            for (const [partName, partData] of Object.entries(bookData.parts)) {{
                const option = document.createElement('option');
                option.value = partName;
                option.textContent = partName;
                select.appendChild(option);
            }}
        }}
        
        // Load selected part
        async function loadPart() {{
            const partName = document.getElementById('part-select').value;
            if (!partName) return;
            
            currentPart = bookData.parts[partName];
            
            // Load MusicXML notation
            const musicxmlResponse = await fetch(currentPart.musicxml);
            const musicxmlText = await musicxmlResponse.text();
            
            // Display notation (simplified - in production use OSMD or VexFlow)
            const notationDisplay = document.getElementById('notation-display');
            notationDisplay.innerHTML = `
                <h3>${{partName}}</h3>
                <p><strong>Instrument:</strong> ${{currentPart.instrument}}</p>
                <p style="margin-top: 20px;">
                    <em>MusicXML notation loaded. In a full implementation, this would display 
                    interactive sheet music using libraries like OpenSheetMusicDisplay.</em>
                </p>
                <pre style="max-height: 300px; overflow: auto; background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px;">
${{musicxmlText.substring(0, 500)}}...
                </pre>
            `;
            
            // Enable player controls
            document.getElementById('play-btn').disabled = false;
            document.getElementById('stop-btn').disabled = false;
            
            // Show info panel
            document.getElementById('info-panel').style.display = 'block';
            document.getElementById('part-info').textContent = 
                `Part: ${{partName}} | Instrument: ${{currentPart.instrument}}`;
            
            // Set download links
            document.getElementById('download-musicxml').href = currentPart.musicxml;
            document.getElementById('download-midi').href = currentPart.midi;
        }}
        
        // Audio playback functions
        function playAudio() {{
            // In production, use MIDI.js or Web MIDI API to play the MIDI file
            alert('Audio playback would start here. In a full implementation, this would use MIDI.js or Web Audio API to play the MIDI file.');
            document.getElementById('pause-btn').disabled = false;
        }}
        
        function pauseAudio() {{
            alert('Audio paused');
            document.getElementById('pause-btn').disabled = true;
        }}
        
        function stopAudio() {{
            alert('Audio stopped');
            document.getElementById('pause-btn').disabled = true;
        }}
        
        // Initialize
        window.addEventListener('DOMContentLoaded', loadBookData);
    </script>
</body>
</html>
"""
        
        with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)


def create_digital_book_from_multipart_score(multipart_score,
                                             output_dir: str,
                                             book_title: str = "Digital Music Book"):
    """
    Convenience function to create an interactive book from a MultiPartScore.
    
    Args:
        multipart_score: MultiPartScore object
        output_dir: Directory to save the interactive book
        book_title: Title of the book
    """
    generator = InteractiveBookGenerator()
    generator.create_interactive_book(
        multipart_score.parts,
        output_dir,
        book_title
    )
