"""
file implementing the gui of the application
"""
import tkinter as tk
from typing import Union
import app_data as ad
import final_window

g, song_name_list, genre = ad.create_graph_without_edges("songs_test_small.csv")


class DragDropListbox(tk.Listbox):
    """
    This class creates a listbox which contains items that can be moved through drag and drop. It is a child class
    that inherits the Listbox widget built into the tkinter module. The list box module creates a box with ordered
    items. This child class lets the user move it around.

    Instance Attributes:
        - curIndex

    """

    curIndex: Union[None, float]

    def __init__(self, root: tk.Tk, background: str):
        """
        Initializes a dragdroplistbox object that lets the user drag around the items in the listbox
        """
        super().__init__(root, bg=background, justify="center")
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)

        self.items = [
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
            "genre"
        ]

        self.selection = tk.Label(root, text="Please rank how you value these musical characteristics:",
                                  font=('Times New Roman', 18))
        self.selection.pack(pady=10)

        for item in self.items:
            self.insert(tk.END, item.capitalize())
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.attributes_with_weights = {}
        self.curIndex = None

    def set_current(self, event):
        """
        When the left mouse is clicked, this function gets called. It takes in the mouse y coordinate and assigns it to
        currIndex.
        """
        self.curIndex = self.nearest(event.y)

    def shift_selection(self, event):
        """
        gets the nearest position where the mouse is moved and then moves it down or above based on whether it is lesser
        or greater than the currIndex
        """

        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i

    def save_prioritization(self):
        """
        Saves the prioritized items and prints them out for now, this will chance later.
        """
        weight = 1
        prioritized_attributes = self.get(0, tk.END)
        for attribute_imdex in range(len(prioritized_attributes) - 1, -1, -1):
            self.attributes_with_weights[prioritized_attributes[attribute_imdex].lower()] = (10 ** weight)
            weight += 1
        print("Prioritized Items with weights: " + str(self.attributes_with_weights))


class DropdownBox:
    """
    Creates a dropdown menu
    """

    selected_song: str = "Oops!...I Did It Again"

    def __init__(self, root):
        self.root = root

        self.label = tk.Label(root, text="Select a Song:", font=('Times New Roman', 18))
        self.label.pack()

        self.options = song_name_list
        self.value_inside = tk.StringVar(root)
        self.value_inside.set(self.options[0])
        self.dropdown_menu = tk.OptionMenu(root, self.value_inside, *self.options)
        # self.dropdown_menu = customtkinter.CTkOptionMenu(master=root, variable=self.value_inside, values=self.options)
        self.dropdown_menu.pack()

    def on_select(self):
        """
        Gets the chosen song.
        """
        self.selected_song = self.value_inside.get()


def save_all_information(root, priority_list_object: DragDropListbox, drag_drop_object: DropdownBox, explicit: bool):
    """
    saves all the information and adds the weighted edges to the graph
    """
    drag_drop_object.on_select()
    priority_list_object.save_prioritization()
    user_selected_song = g.return_and_save_chosen_song(drag_drop_object.selected_song)
    g.add_all_weighted_edges(chosen_song=user_selected_song,
                             prioritylist=priority_list_object.attributes_with_weights,
                             explicit=explicit)
    final_selected_songs = g.sort_weights(10)
    root.destroy()
    final_window.final_window(final_selected_songs, drag_drop_object.selected_song)


def what_is_item(item: str):
    """artist: str, song_name: str, explicit: bool, year: int, popularity: int, danceability: float,
    energy: float, key: int, loudness: float, mode: int, speechiness: float, acousticness: float,
    instrumentalness: float, valence: float, tempo: float, genre: set[str]"""

    final_window.description(item)


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    root.title("MelodyMatcher")
    root.geometry("600x700")

    song_selection_object = DropdownBox(root)
    priority_list_object = DragDropListbox(root, "gray")

    checkbox_var = tk.BooleanVar()

    buttonframe = tk.Frame(root)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)
    buttonframe.columnconfigure(2, weight=1)

    dictionary = {"Genre?": [lambda: what_is_item('genre'), [0, 0]],
                  "Year Released?": [lambda: what_is_item('year released'), [0, 1]],
                  "Popularity?": [lambda: what_is_item('popularity'), [0, 2]],
                  "Danceability?": [lambda: what_is_item('danceability'), [1, 0]],
                  "Energy?": [lambda: what_is_item('energy'), [1, 1]],
                  "Key?": [lambda: what_is_item('key'), [1, 2]],
                  "Loudness?": [lambda: what_is_item('loudness'), [2, 0]],
                  "Mode?": [lambda: what_is_item('mode'), [2, 1]],
                  "Speechiness?": [lambda: what_is_item('speechiness'), [2, 2]],
                  "Acousticness?": [lambda: what_is_item('acousticness'), [3, 0]],
                  "Instrumentalness?": [lambda: what_is_item('instrumentalness'), [3, 1]],
                  "Valence?": [lambda: what_is_item('valence'), [3, 2]],
                  "Tempo?": [lambda: what_is_item('tempo'), [4, 0]],
                  "Explicit?": [lambda: what_is_item('explicit'), [4, 1]]}

    for item in dictionary:
        button = tk.Button(buttonframe, text=item, font=("Times New Roman", 18), command=dictionary[item][0])
        button.grid(row=dictionary[item][1][0], column=dictionary[item][1][1], sticky=tk.W + tk.E)

    buttonframe.pack(fill='x')

    checkbox = tk.Checkbutton(root, text="Explicit", variable=checkbox_var)
    # checkbox = customtkinter.CTkCheckBox(master=root, text="Explicit", variable=checkbox_var)
    checkbox.pack(pady=10)

    # save_button = tk.Button(root, text="Calculate similar songs",
    #                         command=lambda: save_all_information(root,
    #                                                              priority_list_object,
    #                                                              song_selection_object,
    #                                                              checkbox_var.get()))
    save_button = tk.Button(root, text="Calculate similar songs",
                            command=lambda: save_all_information(root,
                                                                 priority_list_object,
                                                                 song_selection_object,
                                                                 checkbox_var.get()))
    save_button.pack(pady=50)
    root.mainloop()


if __name__ == "__main__":
    main()
