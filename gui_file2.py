"""
file implementing the gui of the application
"""
import tkinter as tk
from typing import Union
import app_data as ad
from final_window import FinalWindow

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
        super().__init__(root, bg=background)
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
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


class PrioritizeApp:
    """
    doing something right now i dont really know right now
    """

    attributes_with_weights: dict[str, int]

    def __init__(self, root):
        self.root = root

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

        # Create a DragDropListbox and fill it with items
        self.listbox = DragDropListbox(root, "gray")
        for item in self.items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.attributes_with_weights = {}

    def save_prioritization(self):
        """
        Saves the prioritized items and prints them out for now, this will chance later.
        """
        weight = 1
        prioritized_attributes = self.listbox.get(0, tk.END)
        for attribute_imdex in range(len(prioritized_attributes) - 1, -1, -1):
            self.attributes_with_weights[prioritized_attributes[attribute_imdex]] = (10 ** weight)
            weight += 1
        print("Prioritized Items with weights: " + str(self.attributes_with_weights))


class DropdownApp:
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
        self.dropdown_menu.pack()

        self.selection = tk.Label(root, text="Please rank how you value these musical characteristics:",
                                  font=('Times New Roman', 18))
        self.selection.pack(pady=10)

    def on_select(self):
        self.selected_song = self.value_inside.get()


def save_all_information(root, priority_list: PrioritizeApp, drag_drop_object: DropdownApp, explicit: bool):
    """
    saves all the information and adds the weighted edges to the graph
    """
    drag_drop_object.on_select()
    priority_list.save_prioritization()
    user_selected_song = g.return_and_save_chosen_song(drag_drop_object.selected_song)
    g.add_all_weighted_edges(chosen_song=user_selected_song,
                             prioritylist=priority_list.attributes_with_weights,
                             explicit=explicit)
    final_selected_songs = g.sort_weights(10)
    root.destroy()
    new_root = tk.Tk()
    FinalWindow(new_root, final_selected_songs)
    new_root.title("FinalWindow")
    new_root.geometry("400x700")
    new_root.mainloop()


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    drag_drop_object = DropdownApp(root)
    priority_list = PrioritizeApp(root)
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text="Explicit", variable=checkbox_var)
    checkbox.pack(pady=10)
    root.title("MelodyMatcher")
    root.geometry("450x500")

    save_button = tk.Button(root, text="Calculate similar songs",
                            command=lambda: save_all_information(root, priority_list, drag_drop_object, checkbox_var.get()))
    save_button.pack(pady=50)

    root.mainloop()


if __name__ == "__main__":
    main()
