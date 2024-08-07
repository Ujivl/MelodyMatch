"""
The final window file is responsible for creating the final window of the application. This is where 10 similar songs
are diplayed to the user, FinalListBox is a class here that displays the 10 songs, and when the user clicks on a song,
information about the song is displayed under the listbox.
"""
import tkinter as tk
import app_data as ad


class FinalListBox(tk.Listbox):
    """
    This class implements a listbox that inherits from the built-in listbox widget. This widget lets the user click on
    the items, which in turn displays information about the songs.

    Instance Attributes:
        songs: A list of songs that are most similar to the user selected songs or attributes.
        output_text: a text widget that displays all the information about the song the user clicks on.
    """
    songs: list[ad.Song]
    output_text: tk.Text

    def __init__(self, root: tk.Tk, background: str, songs: list[ad.Song], output_text: tk.Text) -> None:
        """
        Initializes the finallistbox object.
        """
        super().__init__(root, bg=background, width=50, justify="center")
        self.songs = songs
        self.bind('<Button-1>', self.display_info)
        self.output_text = output_text
        for song in self.songs:
            self.insert(tk.END, song.song_name)

    def display_info(self, event: tk.Event) -> None:
        """
        This function is called when the left mouse button clicked. It fills a text box with information about the song
        that was clicked on.
        """
        i = self.nearest(event.y)
        chosen_song = self.songs[i]
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        song_info = f"Song Name: {chosen_song.song_name}\nArtist: {chosen_song.artist}"
        for i in chosen_song.similarity_factors:
            song_info += f"\n{i}: {chosen_song.similarity_factors[i]}"
        self.output_text.insert(tk.END, song_info)
        self.output_text.config(state="disabled")
        self.output_text.pack(pady=10)


def final_window(top_songs: list[ad.Song], selected_song: str) -> None:
    """
    This function is called after the similar songs are calculated. It is essentially the last function being called in
    the application. It creates the root for the final window and packs all the widgets.
    """
    root = tk.Tk()
    root.title("Top 10 songs")
    root.geometry("600x600")

    label = tk.Label(root, text=f"10 songs that are similar to: {selected_song}", font=('Times New Roman', 18))
    label.pack(pady=10)
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(side=tk.TOP, pady=10)

    textbox = tk.Text(root, width=70, height=100, wrap="word")
    listbox = FinalListBox(root, background="gray", songs=top_songs, output_text=textbox)
    listbox.pack()
    root.mainloop()


def description(item: str) -> None:
    """
    This function creates a temporary window that displays information about the attribute that the user clicked [item].
    """
    root = tk.Tk()
    root.title(item)
    root.geometry('600x100')

    dictionary = {'genre': 'This is the genre of the song. This is considered to be the category the song is in.',
                  'year released': 'This is the release year of the song.',
                  'popularity': 'This is how well-known the song is. The higher the value,'
                                ' the more popular the song is.',
                  'danceability': "This is the song's ability to be used to "
                                  "dance. A value of 0.0 is least danceable and 1.0 is most "
                                  "danceable",
                  'energy': 'This represents the measure of intensity and activity of the song.',
                  'key': 'This is the key the track is in. ',
                  'loudness': 'This is the overall loudness of the song in decibels (dB).',
                  'mode': 'This represents the modality (major or minor) of the song.',
                  'speechiness': 'Speechiness detects the presence of spoken words in a song.',
                  'acousticness': 'A measure from 0.0 to 1.0 representing whether the song is acoustic.',
                  'instrumentalness': 'This predicts whether the song contains no vocals.',
                  'valence': 'A measure from 0.0 to 1.0 representing the musical positiveness shown by the song.',
                  'explicit': 'This asks whether the song contains curse words or not.',
                  'tempo': 'The estimated tempo of the song in beats per minute (BPM).'
                  }

    text = dictionary[item]

    title = tk.Label(root, text=item.upper(), font=("Times New Roman", 30))
    title.pack()

    label = tk.Label(root, text=text, font=("Times New Roman", 18), wraplength=500)
    label.pack()

    root.mainloop()
