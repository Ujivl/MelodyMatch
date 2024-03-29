import tkinter as tk
from typing import Union
from typing import Union
import app_data as ad


class FinalWindow:
    def __init__(self, root, top_song):
        self.root = root

        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(side=tk.TOP, fill=tk.X)

        self.title = tk.Label(self.title_frame, text="Songs", font=("Times New Roman", 50))
        self.title.pack(side=tk.TOP, padx=10, pady=10)

        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(side=tk.TOP, pady=10)

        listbox = tk.Listbox(listbox_frame, width=50, height=10)
        for song in top_song:
            listbox.insert(tk.END, song.item.song_name)

        listbox.pack()
