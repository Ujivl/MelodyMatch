"""
file implementing the gui of the application
"""
import tkinter as tk
from tkinter import BOTH, Canvas, Frame, LEFT, RIGHT, Scale, Y
from typing import Any

import app_data as ad
import final_window
from app_data import Song, FILE_NAME

G, SONG_NAME_LIST, GENRE_NAME_SET = ad.create_graph_without_edges(FILE_NAME)


class PrioritizeApp:
    """
    This class creates the user interface for a music prioritization application.

    It initializes a graphical interface where users can select and prioritize various song
    attributes such as genre, year released, and other characteristics to find songs that match
    their preferences.

    Instance Attributes:
    - root: The Tkinter Window
    - second: The Tkinter Frame
    - items: List of song characterisics
    - entries: Key Value for each characteristic
    - y_count: Column value to display each characteristic and its slider
    - button: Button for each characterstic
    - submit_button: Button to submit user entered value
    """
    root: tk.Tk
    second: Frame
    items: list[str]
    entries: dict[str, Any]
    y_count: int
    button: tk.Button
    submit_button: tk.Button

    def __init__(self, second: Frame, root: tk.Tk) -> None:
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
        self.y_count = 0

        for item in self.items:
            if item == 'genre':
                question_label = tk.Label(second, text=item)
                # self.question_label.pack()
                question_label.grid(column=0, row=0)
                options = sorted(GENRE_NAME_SET)
                value_inside = tk.StringVar(second)
                value_inside.set(options[0])  # Set the default value
                dropdown_menu = tk.OptionMenu(second, value_inside, *options)
                dropdown_menu.grid(column=0, row=1)
                self.entries[item] = value_inside

            elif item == 'explicit':
                checkbox_var = tk.BooleanVar()
                check = tk.Checkbutton(second, text="Explicit", variable=checkbox_var)
                check.grid(column=0, row=40)
                self.entries[item] = checkbox_var

            else:
                question_label = tk.Label(second, text=item)
                question_label.grid(column=0, row=2 * self.y_count + 3)
                minimum, maximum, index = get_max_min(item)
                slider = Scale(second, from_=minimum, to=maximum, resolution=index, orient='horizontal')
                slider.grid(column=0, row=2 * self.y_count + 4)
                self.entries[item] = slider

            self.y_count += 1

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
            self.button = tk.Button(second, text=item, command=dictionary[item][0])
            self.button.grid(column=1, row=dictionary[item][1])

        self.submit_button = tk.Button(second, text="Submit", command=self.submit_answer)
        self.submit_button.grid(column=0, row=45)

    def submit_answer(self) -> None:
        """
        Processes user input to create a Song object and finds the top 10 similar songs.
        It gathers data from GUI entries, creates a Song object, and uses a graph to calculate
        the similarity with other songs. Priority scores are assigned for the similarity factors.
        The function then opens a new window displaying the top 10 similar songs.
        """

        ans = [entry.get() for _, entry in self.entries.items()]

        temp_song = Song('user', 'user song', ans[13], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6],
                         ans[7], ans[8], ans[9], ans[10], ans[11], ans[12], set(ans[0].split(',')))

        # WHAT TO SET PRIORITY SCORE?
        priority = {factor: 1000000 for factor in temp_song.similarity_factors}
        G.add_vertex(temp_song)
        G.chosen_song = temp_song
        G.add_all_weighted_edges(chosen_song=G.chosen_song, prioritylist=priority, explicit=temp_song.explicit)

        chosen_songs = G.sort_weights(10)
        self.root.destroy()
        final_window.final_window(chosen_songs, "Your Values")

    def what_is_item(self, item: str) -> None:
        """
        Displays a detailed description of the specified song attribute in a new window.
        """

        final_window.description(item)


def get_max_min(item: str) -> (float, float, float):
    """
    Returns the minimum, maximum, and step values for the scale of a given song attribute.
    """
    if item == 'year released':
        return 1990, 2020, 1
    elif item == 'popularity':
        return 0, 100, 1
    elif item in {'danceability', 'energy', 'acousticness', 'instrumentalness', 'valence'}:
        return 0, 1, 0.01
    elif item == 'key':
        return 0, 11, 1
    elif item == 'loudness':
        return -0.28, -20.5, -0.01
    elif item == 'mode':
        return 0, 1, 1
    elif item == 'speechiness':
        return 0.02, 0.58, 0.01
    elif item == 'liveness':
        return 0.02, 0.85, 0.01
    elif item == 'tempo':
        return 60, 211, 1
    else:
        return 0, 0, 0


def main() -> None:
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

    scroller = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroller.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scroller.set)

    canvas.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    PrioritizeApp(second_frame, root)

    root.mainloop()


if __name__ == "__main__":
    main()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'max-nested-blocks': 4
    })
