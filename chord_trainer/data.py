"""Chord progressions and song data."""

from dataclasses import dataclass


@dataclass
class Progression:
    """A chord progression pattern."""
    name: str
    description: str
    chords: list[str]
    numerals: str


@dataclass
class Song:
    """A song with its chord progression."""
    title: str
    artist: str
    chords: list[str]


# ============================================================================
# PROGRESSIONS
# ============================================================================

PROGRESSIONS: dict[str, Progression] = {
    "pop": Progression(
        name="Pop",
        description="I-V-vi-IV - The most common pop progression",
        chords=["G", "D", "Em", "C"],
        numerals="I → V → vi → IV",
    ),
    "rock": Progression(
        name="Rock",
        description="I-IV-V-I - Classic rock & roll",
        chords=["G", "C", "D", "G"],
        numerals="I → IV → V → I",
    ),
    "blues": Progression(
        name="Blues",
        description="12-bar blues in A",
        chords=["A", "A", "A", "A", "D", "D", "A", "A", "E", "D", "A", "E"],
        numerals="I-I-I-I-IV-IV-I-I-V-IV-I-V",
    ),
    "sad": Progression(
        name="Sad",
        description="vi-IV-I-V - Emotional minor feel",
        chords=["Am", "F", "C", "G"],
        numerals="vi → IV → I → V",
    ),
    "jazz": Progression(
        name="Jazz",
        description="ii-V-I - The most common jazz progression",
        chords=["Dm7", "G7", "Cmaj7"],
        numerals="ii → V → I",
    ),
    "folk": Progression(
        name="Folk",
        description="I-IV-I-V - Simple folk pattern",
        chords=["G", "C", "G", "D"],
        numerals="I → IV → I → V",
    ),
    "doowop": Progression(
        name="Doo-Wop",
        description="I-vi-IV-V - 50s progression",
        chords=["C", "Am", "F", "G"],
        numerals="I → vi → IV → V",
    ),
    "andalusian": Progression(
        name="Andalusian",
        description="i-VII-VI-V - Spanish/flamenco cadence",
        chords=["Am", "G", "F", "E"],
        numerals="i → VII → VI → V",
    ),
}


# ============================================================================
# SONGS (100 Popular Songs)
# ============================================================================

SONGS: list[Song] = [
    # ---- Original 10 ----
    Song("Wonderwall", "Oasis", ["Em", "G", "D", "A"]),
    Song("Horse With No Name", "America", ["Em", "D6/9"]),
    Song("Knockin' on Heaven's Door", "Bob Dylan", ["G", "D", "Am", "C"]),
    Song("Let It Be", "Beatles", ["C", "G", "Am", "F"]),
    Song("No Woman No Cry", "Bob Marley", ["C", "G", "Am", "F"]),
    Song("Leaving on a Jet Plane", "John Denver", ["G", "C", "D"]),
    Song("Brown Eyed Girl", "Van Morrison", ["G", "C", "G", "D"]),
    Song("Sweet Home Alabama", "Lynyrd Skynyrd", ["D", "C", "G"]),
    Song("Wish You Were Here", "Pink Floyd", ["Em", "G", "A7", "Em"]),
    Song("Three Little Birds", "Bob Marley", ["A", "D", "E"]),

    # ---- Classic Rock ----
    Song("Free Fallin'", "Tom Petty", ["D", "G", "A"]),
    Song("Bad Moon Rising", "CCR", ["D", "A", "G"]),
    Song("Have You Ever Seen the Rain", "CCR", ["Am", "F", "C", "G"]),
    Song("Proud Mary", "CCR", ["D", "A", "Bm", "G"]),
    Song("Wild Thing", "The Troggs", ["A", "D", "E"]),
    Song("Louie Louie", "The Kingsmen", ["A", "D", "Em"]),
    Song("La Bamba", "Ritchie Valens", ["C", "F", "G"]),
    Song("Twist and Shout", "Beatles", ["D", "G", "A"]),
    Song("I Saw Her Standing There", "Beatles", ["E", "A", "B"]),
    Song("Love Me Do", "Beatles", ["G", "C", "D"]),

    # ---- 60s/70s Folk & Rock ----
    Song("Blowin' in the Wind", "Bob Dylan", ["G", "C", "D"]),
    Song("The Times They Are A-Changin'", "Bob Dylan", ["G", "Em", "C", "D"]),
    Song("Mr. Tambourine Man", "Bob Dylan", ["G", "A", "D"]),
    Song("Hey Jude", "Beatles", ["F", "C", "Bb"]),
    Song("Here Comes the Sun", "Beatles", ["G", "C", "D", "A"]),
    Song("Blackbird", "Beatles", ["G", "Am", "C", "D"]),
    Song("Yesterday", "Beatles", ["G", "F", "Em", "D"]),
    Song("Redemption Song", "Bob Marley", ["G", "Em", "C", "Am", "D"]),
    Song("Stir It Up", "Bob Marley", ["A", "D", "E"]),
    Song("Is This Love", "Bob Marley", ["F", "Am", "Dm", "C"]),

    # ---- Acoustic Favorites ----
    Song("Wagon Wheel", "Old Crow Medicine Show", ["G", "D", "Em", "C"]),
    Song("Ho Hey", "The Lumineers", ["C", "F", "Am", "G"]),
    Song("Riptide", "Vance Joy", ["Am", "G", "C"]),
    Song("I'm Yours", "Jason Mraz", ["G", "D", "Em", "C"]),
    Song("Hey There Delilah", "Plain White T's", ["D", "A", "Bm", "G"]),
    Song("Chasing Cars", "Snow Patrol", ["A", "E", "D"]),
    Song("The Scientist", "Coldplay", ["Dm", "F", "C", "Bb"]),
    Song("Yellow", "Coldplay", ["G", "D", "C"]),
    Song("Fix You", "Coldplay", ["C", "Em", "G"]),
    Song("Clocks", "Coldplay", ["D", "Am", "Em"]),

    # ---- Pop/Rock 2000s ----
    Song("Counting Stars", "OneRepublic", ["Am", "C", "G", "F"]),
    Song("Demons", "Imagine Dragons", ["D", "A", "Bm", "G"]),
    Song("Radioactive", "Imagine Dragons", ["Am", "C", "G", "D"]),
    Song("Viva La Vida", "Coldplay", ["C", "D", "G", "Em"]),
    Song("Use Somebody", "Kings of Leon", ["C", "Em", "Am", "F"]),
    Song("Sex on Fire", "Kings of Leon", ["E", "A"]),
    Song("Boulevard of Broken Dreams", "Green Day", ["Em", "G", "D", "A"]),
    Song("Good Riddance", "Green Day", ["G", "Cadd9", "D"]),
    Song("21 Guns", "Green Day", ["D", "Bm", "G", "A"]),
    Song("When I Come Around", "Green Day", ["G", "D", "Em", "C"]),

    # ---- Country ----
    Song("Take Me Home, Country Roads", "John Denver", ["G", "Em", "D", "C"]),
    Song("Ring of Fire", "Johnny Cash", ["G", "C", "D"]),
    Song("Folsom Prison Blues", "Johnny Cash", ["E", "A", "B"]),
    Song("I Walk the Line", "Johnny Cash", ["A", "D", "E"]),
    Song("Jolene", "Dolly Parton", ["Am", "C", "G", "Em"]),
    Song("Crazy", "Patsy Cline", ["G", "E7", "Am", "D7"]),
    Song("Stand By Your Man", "Tammy Wynette", ["A", "D", "E"]),
    Song("Friends in Low Places", "Garth Brooks", ["A", "Bm", "E"]),
    Song("The Gambler", "Kenny Rogers", ["C", "F", "G"]),
    Song("On the Road Again", "Willie Nelson", ["E", "A", "B"]),

    # ---- 80s/90s ----
    Song("With or Without You", "U2", ["D", "A", "Bm", "G"]),
    Song("One", "U2", ["Am", "D", "Fmaj7", "G"]),
    Song("Where the Streets Have No Name", "U2", ["D", "G", "Bm", "A"]),
    Song("Every Breath You Take", "The Police", ["A", "F#m", "D", "E"]),
    Song("Zombie", "The Cranberries", ["Em", "C", "G", "D"]),
    Song("Dreams", "The Cranberries", ["G", "D", "Am", "C"]),
    Song("Linger", "The Cranberries", ["A", "D", "E"]),
    Song("Creep", "Radiohead", ["G", "B", "C"]),
    Song("Torn", "Natalie Imbruglia", ["F", "Am", "Bb", "C"]),
    Song("Breakfast at Tiffany's", "Deep Blue Something", ["D", "G", "A"]),

    # ---- Modern Pop ----
    Song("Someone Like You", "Adele", ["A", "E", "F#m", "D"]),
    Song("Rolling in the Deep", "Adele", ["Am", "Em", "G"]),
    Song("Stay With Me", "Sam Smith", ["Am", "F", "C"]),
    Song("Thinking Out Loud", "Ed Sheeran", ["D", "G", "A", "Bm"]),
    Song("Perfect", "Ed Sheeran", ["G", "Em", "C", "D"]),
    Song("Shape of You", "Ed Sheeran", ["Am", "Dm", "F", "G"]),
    Song("Photograph", "Ed Sheeran", ["E", "A", "B"]),
    Song("Let Her Go", "Passenger", ["G", "D", "Em", "C"]),
    Song("Happier", "Marshmello", ["Am", "F", "C", "G"]),
    Song("Shallow", "Lady Gaga", ["Em", "D", "G", "C"]),

    # ---- Indie/Alternative ----
    Song("Pumped Up Kicks", "Foster the People", ["Em", "G", "D", "A"]),
    Song("Little Talks", "Of Monsters and Men", ["Am", "F", "C", "G"]),
    Song("Take Me to Church", "Hozier", ["Em", "Am", "G", "C"]),
    Song("The A Team", "Ed Sheeran", ["G", "D", "Em", "C"]),
    Song("Budapest", "George Ezra", ["G", "D", "C"]),
    Song("Shotgun", "George Ezra", ["G", "D", "Em", "C"]),
    Song("Mr. Brightside", "The Killers", ["D", "G", "Bm", "A"]),
    Song("Somewhere Only We Know", "Keane", ["A", "E", "D"]),
    Song("High and Dry", "Radiohead", ["E", "A", "F#m"]),
    Song("Champagne Supernova", "Oasis", ["A", "E", "D"]),

    # ---- More Classics ----
    Song("House of the Rising Sun", "The Animals", ["Am", "C", "D", "F", "E"]),
    Song("Stand By Me", "Ben E. King", ["A", "F#m", "D", "E"]),
    Song("Lean on Me", "Bill Withers", ["C", "F", "G"]),
    Song("Ain't No Sunshine", "Bill Withers", ["Am", "Em", "Dm"]),
    Song("What's Going On", "Marvin Gaye", ["E", "C", "G", "D"]),
    Song("Wonderful Tonight", "Eric Clapton", ["G", "D", "C"]),
    Song("Tears in Heaven", "Eric Clapton", ["A", "E", "F#m", "D"]),
    Song("Layla (Unplugged)", "Eric Clapton", ["Am", "C", "G", "D"]),
    Song("Hotel California", "Eagles", ["Am", "E", "G", "D", "F", "C", "Dm"]),
    Song("Take It Easy", "Eagles", ["G", "D", "C", "Em"]),

]
