"""
This file includes all the back-end for the program. It includes the song class, weighted vertex class, weighted graph
class, and the create_graph_without_edges function. This function creates the graph and adds all the song objects by
parsing through the csv file.
"""
from __future__ import annotations
import csv
from typing import Any, Optional


FILE_NAME = "songs_normalize.csv"


class Song:
    """
    A song object that stores the song, including all of its properties. This is where we will access a song's:
    artist, song name, duration_ms, explicit, year, popularity, danceability, energy, key, loudness, mode, speechiness,
    acousticness, instrumentalness, liveness, valence, tempo, genre

    Instance Attributes:
        - artist: The person that made the song (str)
        - song_name: The name of the song (str)
        - explicit: If the song is explicit or not (bool)
        - similarity_factors: a dictionary containing all the song attributes we will be comparing. The key is the
            attribute name denoted in string format. The values are the attribute values.
    """

    artist: str
    song_name: str
    explicit: bool
    similarity_factors: dict

    def __init__(self, artist: str, song_name: str, explicit: bool, year: int, popularity: int, danceability: float,
                 energy: float, key: int, loudness: float, mode: int, speechiness: float, acousticness: float,
                 instrumentalness: float, valence: float, tempo: float, genre: set[str]) -> None:
        """
        Initializes a new song object with the attributes in the csv file
        """
        self.artist = artist
        self.song_name = song_name
        self.explicit = explicit
        self.similarity_factors = {
            "year released": year,
            "popularity": popularity,
            "danceability": danceability,
            "energy": energy,
            "key": key,
            "loudness": loudness,
            "mode": mode,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
            "valence": valence,
            "tempo": tempo,
            "genre": genre}


class _WeightedVertex:
    """A vertex in a weighted graph, used to represent a Song.

    Instance Attributes:
        - item: The data stored in this vertex, representing a song.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Song
    neighbours: dict[_WeightedVertex, float]

    def __init__(self, item: Song, neighbours: dict[_WeightedVertex, float]) -> None:
        self.item = item
        self.neighbours = neighbours


class WeightedGraph:
    """
    A weighted graph with each song being the node and each edge having a weight to denote similarity between songs.

    Instance Attributes:
        - chosen_song: The song object that the user picked.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.

    _vertices: dict[Song, _WeightedVertex]
    chosen_song: Song

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

    def add_edge(self, item1: Any, item2: Any, weight: float = 0.0) -> None:
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

    def add_all_weighted_edges(self, chosen_song: Song, prioritylist: dict[str, int], explicit: bool) -> None:
        """
        Adds the edges to the weighted graph we made, this is also where the similarity score will be calculated
        """
        for other_song in self._vertices:  # Iterates through all the songs in the graph
            weight = 0
            if chosen_song.song_name == other_song.song_name:  # If other song is the chosen song, we ignore
                continue
            elif explicit != other_song.explicit:  # filtering out whether we want explicit or not
                self.add_edge(chosen_song, other_song, 0.0)  # adds an edge with 0 as weight
            else:
                for factor in prioritylist:  # this will loop through each factor and add it to the vertex
                    # calls the calculate initial weight function to get a raw weight then prioritizes it
                    weight += (self.calculate_initial_weight(factor, other_song, chosen_song) * prioritylist[factor])
                self.add_edge(chosen_song, other_song, weight)  # adds an edge with the calcucated weight

    def calculate_initial_weight(self, factor: str, other_song: Song, chosen_song: Song) -> float:
        """
        Helper function to calculate the initial weights before multiplying them by the priority list.
        """
        if factor == "genre":
            #  Uses intersection over union to get similarity value for all the genres
            numerator = len(chosen_song.similarity_factors[factor].intersection(other_song.similarity_factors[factor]))
            denominator = len(chosen_song.similarity_factors[factor].union(other_song.similarity_factors[factor]))
            return (numerator / denominator) * 1000000
        elif abs(chosen_song.similarity_factors[factor] - other_song.similarity_factors[factor]) != 0:
            return 1 / (abs(chosen_song.similarity_factors[factor] - other_song.similarity_factors[factor]))
        else:
            return 1000000

    def return_and_save_chosen_song(self, chosen_song_name: str) -> Optional[Song, str]:
        """
        Returns the song object from the name of the song.
        """
        for song in self._vertices:
            if chosen_song_name == song.song_name:
                self.chosen_song = song
                return song
        return "song does not exist"

    def sort_weights(self, num_of_songs: int) -> list[Song]:
        """
        This function sorts the neighbors of the chosen song by weight and returns the first 10. It uses a lambda
        function to sort the list of weights in descending order, so that it can just slice it into the first
        [num_of_songs] elements, and return it back into dictionary format.
        """
        sorted_dict = dict(sorted(self._vertices[self.chosen_song].neighbours.items(), key=lambda item: item[1],
                                  reverse=True)[:num_of_songs])

        return [x.item for x in sorted_dict]


def create_graph_without_edges(file: str) -> tuple[WeightedGraph, list[str], set[str]]:
    """
    Returns a weighted graph without any edge connections yet.
    """
    g = WeightedGraph()
    li = []
    genre_name_set = set()
    with open(file, 'r') as song_file:
        line_reader = csv.reader(song_file)
        song_file.readline()
        for row in line_reader:
            li.append(row[1])
            genre_name_set.add(row[17])
            song = Song(row[0], row[1], (row[3] == "True"), int(row[4]), int(row[5]), float(row[6]), float(row[7]),
                        int(row[8]), float(row[9]), int(row[10]), float(row[11]), float(row[12]), float(row[13]),
                        float(row[14]), float(row[15]), set(row[17].split(", ")))
            g.add_vertex(song)
    return g, li, genre_name_set
