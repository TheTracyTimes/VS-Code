"""
Multi-part score management for orchestral and band arrangements.
"""

from typing import List, Dict, Optional, Tuple
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

from .postprocessing.notation_converter import MusicScore
from .instruments import InstrumentConfig, StandardEnsembles, BandInstruments
from .transposition import Transposer, ScoreTransposer


class MultiPartScore:
    """Represents a complete multi-part musical score."""

    def __init__(self, title: str = "Untitled", composer: str = "Unknown"):
        """
        Initialize a multi-part score.

        Args:
            title: Score title
            composer: Composer name
        """
        self.title = title
        self.composer = composer
        self.parts: Dict[str, MusicScore] = {}  # part_name -> MusicScore
        self.instruments: Dict[str, InstrumentConfig] = {}  # part_name -> InstrumentConfig
        self.time_signature = (4, 4)
        self.key_signature = 0
        self.tempo = 120
        self.part_order: List[str] = []  # Maintains score order (top to bottom)

    def add_part(self, part_name: str, score: MusicScore, instrument: InstrumentConfig):
        """
        Add a part to the score.

        Args:
            part_name: Name identifier for the part
            score: MusicScore for this part
            instrument: Instrument configuration
        """
        self.parts[part_name] = score
        self.instruments[part_name] = instrument

        if part_name not in self.part_order:
            self.part_order.append(part_name)

        # Sync metadata from first part
        if len(self.parts) == 1:
            self.time_signature = score.time_signature
            self.key_signature = score.key_signature
            self.tempo = score.tempo

    def remove_part(self, part_name: str):
        """Remove a part from the score."""
        if part_name in self.parts:
            del self.parts[part_name]
        if part_name in self.instruments:
            del self.instruments[part_name]
        if part_name in self.part_order:
            self.part_order.remove(part_name)

    def reorder_parts(self, new_order: List[str]):
        """
        Reorder parts in the score.

        Args:
            new_order: List of part names in desired order
        """
        # Validate that all parts exist
        for part_name in new_order:
            if part_name not in self.parts:
                raise ValueError(f"Part '{part_name}' not found in score")

        self.part_order = new_order

    def get_num_measures(self) -> int:
        """Get the number of measures (from longest part)."""
        if not self.parts:
            return 0
        return max(len(score.measures) for score in self.parts.values())

    def to_concert_pitch(self) -> 'MultiPartScore':
        """
        Create a new score with all parts in concert pitch.

        Returns:
            MultiPartScore in concert pitch
        """
        concert_score = MultiPartScore(
            title=f"{self.title} (Concert Pitch)",
            composer=self.composer
        )
        concert_score.time_signature = self.time_signature
        concert_score.key_signature = self.key_signature
        concert_score.tempo = self.tempo
        concert_score.part_order = self.part_order.copy()

        # Transpose each part to concert pitch
        concert_parts = ScoreTransposer.transpose_score_to_concert(
            self.parts,
            self.instruments
        )

        for part_name in self.part_order:
            concert_score.parts[part_name] = concert_parts[part_name]
            concert_score.instruments[part_name] = self.instruments[part_name]

        return concert_score

    def export_musicxml(self, output_path: str, concert_pitch: bool = False):
        """
        Export multi-part score to MusicXML.

        Args:
            output_path: Path to save MusicXML file
            concert_pitch: Export in concert pitch if True
        """
        score_to_export = self.to_concert_pitch() if concert_pitch else self

        # Create score-partwise root
        score_partwise = ET.Element('score-partwise', version='3.1')

        # Add title and composer
        identification = ET.SubElement(score_partwise, 'identification')
        creator = ET.SubElement(identification, 'creator', type='composer')
        creator.text = score_to_export.composer

        # Create part list
        part_list = ET.SubElement(score_partwise, 'part-list')

        for idx, part_name in enumerate(score_to_export.part_order, 1):
            instrument = score_to_export.instruments[part_name]

            score_part = ET.SubElement(part_list, 'score-part', id=f'P{idx}')

            part_name_elem = ET.SubElement(score_part, 'part-name')
            part_name_elem.text = instrument.name

            part_abbr = ET.SubElement(score_part, 'part-abbreviation')
            part_abbr.text = instrument.short_name

            # Add instrument info
            score_instrument = ET.SubElement(score_part, 'score-instrument', id=f'P{idx}-I1')
            instrument_name = ET.SubElement(score_instrument, 'instrument-name')
            instrument_name.text = instrument.name

        # Add parts
        num_measures = score_to_export.get_num_measures()

        for idx, part_name in enumerate(score_to_export.part_order, 1):
            part_score = score_to_export.parts[part_name]
            instrument = score_to_export.instruments[part_name]

            part = ET.SubElement(score_partwise, 'part', id=f'P{idx}')

            # Add measures
            for measure_num in range(1, num_measures + 1):
                measure = ET.SubElement(part, 'measure', number=str(measure_num))

                # Add attributes in first measure
                if measure_num == 1:
                    attributes = ET.SubElement(measure, 'attributes')

                    divisions = ET.SubElement(attributes, 'divisions')
                    divisions.text = '1'

                    # Key signature
                    key = ET.SubElement(attributes, 'key')
                    fifths = ET.SubElement(key, 'fifths')
                    fifths.text = str(score_to_export.key_signature)

                    # Time signature
                    time_elem = ET.SubElement(attributes, 'time')
                    beats = ET.SubElement(time_elem, 'beats')
                    beats.text = str(score_to_export.time_signature[0])
                    beat_type = ET.SubElement(time_elem, 'beat-type')
                    beat_type.text = str(score_to_export.time_signature[1])

                    # Clef
                    clef = ET.SubElement(attributes, 'clef')
                    sign = ET.SubElement(clef, 'sign')
                    line = ET.SubElement(clef, 'line')

                    if instrument.clef.value == 'G':  # Treble
                        sign.text = 'G'
                        line.text = '2'
                    elif instrument.clef.value == 'F':  # Bass
                        sign.text = 'F'
                        line.text = '4'
                    elif instrument.clef.value == 'C':  # Alto/Tenor
                        sign.text = 'C'
                        line.text = '3'

                    # Add tempo in first part only
                    if idx == 1:
                        direction = ET.SubElement(measure, 'direction', placement='above')
                        direction_type = ET.SubElement(direction, 'direction-type')
                        metronome = ET.SubElement(direction_type, 'metronome')
                        beat_unit = ET.SubElement(metronome, 'beat-unit')
                        beat_unit.text = 'quarter'
                        per_minute = ET.SubElement(metronome, 'per-minute')
                        per_minute.text = str(score_to_export.tempo)

                # Add notes for this measure
                if measure_num - 1 < len(part_score.measures):
                    measure_notes = part_score.measures[measure_num - 1]

                    for note_data in measure_notes:
                        note_elem = ET.SubElement(measure, 'note')

                        if note_data['type'] == 'rest':
                            ET.SubElement(note_elem, 'rest')
                        else:
                            pitch_elem = ET.SubElement(note_elem, 'pitch')
                            pitch_str = note_data['pitch']

                            step = ET.SubElement(pitch_elem, 'step')
                            step.text = pitch_str[0]

                            # Handle accidentals
                            if len(pitch_str) > 2 and pitch_str[1] in ['#', 'b']:
                                alter = ET.SubElement(pitch_elem, 'alter')
                                alter.text = '1' if pitch_str[1] == '#' else '-1'
                                octave_idx = 2
                            else:
                                octave_idx = 1

                            octave = ET.SubElement(pitch_elem, 'octave')
                            octave.text = pitch_str[octave_idx:]

                        duration = ET.SubElement(note_elem, 'duration')
                        duration.text = str(int(note_data['duration']))

                        type_elem = ET.SubElement(note_elem, 'type')
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
                else:
                    # Add whole rest for empty measure
                    note_elem = ET.SubElement(measure, 'note')
                    ET.SubElement(note_elem, 'rest', measure='yes')
                    duration = ET.SubElement(note_elem, 'duration')
                    duration.text = str(score_to_export.time_signature[0])

        # Write to file
        xml_str = ET.tostring(score_partwise, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ')

        with open(output_path, 'w') as f:
            f.write(pretty_xml)

        print(f"Multi-part score exported to {output_path}")

    def export_parts_separately(self, output_dir: str, format: str = 'musicxml'):
        """
        Export each part as a separate file.

        Args:
            output_dir: Directory to save part files
            format: Export format ('musicxml', 'midi', 'abc')
        """
        from .postprocessing import NotationConverter

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        for part_name in self.part_order:
            score = self.parts[part_name]
            instrument = self.instruments[part_name]

            converter = NotationConverter()
            converter.current_score = score

            safe_name = part_name.replace(' ', '_').replace('/', '_')

            if format == 'musicxml':
                file_path = output_path / f"{safe_name}.xml"
                converter.export_musicxml(str(file_path))
            elif format == 'midi':
                file_path = output_path / f"{safe_name}.mid"
                converter.export_midi(str(file_path))
            elif format == 'abc':
                file_path = output_path / f"{safe_name}.abc"
                converter.export_abc(str(file_path))

        print(f"Exported {len(self.parts)} parts to {output_dir}/")

    def export_pdf(self, output_path: str, method: str = 'auto', concert_pitch: bool = False) -> bool:
        """
        Export multi-part score to PDF.

        Args:
            output_path: Path for output PDF
            method: Export method ('auto', 'music21', 'verovio', 'basic')
            concert_pitch: Export in concert pitch if True

        Returns:
            True if successful, False otherwise
        """
        from .pdf_export import MultiPartPDFExporter

        exporter = MultiPartPDFExporter()
        return exporter.export_full_score(
            self,
            output_path,
            method=method,
            concert_pitch=concert_pitch
        )

    def export_parts_as_pdf(self, output_dir: str, method: str = 'auto') -> bool:
        """
        Export each part as a separate PDF file.

        Args:
            output_dir: Directory to save PDF files
            method: Export method ('auto', 'music21', 'verovio', 'basic')

        Returns:
            True if all successful, False otherwise
        """
        from .pdf_export import MultiPartPDFExporter

        exporter = MultiPartPDFExporter()
        return exporter.export_parts_as_pdf(self, output_dir, method=method)

    def export_parts_book(self, output_path: str):
        """
        Create a PDF "parts book" with all parts.

        Args:
            output_path: Path for output PDF
        """
        from .pdf_export import MultiPartPDFExporter

        exporter = MultiPartPDFExporter()
        exporter.create_parts_book(self, output_path)

    def export_with_toc(self, output_path: str, include_blank_pages: bool = True):
        """
        Export score with table of contents.

        Args:
            output_path: Path for output PDF
            include_blank_pages: Include blank staff pages for each part
        """
        from .table_of_contents import create_score_with_toc

        # Prepare parts list for TOC
        parts_list = []
        page_num = 3  # Start after title and TOC pages

        for part_name in self.part_order:
            instrument = self.instruments[part_name]
            score = self.parts[part_name]

            parts_list.append({
                'name': part_name,
                'instrument': instrument.name,
                'clef': instrument.clef.value,
                'time_signature': self.time_signature,
                'page': page_num if include_blank_pages else None,
                'measures': len(score.measures)
            })

            if include_blank_pages:
                page_num += 1

        # Create the score
        create_score_with_toc(
            output_path,
            self.title,
            self.composer,
            parts_list,
            include_part_pages=include_blank_pages
        )

    def to_dict(self) -> Dict:
        """Convert multi-part score to dictionary."""
        return {
            'title': self.title,
            'composer': self.composer,
            'time_signature': self.time_signature,
            'key_signature': self.key_signature,
            'tempo': self.tempo,
            'parts': {
                part_name: score.to_dict()
                for part_name, score in self.parts.items()
            },
            'instruments': {
                part_name: {
                    'name': inst.name,
                    'short_name': inst.short_name,
                    'clef': inst.clef.value,
                    'transposition': inst.transposition.name
                }
                for part_name, inst in self.instruments.items()
            },
            'part_order': self.part_order
        }


class ScoreAssembler:
    """Assembles multi-part scores from individual part images."""

    def __init__(self, recognition_system=None):
        """
        Initialize score assembler.

        Args:
            recognition_system: MusicRecognitionSystem instance for recognizing parts
        """
        self.recognition_system = recognition_system

    def create_score_from_parts(
        self,
        part_images: Dict[str, str],
        instruments: Dict[str, InstrumentConfig],
        title: str = "Untitled",
        composer: str = "Unknown"
    ) -> MultiPartScore:
        """
        Create a multi-part score from individual part images.

        Args:
            part_images: Dictionary of part_name -> image_path
            instruments: Dictionary of part_name -> InstrumentConfig
            title: Score title
            composer: Composer name

        Returns:
            MultiPartScore object
        """
        if self.recognition_system is None:
            raise ValueError("Recognition system not provided")

        multi_score = MultiPartScore(title=title, composer=composer)

        print(f"Processing {len(part_images)} parts...")

        for part_name, image_path in part_images.items():
            print(f"  Recognizing: {part_name}")

            # Recognize the part
            part_score = self.recognition_system.recognize(image_path)

            # Get instrument config
            instrument = instruments.get(part_name)
            if instrument is None:
                raise ValueError(f"No instrument configuration for part: {part_name}")

            # Add to multi-part score
            multi_score.add_part(part_name, part_score, instrument)

        print("All parts processed!")
        return multi_score

    @staticmethod
    def create_standard_ensemble_score(
        ensemble_type: str = "concert_band",
        title: str = "Untitled",
        composer: str = "Unknown"
    ) -> MultiPartScore:
        """
        Create an empty multi-part score for a standard ensemble.

        Args:
            ensemble_type: Type of ensemble ('concert_band', 'brass_ensemble', etc.)
            title: Score title
            composer: Composer name

        Returns:
            Empty MultiPartScore with all parts configured
        """
        multi_score = MultiPartScore(title=title, composer=composer)

        # Get ensemble configuration
        if ensemble_type == "concert_band":
            instruments = StandardEnsembles.CONCERT_BAND
        elif ensemble_type == "full_concert_band":
            instruments = StandardEnsembles.FULL_CONCERT_BAND
        elif ensemble_type == "brass_ensemble":
            instruments = StandardEnsembles.BRASS_ENSEMBLE
        elif ensemble_type == "woodwind_quintet":
            instruments = StandardEnsembles.WOODWIND_QUINTET
        else:
            raise ValueError(f"Unknown ensemble type: {ensemble_type}")

        # Add all parts with empty scores
        for instrument in instruments:
            empty_score = MusicScore()
            empty_score.clef = instrument.clef.value
            multi_score.add_part(instrument.name, empty_score, instrument)

        return multi_score
