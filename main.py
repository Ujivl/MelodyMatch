import tkinter as tk

import customtkinter

import gui_file
import gui_file2


class HomeScreen:
    """
    Home screen class (Decide which way of music...
    """

    def __init__(self, root):
        self.root = root

        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(side=tk.TOP, fill=tk.X)

        self.title = tk.Label(self.title_frame, text="MelodyMatcher", font=("Times New Roman", 50))
        self.title.pack(side=tk.LEFT, padx=10, pady=10)

        self.image = tk.PhotoImage(file="MelodyMatcher.gif")
        self.image_resized = self.image.subsample(4, 4)
        self.label = tk.Label(self.title_frame, image=self.image_resized)
        self.label.pack(side=tk.RIGHT)

        text = ("Welcome to MelodyMatch! We will help you discover music that matches your melodic taste! You are"
                " given two options for how you would like to tell us your music preferences. Choose 'Manual' if you"
                " would rather get music recommendations based on your manually inputted musical characteristic"
                " preferences. Choose 'Automatic' if you rather get music recommendations based on your favourite song"
                " and how you rank musical characteristics")

        self.description = tk.Label(self.root, text=text, font=("Times New Roman", 18), wraplength=700)
        self.description.pack(side=tk.TOP, pady=10)

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        # self.button = tk.Button(self.buttonframe, text="Manual", font=("Times New Roman", 18),
        #                         command=self.open_project_one)
        self.button = customtkinter.CTkButton(master=self.buttonframe, text="Manual", font=("Times New Roman", 18),
                                command=self.open_project_one)
        self.button.grid(row=0, column=0, sticky=tk.W + tk.E)
        # self.button2 = tk.Button(self.buttonframe, text="Automatic", font=("Times New Roman", 18),
        #                          command=self.open_project_two)
        self.button2 = customtkinter.CTkButton(master=self.buttonframe, text="Automatic", font=("Times New Roman", 18),
                                 command=self.open_project_two)
        self.button2.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.buttonframe.pack(fill='x')

    def open_project_one(self):
        """
        Destroy home window, and call upon Gui_1
        """
        self.root.destroy()
        gui_file.main()

    def open_project_two(self):
        """
       Destroy home window, and call upon Gui_2
       """
        self.root.destroy()
        gui_file2.main()


def main():
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
