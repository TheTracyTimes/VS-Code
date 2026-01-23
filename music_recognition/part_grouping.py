"""
Part grouping for conductor scores.

When multiple instruments play the same music, group them together on the score
with a bracket and combined label to save space and improve readability.

Example:
    Instead of:
        1st Bb Clarinet:  [music staff]
        1st Bb Trumpet:   [same music staff]
        Bb Soprano Sax:   [same music staff]

    Show:
        1st Bb Clarinet  }
        1st Bb Trumpet   } [music staff once]
        Bb Soprano Sax   }
"""

from typing import List, Dict, Tuple, Set
from .postprocessing import MusicScore
from .instruments import InstrumentConfig


class PartGrouper:
    """Groups identical parts together for conductor scores."""

    @staticmethod
    def measures_are_identical(measure1: List[Dict], measure2: List[Dict]) -> bool:
        """
        Check if two measures contain identical music.

        Args:
            measure1: First measure
            measure2: Second measure

        Returns:
            True if measures are identical
        """
        if len(measure1) != len(measure2):
            return False

        for note1, note2 in zip(measure1, measure2):
            # Compare note properties
            if note1.get('type') != note2.get('type'):
                return False
            if note1.get('pitch') != note2.get('pitch'):
                return False
            if note1.get('duration') != note2.get('duration'):
                return False
            # Add more comparisons as needed

        return True

    @staticmethod
    def scores_are_identical(score1: MusicScore, score2: MusicScore) -> bool:
        """
        Check if two scores contain identical music throughout.

        Args:
            score1: First score
            score2: Second score

        Returns:
            True if all measures are identical
        """
        if len(score1.measures) != len(score2.measures):
            return False

        for m1, m2 in zip(score1.measures, score2.measures):
            if not PartGrouper.measures_are_identical(m1, m2):
                return False

        return True

    @staticmethod
    def find_identical_parts(parts: Dict[str, Tuple[MusicScore, InstrumentConfig]]) -> List[List[str]]:
        """
        Find groups of parts that have identical music.

        Args:
            parts: Dictionary of part name to (score, instrument) tuples

        Returns:
            List of groups, where each group is a list of part names with identical music

        Example:
            >>> parts = {
            ...     '1st Bb Clarinet': (score1, inst1),
            ...     '1st Bb Trumpet': (score1, inst2),  # Same as clarinet
            ...     'Bb Soprano Sax': (score1, inst3),  # Same as clarinet
            ...     '2nd Bb Clarinet': (score2, inst4),
            ... }
            >>> find_identical_parts(parts)
            [['1st Bb Clarinet', '1st Bb Trumpet', 'Bb Soprano Sax'], ['2nd Bb Clarinet']]
        """
        part_names = list(parts.keys())
        groups = []
        processed = set()

        for i, name1 in enumerate(part_names):
            if name1 in processed:
                continue

            # Start a new group
            group = [name1]
            score1 = parts[name1][0]

            # Find all other parts with identical music
            for j, name2 in enumerate(part_names[i+1:], start=i+1):
                if name2 in processed:
                    continue

                score2 = parts[name2][0]

                if PartGrouper.scores_are_identical(score1, score2):
                    group.append(name2)
                    processed.add(name2)

            groups.append(group)
            processed.add(name1)

        return groups

    @staticmethod
    def create_grouped_score_layout(parts: Dict[str, Tuple[MusicScore, InstrumentConfig]]) -> Dict[str, any]:
        """
        Create a score layout with grouped identical parts.

        Args:
            parts: Dictionary of part name to (score, instrument) tuples

        Returns:
            Dictionary with grouped layout information

        Structure:
            {
                'groups': [
                    {
                        'label': '1st Bb Clarinet/1st Bb Trumpet/Bb Soprano Sax',
                        'part_names': ['1st Bb Clarinet', '1st Bb Trumpet', 'Bb Soprano Sax'],
                        'score': MusicScore,
                        'instrument': InstrumentConfig
                    },
                    ...
                ]
            }
        """
        groups = PartGrouper.find_identical_parts(parts)

        grouped_layout = {
            'groups': []
        }

        for group in groups:
            if len(group) == 1:
                # Single part, no grouping needed
                part_name = group[0]
                score, instrument = parts[part_name]
                grouped_layout['groups'].append({
                    'label': part_name,
                    'part_names': [part_name],
                    'score': score,
                    'instrument': instrument,
                    'is_grouped': False
                })
            else:
                # Multiple identical parts - group them
                combined_label = '/'.join(group)
                # Use the first part's score and instrument as representative
                score, instrument = parts[group[0]]
                grouped_layout['groups'].append({
                    'label': combined_label,
                    'part_names': group,
                    'score': score,
                    'instrument': instrument,
                    'is_grouped': True
                })

        return grouped_layout


class GroupedScoreExporter:
    """Export conductor scores with grouped identical parts."""

    def __init__(self):
        """Initialize grouped score exporter."""
        self.grouper = PartGrouper()

    def export_grouped_conductor_score(self, multipart_score: 'MultiPartScore',
                                       output_path: str,
                                       group_identical: bool = True) -> str:
        """
        Export a conductor score with grouped identical parts.

        Args:
            multipart_score: MultiPartScore to export
            output_path: Path for output PDF
            group_identical: Whether to group identical parts (default: True)

        Returns:
            Path to exported PDF

        Example usage:
            >>> exporter = GroupedScoreExporter()
            >>> exporter.export_grouped_conductor_score(
            ...     complete_score,
            ...     'conductor_score.pdf',
            ...     group_identical=True
            ... )
            # Creates score with grouped parts:
            # "1st Bb Clarinet/1st Bb Trumpet/Bb Soprano Sax" [music shown once]
            # "2nd Bb Clarinet/2nd Bb Trumpet" [music shown once]
            # etc.
        """
        if not group_identical:
            # Export normally without grouping
            multipart_score.export_full_score_book(output_path)
            return output_path

        # Find grouped parts
        layout = self.grouper.create_grouped_score_layout(multipart_score.parts)

        # Create a new MultiPartScore with grouped parts
        from .multipart_score import MultiPartScore

        grouped_score = MultiPartScore(
            title=multipart_score.title,
            composer=multipart_score.composer
        )

        # Add each group as a single part
        for group_info in layout['groups']:
            label = group_info['label']
            score = group_info['score']
            instrument = group_info['instrument']

            grouped_score.add_part(label, score, instrument)

        # Export the grouped score
        grouped_score.export_full_score_book(
            output_path,
            num_pages=50,
            measures_per_system=4,
            systems_per_page=3
        )

        # Print summary
        print(f"\n✓ Created grouped conductor score: {output_path}")
        if group_identical:
            original_count = len(multipart_score.parts)
            grouped_count = len(layout['groups'])
            saved = original_count - grouped_count
            print(f"  Grouped {original_count} parts into {grouped_count} staves")
            print(f"  Saved {saved} staves by grouping identical parts")

            # Show groupings
            for group_info in layout['groups']:
                if group_info['is_grouped']:
                    print(f"  • {group_info['label']}")

        return output_path


def create_grouped_conductor_score(multipart_score: 'MultiPartScore',
                                   output_path: str = 'conductor_score.pdf',
                                   group_identical: bool = True) -> str:
    """
    Main function to create a conductor score with grouped identical parts.

    Args:
        multipart_score: MultiPartScore to export
        output_path: Path for output PDF
        group_identical: Whether to group identical parts

    Returns:
        Path to exported PDF

    Example:
        >>> from music_recognition import create_grouped_conductor_score
        >>>
        >>> # After creating your complete score
        >>> create_grouped_conductor_score(
        ...     complete_score,
        ...     'output/conductor_score.pdf',
        ...     group_identical=True
        ... )
        #
        # Instead of 22+ separate staves, you'll get maybe 15-18 staves with:
        # - "1st Bb Clarinet/1st Bb Trumpet/Bb Soprano Sax" (1 staff)
        # - "2nd Bb Clarinet/2nd Bb Trumpet" (1 staff)
        # - "3rd Bb Clarinet/3rd Bb Trumpet/Bb Tenor Sax" (1 staff)
        # - "Baritone T.C./Bb Bass Clarinet" (1 staff)
        # - "Eb Alto Sax 3/Alto Clarinet" (1 staff)
        # - "Cello/Trombone 1" (1 staff)
        # - "Bassoon/Trombone 2" (1 staff)
        # - "Oboe/Flute 2" (1 staff)
        # - "Viola/Flute 3" (1 staff, but different octave)
        # etc.
    """
    exporter = GroupedScoreExporter()
    return exporter.export_grouped_conductor_score(multipart_score, output_path, group_identical)
