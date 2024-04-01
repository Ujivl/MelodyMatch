"""
file implementing the gui of the application
"""
import tkinter as tk
from tkinter import Scale
from tkinter import ttk, Frame, Canvas, BOTH, LEFT, RIGHT, Y
import customtkinter

import app_data as ad
import final_window

from app_data import Song

g, song_name_list, genre_name_set = ad.create_graph_without_edges("songs_test_small.csv")


class PrioritizeApp_1:
    """
`
    """

    def __init__(self, second, root):
        self.root = root
        self.second = second

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
                self.question_label = tk.Label(second, text=item)
                # self.question_label.pack()
                self.question_label.grid(column=0, row=0)
                self.options = sorted(genre_name_set)
                self.value_inside = tk.StringVar(second)
                self.value_inside.set(self.options[0])  # Set the default value
                # self.dropdown_menu = tk.OptionMenu(second, self.value_inside, *self.options)
                self.dropdown_menu = customtkinter.CTkOptionMenu(master=second, variable=self.value_inside,
                                                                 values=self.options)
                # self.dropdown_menu.pack()
                self.dropdown_menu.grid(column=0, row=1)
                self.entries[item] = self.value_inside
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=1)

            elif item == 'explicit':
                self.checkbox_var = tk.BooleanVar()
                # self.check = tk.Checkbutton(second, text="Explicit", variable=self.checkbox_var)
                self.check = customtkinter.CTkCheckBox(master=second, text="Explicit", variable=self.checkbox_var)
                # self.check.pack()
                self.check.grid(column=0, row=40)
                self.entries[item] = self.checkbox_var
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=40)

            else:
                self.question_label = tk.Label(second, text=item)
                # self.question_label.pack()
                self.question_label.grid(column=0, row=2 * y_count + 3)
                minimum, maximum, index = get_max_min(item)
                slider = Scale(second, from_=minimum, to=maximum, resolution=index, orient='horizontal')
                # slider.pack(pady=1)
                slider.grid(column=0, row=2 * y_count + 4)
                self.entries[item] = slider
                # self.button = tk.Button(root, text=f"{item}?", command=lambda: self.what_is_item(item))
                # self.button.grid(column=1, row=2 * y_count + 4)

            y_count += 1

        dictionary = {"Genre?": [lambda: self.what_is_item('genre'), 1],
                      "Year Released?": [lambda: self.what_is_item('year released'), 6],
                      "Popularity?": [lambda: self.what_is_item('popularity'), 8],
                      "Danceability?": [lambda: self.what_is_item('danceability'), 10],
                      "Energy?": [lambda: self.what_is_item('energy'), 12],
                      "Key?": [lambda: self.what_is_item('key'), 14],
                      "Loudness?": [lambda: self.what_is_item('loudness'), 16],
                      "Mode?": [lambda: self.what_is_item('mode'), 18],
                      "Speechiness?": [lambda: self.what_is_item('speechiness'), 20],
                      "Acousticness?": [lambda: self.what_is_item('acousticness'), 22],
                      "Instrumentalness?": [lambda: self.what_is_item('instrumentalness'), 24],
                      "Valence?": [lambda: self.what_is_item('valence'), 26],
                      "Tempo?": [lambda: self.what_is_item('tempo'), 28],
                      "Explicit?": [lambda: self.what_is_item('explicit'), 40]}

        for item in dictionary:
            self.button = customtkinter.CTkButton(master=second, text=item, command=dictionary[item][0])
            self.button.grid(column=1, row=dictionary[item][1])

        # self.submit_button = tk.Button(second, text="Submit", command=self.submit_answer)
        self.submit_button = customtkinter.CTkButton(master=second, text="Submit", command=self.submit_answer)
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
    root.title('MelodyMatcher')
    root.geometry("500x900")

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scroller = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroller.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scroller.set)

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    PrioritizeApp_1(second_frame, root)

    root.mainloop()


if __name__ == "__main__":
    main()
