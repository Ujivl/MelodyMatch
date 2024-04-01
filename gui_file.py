"""
file implementing the gui of the application
"""
import tkinter as tk
from tkinter import Scale

import app_data as ad
import final_window

from app_data import Song

g, song_name_list, genre_name_set = ad.create_graph_without_edges("songs_test_small.csv")


class PrioritizeApp_1:
    """
`
    """

    def __init__(self, root):
        self.root = root

        # Initial list of items
        self.items = [
            "genre",
            "year released",
            "popularity",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo",
            "explicit"
        ]

        self.entries = {}
        y_count = 0

        for item in self.items:
            if item == 'genre':
                self.question_label = tk.Label(root, text=item)
                # self.question_label.pack()
                self.question_label.grid(column=0, row=0)
                self.options = sorted(genre_name_set)
                self.value_inside = tk.StringVar(root)
                self.value_inside.set(self.options[0])  # Set the default value
                self.dropdown_menu = tk.OptionMenu(root, self.value_inside, *self.options)
                # self.dropdown_menu.pack()
                self.dropdown_menu.grid(column=0, row=1)
                self.entries[item] = self.value_inside
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=1)

            elif item == 'explicit':
                self.checkbox_var = tk.BooleanVar()
                self.check = tk.Checkbutton(root, text="Explicit", variable=self.checkbox_var)
                # self.check.pack()
                self.check.grid(column=0, row=40)
                self.entries[item] = self.checkbox_var
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=40)

            else:
                self.question_label = tk.Label(root, text=item)
                # self.question_label.pack()
                self.question_label.grid(column=0, row=2 * y_count + 3)
                minimum, maximum, index = get_max_min(item)
                slider = Scale(root, from_=minimum, to=maximum, resolution=index, orient='horizontal')
                # slider.pack(pady=1)
                slider.grid(column=0, row=2 * y_count + 4)
                self.entries[item] = slider
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=2 * y_count + 4)

            y_count += 1

        self.button = tk.Button(root, text="Genre?", command=lambda: self.what_is_item('genre'))
        self.button.grid(column=1, row=1)
        self.button = tk.Button(root, text="Year Released?", command=lambda: self.what_is_item('year released'))
        self.button.grid(column=1, row=6)
        self.button = tk.Button(root, text="Popularity?", command=lambda: self.what_is_item('popularity'))
        self.button.grid(column=1, row=8)
        self.button = tk.Button(root, text="Danceability?", command=lambda: self.what_is_item('danceability'))
        self.button.grid(column=1, row=10)
        self.button = tk.Button(root, text="Energy?", command=lambda: self.what_is_item('energy'))
        self.button.grid(column=1, row=12)
        self.button = tk.Button(root, text="Key?", command=lambda: self.what_is_item('key'))
        self.button.grid(column=1, row=14)
        self.button = tk.Button(root, text="Loudness?", command=lambda: self.what_is_item('loudness'))
        self.button.grid(column=1, row=16)
        self.button = tk.Button(root, text="Mode?", command=lambda: self.what_is_item('mode'))
        self.button.grid(column=1, row=18)
        self.button = tk.Button(root, text="Speechiness?", command=lambda: self.what_is_item('speechiness'))
        self.button.grid(column=1, row=20)
        self.button = tk.Button(root, text="Acousticness?", command=lambda: self.what_is_item('acousticness'))
        self.button.grid(column=1, row=22)
        self.button = tk.Button(root, text="Instrumentalness?", command=lambda: self.what_is_item('instrumentalness'))
        self.button.grid(column=1, row=24)
        self.button = tk.Button(root, text="Valence?", command=lambda: self.what_is_item('valence'))
        self.button.grid(column=1, row=26)
        self.button = tk.Button(root, text="Tempo?", command=lambda: self.what_is_item('tempo'))
        self.button.grid(column=1, row=28)
        self.button = tk.Button(root, text="Explicit?", command=lambda: self.what_is_item('explicit'))
        self.button.grid(column=1, row=40)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        # self.submit_button.pack(pady=1)
        self.submit_button.grid(column=0, row=45)

    def submit_answer(self):
        """artist: str, song_name: str, explicit: bool, year: int, popularity: int, danceability: float,
        energy: float, key: int, loudness: float, mode: int, speechiness: float, acousticness: float,
        instrumentalness: float, valence: float, tempo: float, genre: set[str]"""

        ans = [entry.get() for item, entry in self.entries.items()]

        temp_song = Song('user', 'user song', ans[13], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6],
                         ans[7], ans[8], ans[9], ans[10], ans[11], ans[12], set(ans[0].split(',')))

        # WHAT TO SET PRIORITY SCORE?
        priority = {factor: 1000000 for factor in temp_song.similarity_factors}
        g.add_vertex(temp_song)
        g.chosen_song = temp_song
        g.add_all_weighted_edges(chosen_song=g.chosen_song, prioritylist=priority, explicit=temp_song.explicit)

        chosen_songs = g.sort_weights(10)
        self.root.destroy()
        # Can edit later
        final_window.final_window(chosen_songs, "Your Values")

    def what_is_item(self, item: str):
        """artist: str, song_name: str, explicit: bool, year: int, popularity: int, danceability: float,
        energy: float, key: int, loudness: float, mode: int, speechiness: float, acousticness: float,
        instrumentalness: float, valence: float, tempo: float, genre: set[str]"""

        final_window.description(item)


def get_max_min(item: str) -> (float, float, float):
    """
    Need to incoroprate for each properly
    """
    if item == 'year released':
        return 1990, 2020, 1
    elif item == 'popularity':
        return 0, 100, 1
    elif (item == 'danceability' or item == 'energy' or item == 'acousticness'
          or item == 'instrumentalness' or item == 'valence'):
        return 0, 1, 0.01
    elif item == 'key':
        return 0, 11, 1
    elif item == 'loudness':
        return -20.5, -0.28, 0.01
    elif item == 'mode':
        return 0, 1, 1
    elif item == 'speechiness':
        return 0.02, 0.58, 0.01
    elif item == 'liveness':
        return 0.02, 0.85, 0.01
    elif item == 'tempo':
        return 60, 211, 1


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    PrioritizeApp_1(root)
    root.title("MelodyMatcher")
    root.geometry("300x1200")
    root.mainloop()


if __name__ == "__main__":
    main()
