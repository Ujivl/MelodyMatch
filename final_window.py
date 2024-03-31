import tkinter as tk
import app_data as ad


class FinalListBox(tk.Listbox):
    """
    This class creates a listbox which contains items that can be moved through drag and drop. It is a child class
    that inherits the Listbox widget built into the tkinter module. The list box module creates a box with ordered
    items. This child class lets the user move it around.

    Instance Attributes:
        - curIndex

    """

    def __init__(self, root: tk.Tk, background: str, songs:  list[ad.Song], output_text: tk.Text):
        """
        Initializes a dragdroplistbox object that lets the user drag around the items in the listbox
        """
        super().__init__(root, bg=background)
        self.songs = songs
        self.bind('<Button-1>', self.display_info)
        self.output_text = output_text
        for song in self.songs:
            self.insert(tk.END, song.song_name)

    def display_info(self, event):
        """
        When the left mouse is clicked, this function gets called. It takes in the mouse y coordinate and assigns it to
        currIndex.
        """
        i = self.nearest(event.y)
        chosen_song = self.songs[i]
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Artist: {chosen_song.artist}")
        self.output_text.insert(tk.END, f"\nyear released: {chosen_song.similarity_factors["year released"]}")
        self.output_text.config(state="disabled")
        self.output_text.pack(pady=10)


def final_window(top_songs):
    """
    blah
    """
    root = tk.Tk()
    root.title("Top 10 songs")
    root.geometry("400x700")

    title_frame = tk.Frame(root)
    title_frame.pack(side=tk.TOP, fill=tk.X)

    title = tk.Label(title_frame, text="Songs", font=("Times New Roman", 50))
    title.pack(side=tk.TOP, padx=10, pady=10)

    listbox_frame = tk.Frame(root)
    listbox_frame.pack(side=tk.TOP, pady=10)

    textbox = tk.Text(root, width=40, height=5, wrap="word")
    listbox = FinalListBox(root, background="gray", songs=top_songs, output_text=textbox)
    listbox.pack()
    root.mainloop()
