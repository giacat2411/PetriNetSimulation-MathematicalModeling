from tkinter import *
import tkinter.messagebox

from Item1_bi import Item1_bi
from Item1_bii import Item1_bii
from Item2 import Item2
from Item3 import Item3

class PetriLauncher:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)

        self.windows = ""

        self.createWidgets()

    def createWidgets(self):
        self.item1_bi_button = Button(self.master, width=16, padx=3, pady=3)
        self.item1_bi_button['text'] = "ITEM 1B.I"
        self.item1_bi_button['command'] = self.load_1b_i
        self.item1_bi_button.grid(row=0, column=0, padx=2, pady=2)

        self.item1_bii_button = Button(self.master, width=16, padx=3, pady=3)
        self.item1_bii_button['text'] = "ITEM 1B.II"
        self.item1_bii_button['command'] = self.load_1b_ii
        self.item1_bii_button.grid(row=0, column=1, padx=2, pady=2)

        self.item2_button = Button(self.master, width=16, padx=3, pady=3)
        self.item2_button['text'] = "ITEM 2"
        self.item2_button['command'] = self.load_2
        self.item2_button.grid(row=1, column=0, padx=2, pady=2)

        self.item3_button = Button(self.master, width=16, padx=3, pady=3)
        self.item3_button['text'] = "ITEM 3"
        self.item3_button['command'] = self.load_3
        self.item3_button.grid(row=1, column=1, padx=2, pady=2)

    def load_1b_i(self):
        if self.windows == "": 
            self.windows = Tk()
        elif self.app.isClosed == 1:
            self.windows = Tk()
        else:
            self.windows.destroy()
            self.windows = Tk()

        self.app = Item1_bi(self.windows)
        self.app.master.title("Item 1b.i - Assignment - Petri Net")
        self.windows.mainloop()

    def load_1b_ii(self):
        if self.windows == "": 
            self.windows = Tk()
        elif self.app.isClosed == 1:
            self.windows = Tk()
        else:
            self.windows.destroy()
            self.windows = Tk()

        self.app = Item1_bii(self.windows)
        self.app.master.title("Item 1b.ii - Assignment - Petri Net")
        self.windows.mainloop()

    def load_2(self):
        if self.windows == "": 
            self.windows = Tk()
        elif self.app.isClosed == 1:
            self.windows = Tk()
        else:
            self.windows.destroy()
            self.windows = Tk()

        self.app = Item2(self.windows)
        self.app.master.title("Item 2 - Assignment - Petri Net")
        self.windows.mainloop()

    def load_3(self):
        if self.windows == "": 
            self.windows = Tk()
        elif self.app.isClosed == 1:
            self.windows = Tk()
        else:
            self.windows.destroy()
            self.windows = Tk()

        self.app = Item3(self.windows)
        self.app.master.title("Item 3 - Assignment - Petri Net")
        self.windows.mainloop()

    def handler(self):
        if tkinter.messagebox.askokcancel("Quit app ?", "Are you sure to quit"):
            self.master.destroy()

if __name__ == "__main__":
    root = Tk()

    app = PetriLauncher(root)
    app.master.title("Assignment - Petri Net")

    root.mainloop()