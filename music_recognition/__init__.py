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
from .transposition import Transposer, ScoreTransposer, Note
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
    "create_score_with_toc"
]
