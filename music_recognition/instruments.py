"""
Instrument definitions, transpositions, and ranges for orchestral/band instruments.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from enum import Enum


class ClefType(Enum):
    """Standard musical clefs."""
    TREBLE = "G"
    BASS = "F"
    ALTO = "C"
    TENOR = "C"


class TransposeInterval(Enum):
    """Common transposition intervals."""
    NONE = (0, 0)  # (semitones, octaves)
    Bb_DOWN = (-2, 0)  # Bb instruments (clarinet, trumpet)
    Eb_DOWN = (-9, 0)  # Eb instruments (alto sax)
    F_DOWN = (-7, 0)  # F instruments (French horn)
    Eb_UP = (3, 0)  # Eb instruments (alto sax - alternative)


@dataclass
class InstrumentConfig:
    """Configuration for a musical instrument."""
    name: str
    short_name: str
    clef: ClefType
    transposition: TransposeInterval
    range_low: str  # Lowest note (concert pitch)
    range_high: str  # Highest note (concert pitch)
    staff_lines: int = 5
    part_number: Optional[int] = None


class BandInstruments:
    """Standard concert band instrument configurations."""

    # Woodwinds - C instruments
    C_FLUTE = InstrumentConfig(
        name="C Flute",
        short_name="Fl.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="C4",
        range_high="C7"
    )

    C_PICCOLO = InstrumentConfig(
        name="C Piccolo",
        short_name="Picc.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="C5",
        range_high="C8"
    )

    # Bb Clarinets
    Bb_CLARINET_1 = InstrumentConfig(
        name="1st B♭ Clarinet",
        short_name="Cl. 1",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="D3",
        range_high="C7",
        part_number=1
    )

    Bb_CLARINET_2 = InstrumentConfig(
        name="2nd B♭ Clarinet",
        short_name="Cl. 2",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="D3",
        range_high="C7",
        part_number=2
    )

    Bb_CLARINET_3 = InstrumentConfig(
        name="3rd B♭ Clarinet",
        short_name="Cl. 3",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="D3",
        range_high="C7",
        part_number=3
    )

    Bb_BASS_CLARINET = InstrumentConfig(
        name="B♭ Bass Clarinet",
        short_name="B. Cl.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="D2",
        range_high="F5"
    )

    # Saxophones
    Eb_ALTO_SAX_1 = InstrumentConfig(
        name="1st E♭ Alto Saxophone",
        short_name="A. Sax 1",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Eb_DOWN,
        range_low="D3",
        range_high="A5",
        part_number=1
    )

    Eb_ALTO_SAX_2 = InstrumentConfig(
        name="2nd E♭ Alto Saxophone",
        short_name="A. Sax 2",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Eb_DOWN,
        range_low="D3",
        range_high="A5",
        part_number=2
    )

    Eb_ALTO_SAX_3 = InstrumentConfig(
        name="3rd E♭ Alto Saxophone",
        short_name="A. Sax 3",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Eb_DOWN,
        range_low="D3",
        range_high="A5",
        part_number=3
    )

    Bb_TENOR_SAX = InstrumentConfig(
        name="B♭ Tenor Saxophone",
        short_name="T. Sax",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="A2",
        range_high="E5"
    )

    Eb_BARITONE_SAX = InstrumentConfig(
        name="E♭ Baritone Saxophone",
        short_name="Bari. Sax",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Eb_DOWN,
        range_low="D2",
        range_high="A4"
    )

    # Brass - High
    Bb_TRUMPET_1 = InstrumentConfig(
        name="1st B♭ Trumpet",
        short_name="Tpt. 1",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="E3",
        range_high="C6",
        part_number=1
    )

    Bb_TRUMPET_2 = InstrumentConfig(
        name="2nd B♭ Trumpet",
        short_name="Tpt. 2",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="E3",
        range_high="C6",
        part_number=2
    )

    Bb_TRUMPET_3 = InstrumentConfig(
        name="3rd B♭ Trumpet",
        short_name="Tpt. 3",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="E3",
        range_high="C6",
        part_number=3
    )

    F_FRENCH_HORN_1 = InstrumentConfig(
        name="1st F French Horn",
        short_name="Hn. 1",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.F_DOWN,
        range_low="B2",
        range_high="F5",
        part_number=1
    )

    F_FRENCH_HORN_2 = InstrumentConfig(
        name="2nd F French Horn",
        short_name="Hn. 2",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.F_DOWN,
        range_low="B2",
        range_high="F5",
        part_number=2
    )

    # Low Brass
    C_TROMBONE_1 = InstrumentConfig(
        name="1st C Trombone",
        short_name="Tbn. 1",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="E2",
        range_high="F5",
        part_number=1
    )

    C_TROMBONE_2 = InstrumentConfig(
        name="2nd C Trombone",
        short_name="Tbn. 2",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="E2",
        range_high="F5",
        part_number=2
    )

    C_TROMBONE_3 = InstrumentConfig(
        name="3rd C Trombone",
        short_name="Tbn. 3",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="E2",
        range_high="F5",
        part_number=3
    )

    # Euphonium/Baritone
    C_EUPHONIUM_BC = InstrumentConfig(
        name="Euphonium (Bass Clef)",
        short_name="Euph.",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="E2",
        range_high="B4"
    )

    Bb_BARITONE_TC = InstrumentConfig(
        name="Baritone (Treble Clef)",
        short_name="Bar.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="E2",
        range_high="B4"
    )

    # Tuba
    C_TUBA = InstrumentConfig(
        name="C Tuba",
        short_name="Tuba",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="E1",
        range_high="F4"
    )

    Bb_TUBA = InstrumentConfig(
        name="B♭ Tuba",
        short_name="Tuba",
        clef=ClefType.BASS,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="D1",
        range_high="F4"
    )

    # Percussion (non-transposing)
    PERCUSSION = InstrumentConfig(
        name="Percussion",
        short_name="Perc.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="C3",
        range_high="C6"
    )

    # Orchestral Strings (C instruments)
    VIOLIN = InstrumentConfig(
        name="Violin",
        short_name="Vln.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="G3",
        range_high="A7"
    )

    VIOLA = InstrumentConfig(
        name="Viola",
        short_name="Vla.",
        clef=ClefType.ALTO,
        transposition=TransposeInterval.NONE,
        range_low="C3",
        range_high="E6"
    )

    CELLO = InstrumentConfig(
        name="Cello",
        short_name="Vc.",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="C2",
        range_high="C6"
    )

    # Orchestral Woodwinds
    OBOE = InstrumentConfig(
        name="Oboe",
        short_name="Ob.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="B3",
        range_high="A6"
    )

    BASSOON = InstrumentConfig(
        name="Bassoon",
        short_name="Bsn.",
        clef=ClefType.BASS,
        transposition=TransposeInterval.NONE,
        range_low="B1",
        range_high="E5"
    )

    Bb_SOPRANO_SAX = InstrumentConfig(
        name="B♭ Soprano Saxophone",
        short_name="S. Sax",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Bb_DOWN,
        range_low="A3",
        range_high="E6"
    )

    Eb_ALTO_CLARINET = InstrumentConfig(
        name="E♭ Alto Clarinet",
        short_name="A. Cl.",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.Eb_DOWN,
        range_low="E2",
        range_high="C6"
    )

    # Flute parts (for derived parts)
    C_FLUTE_2 = InstrumentConfig(
        name="2nd C Flute",
        short_name="Fl. 2",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="C4",
        range_high="C7",
        part_number=2
    )

    C_FLUTE_3 = InstrumentConfig(
        name="3rd C Flute",
        short_name="Fl. 3",
        clef=ClefType.TREBLE,
        transposition=TransposeInterval.NONE,
        range_low="C4",
        range_high="C7",
        part_number=3
    )


class StandardEnsembles:
    """Pre-defined ensemble configurations."""

    CONCERT_BAND = [
        BandInstruments.C_FLUTE,
        BandInstruments.Bb_CLARINET_1,
        BandInstruments.Bb_CLARINET_2,
        BandInstruments.Bb_CLARINET_3,
        BandInstruments.Eb_ALTO_SAX_1,
        BandInstruments.Eb_ALTO_SAX_2,
        BandInstruments.Bb_TENOR_SAX,
        BandInstruments.Eb_BARITONE_SAX,
        BandInstruments.Bb_TRUMPET_1,
        BandInstruments.Bb_TRUMPET_2,
        BandInstruments.F_FRENCH_HORN_1,
        BandInstruments.F_FRENCH_HORN_2,
        BandInstruments.C_TROMBONE_1,
        BandInstruments.C_TROMBONE_2,
        BandInstruments.C_EUPHONIUM_BC,
        BandInstruments.C_TUBA,
        BandInstruments.PERCUSSION,
    ]

    FULL_CONCERT_BAND = [
        BandInstruments.C_PICCOLO,
        BandInstruments.C_FLUTE,
        BandInstruments.Bb_CLARINET_1,
        BandInstruments.Bb_CLARINET_2,
        BandInstruments.Bb_CLARINET_3,
        BandInstruments.Bb_BASS_CLARINET,
        BandInstruments.Eb_ALTO_SAX_1,
        BandInstruments.Eb_ALTO_SAX_2,
        BandInstruments.Eb_ALTO_SAX_3,
        BandInstruments.Bb_TENOR_SAX,
        BandInstruments.Eb_BARITONE_SAX,
        BandInstruments.Bb_TRUMPET_1,
        BandInstruments.Bb_TRUMPET_2,
        BandInstruments.Bb_TRUMPET_3,
        BandInstruments.F_FRENCH_HORN_1,
        BandInstruments.F_FRENCH_HORN_2,
        BandInstruments.C_TROMBONE_1,
        BandInstruments.C_TROMBONE_2,
        BandInstruments.C_TROMBONE_3,
        BandInstruments.C_EUPHONIUM_BC,
        BandInstruments.C_TUBA,
        BandInstruments.PERCUSSION,
    ]

    BRASS_ENSEMBLE = [
        BandInstruments.Bb_TRUMPET_1,
        BandInstruments.Bb_TRUMPET_2,
        BandInstruments.F_FRENCH_HORN_1,
        BandInstruments.F_FRENCH_HORN_2,
        BandInstruments.C_TROMBONE_1,
        BandInstruments.C_TROMBONE_2,
        BandInstruments.C_EUPHONIUM_BC,
        BandInstruments.C_TUBA,
    ]

    WOODWIND_QUINTET = [
        BandInstruments.C_FLUTE,
        BandInstruments.Bb_CLARINET_1,
        BandInstruments.Eb_ALTO_SAX_1,
        BandInstruments.Bb_TENOR_SAX,
        BandInstruments.Eb_BARITONE_SAX,
    ]


def get_instrument_by_name(name: str) -> Optional[InstrumentConfig]:
    """
    Get instrument configuration by name.

    Args:
        name: Instrument name (e.g., "1st Bb Clarinet", "Bb_CLARINET_1")

    Returns:
        InstrumentConfig if found, None otherwise
    """
    # Normalize name
    normalized = name.upper().replace(" ", "_").replace("♭", "b").replace("♯", "#")

    # Try to get from BandInstruments
    if hasattr(BandInstruments, normalized):
        return getattr(BandInstruments, normalized)

    # Try partial matching
    for attr_name in dir(BandInstruments):
        if attr_name.startswith('_'):
            continue
        if normalized in attr_name:
            return getattr(BandInstruments, attr_name)

    return None


def list_all_instruments() -> Dict[str, InstrumentConfig]:
    """
    Get all available instrument configurations.

    Returns:
        Dictionary mapping instrument names to configurations
    """
    instruments = {}

    for attr_name in dir(BandInstruments):
        if attr_name.startswith('_'):
            continue

        attr = getattr(BandInstruments, attr_name)
        if isinstance(attr, InstrumentConfig):
            instruments[attr.name] = attr

    return instruments


def print_instrument_list():
    """Print formatted list of all available instruments."""
    instruments = list_all_instruments()

    print("\nAvailable Instruments:")
    print("=" * 60)

    categories = {
        "Flutes": [],
        "Clarinets": [],
        "Saxophones": [],
        "Trumpets": [],
        "Horns": [],
        "Trombones": [],
        "Low Brass": [],
        "Percussion": []
    }

    for name, config in instruments.items():
        if "Flute" in name or "Piccolo" in name:
            categories["Flutes"].append(config)
        elif "Clarinet" in name:
            categories["Clarinets"].append(config)
        elif "Saxophone" in name or "Sax" in name:
            categories["Saxophones"].append(config)
        elif "Trumpet" in name:
            categories["Trumpets"].append(config)
        elif "Horn" in name:
            categories["Horns"].append(config)
        elif "Trombone" in name:
            categories["Trombones"].append(config)
        elif "Baritone" in name or "Euphonium" in name or "Tuba" in name:
            categories["Low Brass"].append(config)
        elif "Percussion" in name:
            categories["Percussion"].append(config)

    for category, insts in categories.items():
        if insts:
            print(f"\n{category}:")
            for inst in insts:
                trans = "Non-transposing" if inst.transposition == TransposeInterval.NONE else f"Transposing: {inst.transposition.name}"
                print(f"  - {inst.name} ({inst.short_name}) - {trans}")
