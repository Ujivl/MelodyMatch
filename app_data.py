"""
Song class file
"""
from __future__ import annotations
import csv
from typing import Any, Union


class Song:
    """
    A song object that stores the song, including all of its properties. This is where we will access a song's:
    artist, song name, duration_ms, explicit, year, popularity, danceability, energy, key, loudness, mode, speechiness,
    acousticness, instrumentalness, liveness, valence, tempo, genre

    Instance Attributes:
        - artist: The person that made the song (str)
        - song_name: The name of the song (str)
        - duration: the duration of the song in milliseconds (int) <---- TODO: don't really need it
        - explicit: If the song is explicit or not (bool)
        - year: the year the song was released (int)
        - popularity: the popularity of the song, the higher it is the more popular (int)
        - danceability: a float value that determines the level of danceability (float)
        - energy: measures intensity and activity, it's a value from 0 to 1 (float) <--- TODO: don't really need it
        - key: Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
            If no key was detected, the value is -1. (int) <----  TODO: don't really need it
        - loudness: Decibal units of the song, goes from -60 to 0 (float) <----  TODO: don't really need it
        - mode: if the track is in major or minor, (1 is major, 0 is minor) (int) <----  TODO: don't really need it
        - speechiness: Presence of spoken words in the song (goes from 0 to 1) (float)
        - acousticness: accousticness of the song, 1.0 means high confidence that the song is acoustic (float)
        - instrumentalness: instrument usage in song, goes from 0.0 to 1.0 (float)
        - liveness: detects the likelihood that the song was recorded in front of a
            live audience (float) <---- TODO: don't really need it
        - valence: positivity of the song, closer to 1.0 correlates to more positivity, (float)
        - tempo: the tempo of the song recorded in beats per minute (float)
        - genre: the list of genres in the song (list[str])
    """

    artist: str
    song_name: str
    explicit: bool
    year: int
    popularity: int
    danceability: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    valence: float
    tempo: float
    genre: list[str]

    def __init__(self, artist: str, song_name: str, explicit: bool, year: int, popularity: int, danceability: float,
                 speechiness: float, acousticness: float, instrumentalness: float, valence: float, tempo: float,
                 genre: list[str]) -> None:
        """
        Initializes a new song object with the attributes in the csv file
        """
        self.artist = artist
        self.song_name = song_name
        self.explicit = explicit
        self.year = year
        self.popularity = popularity
        self.danceability = danceability
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.tempo = tempo
        self.genre = genre


class _WeightedVertex:
    """A vertex in a weighted book review graph, used to represent a Song.

    Instance Attributes:
        - item: The data stored in this vertex, representing a song.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_WeightedVertex, float]

    def __init__(self, item: Any, neighbours: dict[_WeightedVertex, float]):
        self.item = item
        self.neighbours = neighbours


class WeightedGraph:
    """
    A weighted graph with each song being the node and each edge having a weight to denote similarity between songs.

    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.

    _vertices: dict[Song, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Song) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item, {})

    def add_edge(self, item1: Any, item2: Any, weight: float) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError


################################################################################################
# Test parser, prints all the artist names in the small test csv file
################################################################################################
with open("songs_test_small.csv", 'r') as song_file:
    line_reader = csv.reader(song_file)
    li = []
    song_file.readline()
    for row in line_reader:
        song = Song(row[0], row[1], bool(row[3]), int(row[4]), int(row[5]), float(row[6]), float(row[11]),
                    float(row[12]), float(row[13]), float(row[14]), float(row[15]), "".split(row[16]))
        li.append(song)
for i in li:
    print(i.artist)
