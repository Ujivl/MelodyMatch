"""
This is the main module for the MelodyMatcher application, a graphical user interface designed
using Tkinter. It allows users to choose between a manual or an automatic method for inputting their
music preferences. This module sets up the main window, initializes the HomeScreen class, and handles the
main execution flow of the application.
"""

import tkinter as tk

import gui_file
import gui_file2


class HomeScreen:
    """
    The HomeScreen class is responsible for creating and managing the initial interface of the
    MelodyMatcher application. This interface is the main entry point for users to select their
    preferred method of receiving music recommendations.

    Instance Attributes:
        - root: The root Tkinter window.
        - image_resized: A resized photo image for display.
    """
    root: tk.Tk
    image_resized: tk.PhotoImage

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        title_frame = tk.Frame(self.root)
        title_frame.pack(side=tk.TOP, fill=tk.X)

        title = tk.Label(title_frame, text="MelodyMatcher", font=("Times New Roman", 50))
        title.pack(side=tk.LEFT, padx=10, pady=10)

        image = tk.PhotoImage(file="MelodyMatcher.gif")
        self.image_resized = image.subsample(4, 4)
        label = tk.Label(title_frame, image=self.image_resized)
        label.pack(side=tk.RIGHT)

        text = ("Welcome to MelodyMatch! We will help you discover music that matches your melodic taste! You are"
                " given two options for how you would like to tell us your music preferences. Choose 'Manual' if you"
                " would rather get music recommendations based on your manually inputted musical characteristic"
                " preferences. Choose 'Automatic' if you rather get music recommendations based on your favourite song"
                " and how you rank musical characteristics")

        description = tk.Label(self.root, text=text, font=("Times New Roman", 18), wraplength=700)
        description.pack(side=tk.TOP, pady=10)

        buttonframe = tk.Frame(self.root)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)

        button = tk.Button(buttonframe, text="Manual", font=("Times New Roman", 18),
                           command=self.open_project_one)
        button.grid(row=0, column=0, sticky=tk.W + tk.E)
        button2 = tk.Button(buttonframe, text="Automatic", font=("Times New Roman", 18),
                            command=self.open_project_two)
        button2.grid(row=0, column=1, sticky=tk.W + tk.E)

        buttonframe.pack(fill='x')

    def open_project_one(self) -> None:
        """
        Destroy home window, and call upon Gui_1
        """
        self.root.destroy()
        gui_file.main()

    def open_project_two(self) -> None:
        """
       Destroy home window, and call upon Gui_2
       """
        self.root.destroy()
        gui_file2.main()


def main() -> None:
    """
   The main function file, this is where the root and main window is called.
   """
    root = tk.Tk()
    HomeScreen(root)
    root.title("MelodyMatcher")
    root.geometry("750x600")
    root.mainloop()


if __name__ == "__main__":
    main()
