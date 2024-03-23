"""
file implementing the gui of the application
"""
import tkinter as tk

class DragDropListbox(tk.Listbox):
    """A Listbox with drag-and-drop reordering of items"""

    def __init__(self, root, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, root, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        """Set the current item to the one clicked on"""
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        """Shift the current item to a new position"""
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
    doing something right now i dont really knwo right now
    """
    def __init__(self, master):
        self.master = master

        # Initial list of items
        self.items = [f"Item {i}" for i in range(1, 11)]

        # Create a DragDropListbox and fill it with items
        self.listbox = DragDropListbox(master, exportselection=0, bg="gray")
        for item in self.items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button to save prioritization
        self.save_button = tk.Button(master, text="Save Prioritization", command=self.save_prioritization)
        self.save_button.pack(pady=5)

    def save_prioritization(self):
        # Get prioritized items and print them
        prioritized_items = self.listbox.get(0, tk.END)
        print("Prioritized Items:", prioritized_items)

def main():
    # Create the tkinter window and PrioritizeApp instance
    root = tk.Tk()
    PrioritizeApp(root)
    root.title("MelodyMatcher")
    root.geometry("600x800")
    root.mainloop()

if __name__ == "__main__":
    main()
