import tkinter as tk
from typing import Union
from tkinter import Button

from gui_file import *
from gui_file2 import *


class HomeScreen:
    """
    Home screen class (Decide which way of music...
    """

    def __init__(self, root):
        self.root = root
        self.button = Button(self.root, text="Project 1", command=self.open_project_one)
        self.button2 = Button(self.root, text="Project 2", command=self.open_project_two)

        self.button.pack()
        self.button2.pack()

    def open_project_one(self):
        """
        Destroy home window, and call upon Gui_1
        """
        self.root.destroy()
        root = tk.Tk()
        PrioritizeApp_1(root)
        root.title("Idea1")
        root.geometry("400x700")
        root.mainloop()

    def open_project_two(self):
        """
       Destroy home window, and call upon Gui_2
       """
        self.root.destroy()
        root = tk.Tk()
        drag_drop_object = DropdownApp(root)
        priority_list = PrioritizeApp(root)
        explicit = False

        root.title("MelodyMatcher")
        root.geometry("400x500")

        save_button = tk.Button(root, text="Calculate similar songs",
                                command=lambda: save_all_information(priority_list, drag_drop_object, explicit))
        save_button.pack(pady=50)

        root.mainloop()


def main():
    """
   The main function file, this is where the root and main window is called.
   """
    root = tk.Tk()
    HomeScreen(root)
    root.title("MelodyMatcher")
    root.geometry("400x700")
    root.mainloop()


if __name__ == "__main__":
    main()
