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
    "list_all_instruments"
]
