"""
file implementing the gui of the application
"""
import tkinter as tk
from typing import Union
from tkinter import Scale



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


class PrioritizeApp_1:
    """
`
    """

    def __init__(self, root):
        self.root = root

        # Initial list of items
        self.items = [
            "year released",
            "popularity",
            "danceability",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo",
            "genre"
        ]

        self.entries = {}

        for item in self.items:
            self.question_label = tk.Label(root, text=item)
            self.question_label.pack(padx=10, pady=5)
            #
            answer_entry = tk.Entry(root, width=50)
            answer_entry.pack(padx=10, pady=5)

            self.entries[item] = answer_entry

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=10)

    def submit_answer(self):
        all_answers = {item: entry.get() for item, entry in self.entries.items()}
        print(all_answers)

        print(verify(all_answers))

        if all([all_answers[key] != "" for key in all_answers.keys()]) and verify(all_answers):
            #NEW WINDOW to display the artists that they match with...
            self.open_new_window()

        else:
            print("please answer all questions")

    def save_prioritization(self):
        """
            Saves the prioritized items and prints them out for now, this will chance later.
            """
        attributes_with_weights = {}
        weight = 9
        prioritized_attributes = self.listbox.get(0, tk.END)
        for attribute in prioritized_attributes:
            attributes_with_weights[attribute] = weight
            weight -= 1
        print("Prioritized Items with weights: " + str(attributes_with_weights))


def verify(all_answers) -> bool:
    """
    Verify every input so it is correct...

    """
    verify_list = [] #NOT SURE?
    verify_list.append((all_answers["year released"].isdigit()
                        and 2010 <= int(all_answers["year released"]) <= 2020))

    print(verify_list)

    return all(verify_list)


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    PrioritizeApp_1(root)
    root.title("MelodyMatcher")
    root.geometry("400x700")
    root.mainloop()


if __name__ == "__main__":
    main()
