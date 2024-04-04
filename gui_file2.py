"""
This file implements gui file 2, which is the automatic song matcher. In this file, each major widget is separated into
classes. The classes are: DragDropListbox and DropdownBox. DragDropListBox inherits from the built-in listbox widget,
and is essentially a listbox where the user can switch the location of the elements. DropdownBox creates a dropdown
widget that lets the user select the song they want similar songs to.
"""
import tkinter as tk
from typing import Union
import app_data as ad
import final_window
from app_data import FILE_NAME

G, SONG_NAME_LIST, GENRE = ad.create_graph_without_edges(FILE_NAME)


class DragDropListbox(tk.Listbox):
    """
    This class creates a listbox which contains items that can be moved through drag and drop. It is a child class
    that inherits the Listbox widget built into the tkinter module. The list box module creates a box with ordered
    items. This child class lets the user move it around.

    Instance Attributes:
        - cur_index: An index value that holds the position of the current clicked on item in the listBox
        - attributes_with_weights: At first this dictionary is empty, but later it will be filled with weights that
            correspond to the song attributes that the user prioritized.

    """

    cur_index: Union[None, float]
    attributes_with_weights: dict = {}

    def __init__(self, root: tk.Tk, background: str) -> None:
        """
        Initializes a dragdroplistbox object that lets the user drag around the items in the listbox
        """
        super().__init__(root, bg=background, justify="center")
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)

        items = [
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

        selection = tk.Label(root, text="Please rank how you value these musical characteristics:",
                             font=('Times New Roman', 18))
        selection.pack(pady=10)

        for item in items:
            self.insert(tk.END, item.capitalize())
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.cur_index = None

    def set_current(self, event: tk.Event) -> None:
        """
        When the left mouse is clicked, this function gets called. It takes in the mouse y coordinate and assigns it to
        currIndex.
        """
        self.cur_index = self.nearest(event.y)

    def shift_selection(self, event: tk.Event) -> None:
        """
        gets the nearest position where the mouse is moved and then moves it down or above based on whether it is lesser
        or greater than the currIndex
        """

        i = self.nearest(event.y)
        if i < self.cur_index:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.cur_index = i
        elif i > self.cur_index:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.cur_index = i

    def save_prioritization(self) -> None:
        """
        Saves the prioritized items, and adds it to the attribute_with_weights dictionary with the attribute name as the
        key.
        """
        weight = 1
        prioritized_attributes = self.get(0, tk.END)
        for attribute_index in range(len(prioritized_attributes) - 1, -1, -1):
            self.attributes_with_weights[prioritized_attributes[attribute_index].lower()] = 10 ** weight
            weight += 1


class DropdownBox:
    """
    Creates a dropdown menu where the user can select songs

    Instance Attributes:
        - selected_song: A string value denoting the name of the song that the user picks through the dropdown menu.
        - root: The Tkinter Window.
        - value_inside: A string variable that will store the name of the song.
    """
    root: tk.Tk
    value_inside: tk.StringVar
    selected_song: str = "Oops!...I Did It Again"

    def __init__(self, root: tk.Tk) -> None:
        """
        initializes the DropdownBox object
        """
        self.root = root

        label = tk.Label(root, text="Select a Song:", font=('Times New Roman', 18))
        label.pack()

        options = SONG_NAME_LIST
        self.value_inside = tk.StringVar(root)
        self.value_inside.set(options[0])
        dropdown_menu = tk.OptionMenu(root, self.value_inside, *options)
        dropdown_menu.pack()

    def on_select(self) -> None:
        """
        Gets the chosen song, this function gets called when the calculate similar songs button is pressed, it takes the
        current selected song in the dropdown box and saves it to selected_song
        """
        self.selected_song = self.value_inside.get()


def save_all_information(root: tk.Tk, priority_list_object: DragDropListbox,
                         drag_drop_object: DropdownBox, explicit: bool) -> None:
    """
    saves all the information and adds the weighted edges to the graph, then the function sorts all the vertexes based
    on weight in descending order and gets the first 10 elements. After that the root is destroyed and the final window
    is called.
    """
    drag_drop_object.on_select()
    priority_list_object.save_prioritization()
    user_selected_song = G.return_and_save_chosen_song(drag_drop_object.selected_song)
    G.add_all_weighted_edges(chosen_song=user_selected_song,
                             prioritylist=priority_list_object.attributes_with_weights,
                             explicit=explicit)
    final_selected_songs = G.sort_weights(10)
    root.destroy()
    final_window.final_window(final_selected_songs, drag_drop_object.selected_song)


def main() -> None:
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    root.state('zoomed')
    root.title("MelodyMatcher")

    song_selection_object = DropdownBox(root)
    priority_list_object = DragDropListbox(root, "gray")

    checkbox_var = tk.BooleanVar()

    buttonframe = tk.Frame(root)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)
    buttonframe.columnconfigure(2, weight=1)

    dictionary = {"Genre?": [lambda: final_window.description('genre'), [0, 0]],
                  "Year Released?": [lambda: final_window.description('year released'), [0, 1]],
                  "Popularity?": [lambda: final_window.description('popularity'), [0, 2]],
                  "Danceability?": [lambda: final_window.description('danceability'), [1, 0]],
                  "Energy?": [lambda: final_window.description('energy'), [1, 1]],
                  "Key?": [lambda: final_window.description('key'), [1, 2]],
                  "Loudness?": [lambda: final_window.description('loudness'), [2, 0]],
                  "Mode?": [lambda: final_window.description('mode'), [2, 1]],
                  "Speechiness?": [lambda: final_window.description('speechiness'), [2, 2]],
                  "Acousticness?": [lambda: final_window.description('acousticness'), [3, 0]],
                  "Instrumentalness?": [lambda: final_window.description('instrumentalness'), [3, 1]],
                  "Valence?": [lambda: final_window.description('valence'), [3, 2]],
                  "Tempo?": [lambda: final_window.description('tempo'), [4, 0]],
                  "Explicit?": [lambda: final_window.description('explicit'), [4, 1]]}

    for item in dictionary:
        button = tk.Button(buttonframe, text=item, font=("Times New Roman", 18), command=dictionary[item][0])
        button.grid(row=dictionary[item][1][0], column=dictionary[item][1][1], sticky=tk.W + tk.E)

    buttonframe.pack(fill='x')

    checkbox = tk.Checkbutton(root, text="Explicit", variable=checkbox_var)
    checkbox.pack(pady=10)

    save_button = tk.Button(root, text="Calculate similar songs",
                            command=lambda: save_all_information(root,
                                                                 priority_list_object,
                                                                 song_selection_object,
                                                                 checkbox_var.get()))
    save_button.pack(pady=50)
    root.mainloop()


if __name__ == "__main__":
    main()
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'max-nested-blocks': 4
    })
