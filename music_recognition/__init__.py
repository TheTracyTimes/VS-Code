"""
Handwritten Music Recognition System
An AI-powered OMR system for digitizing handwritten music notation.
"""

from .system import MusicRecognitionSystem
from .multipart_score import MultiPartScore, ScoreAssembler
from .instruments import (
    InstrumentConfig,
    BandInstruments,
    StandardEnsembles,
    get_instrument_by_name,
    list_all_instruments
)
from .transposition import (
    Transposer,
    ScoreTransposer,
    Note,
    transpose_pitch_string,
    transpose_octaves,
    transpose_measure_octaves,
    transpose_score_octaves
)
from .pdf_export import (
    PDFExporter,
    ScorePDFExporter,
    MultiPartPDFExporter,
    export_score_to_pdf,
    check_pdf_backends
)
from .staff_paper import (
    StaffPaperGenerator,
    create_blank_sheet,
    create_instrument_part
)
from .table_of_contents import (
    TableOfContentsGenerator,
    create_score_with_toc
)
from .score_layout import (
    AlignedScoreLayout,
    SongCollectionLayout,
    create_full_score_book,
    create_song_collection
)
from .pdf_reader import PDFMusicReader
from .part_generator import (
    PartMerger,
    PartGenerator,
    AutoScoreBuilder
)
from .title_extraction import (
    TitleExtractor,
    PartSplitter,
    extract_titles_from_pdf
)
from .individual_books import (
    IndividualBookGenerator,
    create_individual_books_from_score
)
from .song_extraction import (
    SongExtractor,
    IndividualSongScoreGenerator,
    extract_songs_and_create_scores
)

__version__ = "0.1.0"
__all__ = [
    "MusicRecognitionSystem",
    "MultiPartScore",
    "ScoreAssembler",
    "InstrumentConfig",
    "BandInstruments",
    "StandardEnsembles",
    "Transposer",
    "ScoreTransposer",
    "Note",
    "transpose_pitch_string",
    "transpose_octaves",
    "transpose_measure_octaves",
    "transpose_score_octaves",
    "get_instrument_by_name",
    "list_all_instruments",
    "PDFExporter",
    "ScorePDFExporter",
    "MultiPartPDFExporter",
    "export_score_to_pdf",
    "check_pdf_backends",
    "StaffPaperGenerator",
    "create_blank_sheet",
    "create_instrument_part",
    "TableOfContentsGenerator",
    "create_score_with_toc",
    "AlignedScoreLayout",
    "SongCollectionLayout",
    "create_full_score_book",
    "create_song_collection",
    "PDFMusicReader",
    "PartMerger",
    "PartGenerator",
    "AutoScoreBuilder",
    "TitleExtractor",
    "PartSplitter",
    "extract_titles_from_pdf",
    "IndividualBookGenerator",
    "create_individual_books_from_score",
    "SongExtractor",
    "IndividualSongScoreGenerator",
    "extract_songs_and_create_scores"
]
