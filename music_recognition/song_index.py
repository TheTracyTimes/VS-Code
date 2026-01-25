"""
Song Index Management for music collections.

This module helps organize and manage song collections with:
1. Song metadata (title, number, measure boundaries)
2. Alphabetical and numerical indexes
3. Integration with song extraction workflow
4. JSON import/export for song databases
"""

from typing import List, Dict, Optional
from pathlib import Path
import json


class SongIndex:
    """Manages a table of contents / index for a music collection."""

    def __init__(self):
        """Initialize song index."""
        self.songs = []

    def add_song(self, title: str, number: str,
                 start_measure: Optional[int] = None,
                 end_measure: Optional[int] = None,
                 composer: Optional[str] = None):
        """
        Add a song to the index.

        Args:
            title: Song title (e.g., "Hallelujah, I'm Going Home")
            number: Song number in collection (e.g., "003", "001-061")
            start_measure: Optional starting measure in the full score
            end_measure: Optional ending measure in the full score
            composer: Optional composer name
        """
        song_entry = {
            'title': title,
            'number': number,
            'start_measure': start_measure,
            'end_measure': end_measure,
            'composer': composer
        }
        self.songs.append(song_entry)

    def load_from_dict(self, songs_data: List[Dict]):
        """
        Load songs from a list of dictionaries.

        Args:
            songs_data: List of song dictionaries

        Example:
            >>> index = SongIndex()
            >>> index.load_from_dict([
            ...     {'title': 'Goodbye, World, Goodbye', 'number': '004'},
            ...     {'title': 'Extol His Holy Name', 'number': '005'},
            ... ])
        """
        self.songs = songs_data

    def load_from_json(self, json_path: str):
        """
        Load song index from JSON file.

        Args:
            json_path: Path to JSON file with song data

        JSON Format:
            [
                {
                    "title": "Hallelujah, I'm Going Home",
                    "number": "003",
                    "start_measure": 0,
                    "end_measure": 32
                },
                ...
            ]
        """
        with open(json_path, 'r') as f:
            self.songs = json.load(f)

    def save_to_json(self, json_path: str):
        """
        Save song index to JSON file.

        Args:
            json_path: Path to save JSON file
        """
        with open(json_path, 'w') as f:
            json.dump(self.songs, f, indent=2)

    def get_song_by_number(self, number: str) -> Optional[Dict]:
        """
        Get song data by its number.

        Args:
            number: Song number (e.g., "003")

        Returns:
            Song dictionary or None if not found
        """
        for song in self.songs:
            if song['number'] == number:
                return song
        return None

    def get_song_by_title(self, title: str) -> Optional[Dict]:
        """
        Get song data by its title (case-insensitive).

        Args:
            title: Song title

        Returns:
            Song dictionary or None if not found
        """
        title_lower = title.lower()
        for song in self.songs:
            if song['title'].lower() == title_lower:
                return song
        return None

    def get_songs_for_extraction(self) -> List[Dict]:
        """
        Get list of songs formatted for song extraction.

        Returns:
            List of dictionaries with 'title', 'start_measure', 'end_measure'
            Only includes songs that have measure boundaries defined.

        Example:
            >>> index = SongIndex()
            >>> # ... load songs with measure data ...
            >>> song_list = index.get_songs_for_extraction()
            >>> # Use with extract_songs_and_create_scores()
        """
        extraction_list = []

        for song in self.songs:
            if song.get('start_measure') is not None and song.get('end_measure') is not None:
                extraction_list.append({
                    'title': song['title'],
                    'start_measure': song['start_measure'],
                    'end_measure': song['end_measure']
                })

        return extraction_list

    def generate_alphabetical_index(self) -> str:
        """
        Generate a formatted alphabetical index (like a table of contents).

        Returns:
            Formatted string with alphabetical song listing
        """
        # Sort songs by title
        sorted_songs = sorted(self.songs, key=lambda x: x['title'])

        output = "TABLE OF CONTENTS - ALPHABETICAL\n"
        output += "=" * 70 + "\n\n"

        current_letter = ''

        for song in sorted_songs:
            # Get first letter
            first_letter = song['title'][0].upper()

            # Print letter header if new letter
            if first_letter != current_letter:
                current_letter = first_letter
                output += f"\n--- {current_letter} ---\n"

            # Format: "003. Hallelujah, I'm Going Home"
            number = song['number'].rjust(3)
            output += f"{number}. {song['title']}\n"

        return output

    def generate_numerical_index(self) -> str:
        """
        Generate a formatted numerical index (ordered by song number).

        Returns:
            Formatted string with numerical song listing
        """
        # Sort by number (convert to int for proper sorting)
        def get_sort_key(song):
            try:
                # Handle ranges like "001-061"
                num_str = song['number'].split('-')[0]
                return int(num_str)
            except:
                return 0

        sorted_songs = sorted(self.songs, key=get_sort_key)

        output = "TABLE OF CONTENTS - NUMERICAL ORDER\n"
        output += "=" * 70 + "\n\n"

        for song in sorted_songs:
            number = song['number'].rjust(3)
            output += f"{number}. {song['title']}\n"

        return output

    def update_measure_boundaries(self, measure_map: Dict[str, Dict[str, int]]):
        """
        Update measure boundaries for songs.

        Args:
            measure_map: Dictionary mapping song numbers to {'start': X, 'end': Y}

        Example:
            >>> index = SongIndex()
            >>> # ... load songs ...
            >>> index.update_measure_boundaries({
            ...     '003': {'start': 0, 'end': 32},
            ...     '004': {'start': 33, 'end': 64},
            ... })
        """
        for song in self.songs:
            number = song['number']
            if number in measure_map:
                song['start_measure'] = measure_map[number]['start']
                song['end_measure'] = measure_map[number]['end']

    def count(self) -> int:
        """Get total number of songs in index."""
        return len(self.songs)


def create_god_of_mercy_church_band_index() -> SongIndex:
    """
    Create song index from the God of Mercy Church Band hymnal.

    This index contains 125+ songs from the user's table of contents.

    Returns:
        SongIndex with all songs from the collection
    """
    index = SongIndex()

    # Songs from the God of Mercy Church Band table of contents
    # Organized alphabetically as provided
    songs_data = [
        {'title': 'Make me an Instrument', 'number': '001'},
        {'title': 'Thanks To Him', 'number': '002'},
        {'title': 'I Love Him Too Much', 'number': '002'},
        {'title': 'Crown Him King', 'number': '003'},
        {'title': 'Hallelujah, I\'m Going Home', 'number': '003'},
        {'title': 'Goodbye, World, Goodbye', 'number': '004'},
        {'title': 'Make Somebody Glad', 'number': '005'},
        {'title': 'Extol His Holy Name', 'number': '005'},
        {'title': 'A River Shall Flow in the Desert', 'number': '006'},
        {'title': 'There is a River', 'number': '006'},
        {'title': 'Victory', 'number': '007'},
        {'title': 'Take off Your Shoes', 'number': '007'},
        {'title': 'Now I Have Everything', 'number': '008'},
        {'title': 'Fill my Cup, Lord', 'number': '009'},
        {'title': 'Just a Touch from The Lord', 'number': '009'},
        {'title': 'He\'s So Good', 'number': '009'},
        {'title': 'Someone is Praying for You', 'number': '010'},
        {'title': 'Help me, Lord, To Be Willing', 'number': '010'},
        {'title': 'Not my Will, Thine Be Done', 'number': '010'},
        {'title': 'I\'m Standing on the Solid Rock', 'number': '011'},
        {'title': 'A Better Way', 'number': '012'},
        {'title': 'There\'s a New Day', 'number': '012'},
        {'title': 'He\'s Given Life to You', 'number': '013'},
        {'title': 'God\'s Ministry', 'number': '013'},
        {'title': 'Our God Reigns', 'number': '014'},
        {'title': 'Majesty', 'number': '014'},
        {'title': 'All in the Name of Jesus', 'number': '015'},
        {'title': 'Touching Jesus', 'number': '015'},
        {'title': 'The Next Step', 'number': '016'},
        {'title': 'Jesus, Our High Priest', 'number': '016'},
        {'title': 'He is Mine Forever', 'number': '017'},
        {'title': 'I\'m Rejoicing', 'number': '018'},
        {'title': 'On The Solid Rock', 'number': '018'},
        {'title': 'Moving up to Gloryland', 'number': '019'},
        {'title': 'Praise The Lord, I\'m One of Them', 'number': '019'},
        {'title': 'Dig Deep and Strike the Rock', 'number': '020'},
        {'title': 'The Coming of The Lord', 'number': '020'},
        {'title': 'I Feel Healing in my Soul', 'number': '020'},
        {'title': 'You\'ve Got to Keep Walking', 'number': '021'},
        {'title': 'Savior Guide Me', 'number': '021'},
        {'title': 'When Jesus Shall Come Again', 'number': '022'},
        {'title': 'My Friend Divine', 'number': '022'},
        {'title': 'I\'m Going up', 'number': '023'},
        {'title': 'He Paid a Debt', 'number': '023'},
        {'title': 'The Old-Fashioned Meeting', 'number': '024'},
        {'title': 'He\'s Everything to Me', 'number': '024'},
        {'title': 'There\'s Something about That Name', 'number': '025'},
        {'title': 'His Name is Wonderful', 'number': '025'},
        {'title': 'Praise, Praise, Praise', 'number': '025'},
        {'title': 'There is a Purpose for Everything', 'number': '026'},
        {'title': 'Nothing is Impossible With God', 'number': '026'},
        {'title': 'Have Faith in God', 'number': '027'},
        {'title': 'Jesus is the Sweetest Name I Know', 'number': '027'},
        {'title': 'O For a Thousand Tongues', 'number': '028'},
        {'title': 'It Will Rain Again', 'number': '028'},
        {'title': 'Because of Him', 'number': '029'},
        {'title': 'More of You', 'number': '029'},
        {'title': 'Tears are a Language', 'number': '030'},
        {'title': 'Holy Ground', 'number': '030'},
        {'title': 'Emmanuel', 'number': '031'},
        {'title': 'Psalm 42', 'number': '031'},
        {'title': 'Jesus is Coming Soon', 'number': '031'},
        {'title': 'I\'m Too Near Home', 'number': '032'},
        {'title': 'I Want my Life to Count for God', 'number': '032'},
        {'title': 'Help Others', 'number': '033'},
        {'title': 'Somebody Prayed for Me', 'number': '033'},
        {'title': 'Shout and Sing His Praise', 'number': '034'},
        {'title': 'I\'ve Been on the Mountain', 'number': '034'},
        {'title': 'Blow Your Trumpet, Gabriel', 'number': '035'},
        {'title': 'The Sunlight of Love', 'number': '035'},
        {'title': 'Til The Storm Passes By', 'number': '036'},
        {'title': 'He Touched Me', 'number': '036'},
        {'title': 'Love', 'number': '037'},
        {'title': 'Redeeming Love', 'number': '037'},
        {'title': 'The Joy of Heaven', 'number': '038'},
        {'title': 'Let\'s Just Praise The Lord', 'number': '038'},
        {'title': 'Feeling at Home', 'number': '039'},
        {'title': 'The Lighthouse', 'number': '039'},
        {'title': 'Grace to Overcome', 'number': '040'},
        {'title': 'It Will be Worth it All', 'number': '040'},
        {'title': 'All Hail King Jesus', 'number': '041'},
        {'title': 'I Could Never Outlove The Lord', 'number': '041'},
        {'title': 'I Wouldn\'t Give What I Have', 'number': '041'},
        {'title': 'Soon and Very Soon', 'number': '042'},
        {'title': 'Just a Touch from You, Lord', 'number': '042'},
        {'title': 'I Will Serve Thee', 'number': '042'},
        {'title': 'What a Lovely Name', 'number': '043'},
        {'title': 'Only Jesus Can Satisfy Your Soul', 'number': '043'},
        {'title': 'I Lift my Hands', 'number': '044'},
        {'title': 'Jesus, We Just Want to Thank You', 'number': '044'},
        {'title': 'The Blood Will Never Lose its Power', 'number': '044'},
        {'title': 'Breathe on Me', 'number': '045'},
        {'title': 'Jesus is Lord of All', 'number': '045'},
        {'title': 'Just a Closer Walk with Thee', 'number': '045'},
        {'title': 'Gentle Shepherd', 'number': '046'},
        {'title': 'Shepherd of Love', 'number': '046'},
        {'title': 'Canaanland is Just in Sight', 'number': '047'},
        {'title': 'Not a Shadow of Turning', 'number': '047'},
        {'title': 'Teach Me, Lord, To Wait', 'number': '048'},
        {'title': 'Jesus I\'ll Praise You Forever', 'number': '048'},
        {'title': 'Joy - Bells', 'number': '049'},
        {'title': 'Looking for a City', 'number': '049'},
        {'title': 'Crown Him Lord of All', 'number': '050'},
        {'title': 'I am Seeking a City', 'number': '050'},
        {'title': 'Jesus, Hold my Hand', 'number': '051'},
        {'title': 'To God Be The Glory', 'number': '051'},
        {'title': 'Break Me Lord', 'number': '052'},
        {'title': 'Touch me Again, Lord', 'number': '052'},
        {'title': 'In His Presence there is Fullness of Joy', 'number': '052'},
        {'title': 'Let The Temple Be Filled with His Glory', 'number': '053-109'},
        {'title': 'Not my Will, Lord', 'number': '053'},
        {'title': 'Surely The Presence of The Lord Is in This Place', 'number': '053'},
        {'title': 'Just Like Our Mother', 'number': '054'},
        {'title': 'He\'ll Make a Way', 'number': '054'},
        {'title': 'Someone To Care', 'number': '055'},
        {'title': 'Something Beautiful', 'number': '055'},
        {'title': 'Through The Ages', 'number': '056'},
        {'title': 'Sheltered in The Arms of God', 'number': '057'},
        {'title': 'He\'s The Savior of my Soul', 'number': '058-111'},
        {'title': 'The Way That He Loves', 'number': '058'},
        {'title': 'PraiseThe Name of Jesus', 'number': '058'},
        {'title': 'What a Day That Will Be', 'number': '059'},
        {'title': 'Where Could I Go?', 'number': '027'},
        {'title': 'Where No One Stands Alone', 'number': '059'},
        {'title': 'The Family of God', 'number': '060'},
        {'title': 'Learning to Lean', 'number': '060'},
        {'title': 'Consider the Lilies', 'number': '001-061'},
        {'title': 'I Love You Lord', 'number': '061'},
        {'title': 'If That isn\'t Love', 'number': '062'},
        {'title': 'Remind Me, Dear Lord', 'number': '062'},
        {'title': 'Let me Touch Him', 'number': '063'},
        {'title': 'He Looked Beyond My Fault', 'number': '063'},
        {'title': 'I Have Found a Resting Place', 'number': '064'},
        {'title': 'Love Can Be Our Guide', 'number': '064'},
        {'title': 'Give me the Old-Fashioned Way', 'number': '065'},
        {'title': 'Heaven Bound', 'number': '065'},
        {'title': 'Just Over in the Gloryland', 'number': '066'},
        {'title': 'Inside the Gate', 'number': '066'},
        {'title': 'Keep on the Firing Line', 'number': '067'},
        {'title': 'Just a Little Talk with Jesus', 'number': '067'},
        {'title': 'Because He Lives', 'number': '068'},
        {'title': 'Blessed Assurance', 'number': '068'},
        {'title': 'His Eye is on the Sparrow', 'number': '069'},
        {'title': 'Peace in The Valley', 'number': '069'},
        {'title': 'O The Glory Did Roll', 'number': '070'},
        {'title': 'I Want Jesus more than Anything', 'number': '070'},
        {'title': 'Victory March', 'number': '071'},
        {'title': 'I\'m Telling the World about His Love', 'number': '071'},
        {'title': 'Praise Him', 'number': '072'},
        {'title': 'Thank You Lord', 'number': '072-108'},
        {'title': 'Pass Me Not', 'number': '073'},
        {'title': 'Who Am I?', 'number': '073'},
        {'title': 'Chosen in God', 'number': '074'},
        {'title': 'Mansion Over the Hilltop', 'number': '074'},
        {'title': 'Whatever It Takes', 'number': '075'},
        {'title': 'What Would I Do Without Jesus', 'number': '075'},
        {'title': 'God\'s Choosing a People', 'number': '076'},
        {'title': 'Sweet Home of The Soul', 'number': '076-112'},
        {'title': 'Each Step I Take', 'number': '077'},
        {'title': 'It is Well with my Soul', 'number': '077'},
        {'title': 'He is Here', 'number': '078'},
        {'title': 'I Fell in Love with Jesus', 'number': '078'},
        {'title': 'I am Free', 'number': '079'},
        {'title': 'I\'m Free', 'number': '079'},
        {'title': 'This is The Day', 'number': '080'},
        {'title': 'O How I Love Jesus', 'number': '080'},
        {'title': 'The Love of God', 'number': '081'},
        {'title': 'No Name Has Meant so much to Me', 'number': '081'},
        {'title': 'I Know The Lord will Make a way', 'number': '082'},
        {'title': 'Great is Thy Faithfulness', 'number': '082'},
        {'title': 'Endless Joy is Waiting', 'number': '083'},
        {'title': 'I\'ve Got a Wonderful Feeling', 'number': '083'},
        {'title': 'Pity The Man', 'number': '084'},
        {'title': 'He Knows Just What I Need', 'number': '085'},
        {'title': 'I Will Enter His Gates with Thanksgiving', 'number': '085'},
        {'title': 'I\'m a Child of The King', 'number': '086'},
        {'title': 'It is No Secret', 'number': '086'},
        {'title': 'Lord, Fill me with Your Spirit', 'number': '086'},
        {'title': 'A Broken Heart I Gave', 'number': '087'},
        {'title': 'He', 'number': '087'},
        {'title': 'Holy Spirit, Fall on Me', 'number': '087'},
        {'title': 'Sweet Jesus', 'number': '088'},
        {'title': 'How Sweet is the Anointing', 'number': '088'},
        {'title': 'I Never Knew Love \'til I met Him', 'number': '088'},
        {'title': 'Family of a Different Kind', 'number': '089'},
        {'title': 'There\'s a Place, Lord I\'m Longing for in Thee', 'number': '089'},
        {'title': 'Sing Glad Praises', 'number': '090'},
        {'title': 'I\'ve Never Seen the Righteous Forsaken', 'number': '090'},
        {'title': 'I Just Feel Like Something Good is About to Happen', 'number': '091'},
        {'title': 'I\'m Bound for the Kingdom', 'number': '091'},
        {'title': 'Down on my Knees', 'number': '092'},
        {'title': 'Heaven\'s Really Gonna Shine', 'number': '092'},
        {'title': 'Sailing On', 'number': '093'},
        {'title': 'Good News', 'number': '093'},
        {'title': 'Let us Sing', 'number': '094'},
        {'title': 'What Love', 'number': '094'},
        {'title': 'My Savior Leads me All The Way', 'number': '095'},
        {'title': 'Give the World a Smile', 'number': '095'},
        {'title': 'Be an Overcomer', 'number': '096'},
        {'title': 'The Gloryland Way', 'number': '096'},
        {'title': 'I\'m Heaven Bound', 'number': '096'},
        {'title': 'I Want to be Ready to Meet Him', 'number': '097'},
        {'title': 'Higher Ground', 'number': '097'},
        {'title': 'Just a Little While', 'number': '098'},
        {'title': 'There is Power in the Blood', 'number': '098'},
        {'title': 'Behold the Lamb', 'number': '099'},
        {'title': 'This Secret I Will Tell You', 'number': '099'},
        {'title': 'Great is The Lord', 'number': '100'},
        {'title': 'The Name of Jesus', 'number': '100'},
        {'title': 'Without Him', 'number': '101-117'},
        {'title': 'I\'ve Found a People', 'number': '101'},
        {'title': 'I Will Stay in the Vine', 'number': '102'},
        {'title': 'I See the Cloud Arising', 'number': '102'},
        {'title': 'He\'s My King', 'number': '103'},
        {'title': 'He Spoke to Me', 'number': '103'},
        {'title': 'Glory, I\'m Saved', 'number': '104'},
        {'title': 'He Hideth my Soul', 'number': '104'},
        {'title': 'I\'m Moving on', 'number': '104'},
        {'title': 'His Grace is Sufficient for Me', 'number': '105'},
        {'title': 'Where Would I Be', 'number': '105'},
        {'title': 'Wonderful Story of Love', 'number': '105'},
        {'title': 'The Longer I Serve Him', 'number': '106-123'},
        {'title': 'Alleluia', 'number': '106'},
        {'title': 'How Long Has it Been?', 'number': '106'},
        {'title': 'To Have a Heart That\'s Pure', 'number': '107'},
        {'title': 'Touch Him Now', 'number': '107'},
        {'title': 'It\'s My Desire', 'number': '107'},
        {'title': 'His Name is Higher', 'number': '108'},
        {'title': 'How Great Thou Art', 'number': '108'},
        {'title': 'He\'s All I Need', 'number': '109-119'},
        {'title': 'I Feel Like Traveling On', 'number': '109'},
        {'title': 'My Tribute', 'number': '110'},
        {'title': 'I\'ll Fly Away', 'number': '111'},
        {'title': 'When We All Get to Heaven', 'number': '111'},
        {'title': 'The Blood Bought, The Church', 'number': '112'},
        {'title': 'Blessed Redeemer', 'number': '113'},
        {'title': 'Getting Used to the Family of God', 'number': '113'},
        {'title': 'King of Kings', 'number': '113'},
        {'title': 'O My Lord What a Time', 'number': '114'},
        {'title': 'Above Every Name', 'number': '115'},
        {'title': 'Only The Redeemed', 'number': '115'},
        {'title': 'I am so Thankful', 'number': '116'},
        {'title': 'I Thank You, Lord', 'number': '116'},
        {'title': 'I Know Who Holds Tomorrow', 'number': '117'},
        {'title': 'Ten Thousand Years', 'number': '118'},
        {'title': 'I\'ll Keep Holding on to Jesus', 'number': '118'},
        {'title': 'He Is Lord', 'number': '119'},
        {'title': 'I Will Bless Thee, O Lord', 'number': '119'},
        {'title': 'Enter into His Gates', 'number': '120'},
        {'title': 'We Worship You', 'number': '120'},
        {'title': 'Lord, I\'m Hungry and I\'m Thirsty', 'number': '120'},
        {'title': 'Restore My Soul', 'number': '121'},
        {'title': 'Jesus is in This Place', 'number': '121'},
        {'title': 'Oh It is Jesus', 'number': '121'},
        {'title': 'We Have Come into His House', 'number': '122'},
        {'title': 'Sanctuary', 'number': '122'},
        {'title': 'Nowhere Else', 'number': '122'},
        {'title': 'El Shaddai', 'number': '123'},
        {'title': 'By the Grace of God', 'number': '123'},
        {'title': 'I Know He Heard my Prayer', 'number': '124'},
        {'title': 'I Exalt Thee', 'number': '124'},
        {'title': 'Blessed His Holy Name', 'number': '125'},
        {'title': 'Sing me a Song', 'number': '125'},
        {'title': 'Make me Willing', 'number': '008-017'},
    ]

    index.load_from_dict(songs_data)

    return index


# Example usage
if __name__ == '__main__':
    # Create the index from God of Mercy Church Band hymnal
    index = create_god_of_mercy_church_band_index()

    print(f"Loaded {index.count()} songs from God of Mercy Church Band Hymnal")

    # Generate alphabetical index
    print("\n" + index.generate_alphabetical_index())

    # Generate numerical index
    print("\n" + index.generate_numerical_index())

    # Save to JSON for later use
    index.save_to_json('god_of_mercy_songs.json')
    print("\n✓ Saved to god_of_mercy_songs.json")

    # Example: Look up a song
    song = index.get_song_by_title("Hallelujah, I'm Going Home")
    if song:
        print(f"\nFound song: {song['title']} (#{song['number']})")
