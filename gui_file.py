"""
file implementing the gui of the application
"""
import tkinter as tk
from typing import Union
from tkinter import Scale

import app_data as ad
from final_window import FinalWindow

g, song_name_list, genre_name_set = ad.create_graph_without_edges_and_list("songs_test_small.csv")
print(song_name_list)

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
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo",
            "explicit"
        ]

        self.entries = {}

        for item in self.items:
            if item == 'genre':
                self.question_label = tk.Label(root, text=item)
                self.question_label.pack(padx=10, pady=4)
                self.options = sorted(genre_name_set)
                self.value_inside = tk.StringVar(root)
                self.value_inside.set(self.options[0])  # Set the default value
                self.dropdown_menu = tk.OptionMenu(root, self.value_inside, *self.options)
                self.dropdown_menu.pack()
                self.entries[item] = self.value_inside

            elif item == 'explicit':
                checkbox_var = tk.BooleanVar()
                self.check = tk.Checkbutton(root, text="Explicit", variable=checkbox_var)
                self.check.pack(pady=10)

            else:
                self.question_label = tk.Label(root, text=item)
                self.question_label.pack(padx=10, pady=4)
                minimum, maximum = get_max_min(item)
                slider = Scale(root, from_=minimum, to=maximum, orient='horizontal')
                slider.pack(padx=10, pady=4)
                self.entries[item] = slider

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=10)

    def submit_answer(self):
        all_answers = {item: entry.get() for item, entry in self.entries.items()}

        # Create song object and cook...
        temp_song = Song(...)
        g.add_vertex(temp_song)
        g.add_all_weighted_edges(chosen_song=temp_song, prioritylist=..., explicit=...)

        self.root.destroy()
        new_root = tk.Tk()
        FinalWindow(new_root, g.sort_weights(10))
        new_root.title("FinalWindow")
        new_root.geometry("400x800")
        new_root.mainloop()


def get_max_min(item: str) -> (float, float):
    """
    Need to incoroprate for each properly
    """
    if item == 'year released':
        return 1990, 2020

    else:
        return 0, 100


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    PrioritizeApp_1(root)
    root.title("MelodyMatcher")
    root.geometry("400x800")
    root.mainloop()


if __name__ == "__main__":
    main()
