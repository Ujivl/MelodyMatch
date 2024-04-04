import tkinter as tk

import gui_file
import gui_file2


class HomeScreen:
    """
    The HomeScreen class is responsible for creating and managing the initial interface of the
    MelodyMatcher application. This interface is the main entry point for users to select their
    preferred method of receiving music recommendations.
    """

    def __init__(self, root):
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
    import python_ta

    #python_ta.check_all(config={
        #'max-line-length': 120,
        #'disable': ['E1136', 'W0221'],
        #'max-nested-blocks': 4
    #})
