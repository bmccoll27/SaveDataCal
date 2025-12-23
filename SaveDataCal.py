from tkinter import *
from tkinter import ttk
import tkinter


def fsaveDataLimit(*args):
    try:
        if tier.get() != "0":
            saveDataLimit.set(int(tier.get()) * 10 + 20)
        if deepTrauma.get():
            saveDataLimit.set(int(saveDataLimit.get()) + 10)

    except ValueError:
        saveDataLimit.set("")
        pass


root = Tk()
root.title("Save Data Cal")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tier = StringVar()
tier_entry = ttk.Entry(mainframe, width=7, textvariable=tier)
tier_entry.grid(column=2, row=1, sticky=(E, W))
ttk.Label(mainframe, text="Save Data Value").grid(column=1, row=1, sticky=E)

deepTrauma = tkinter.BooleanVar(value=False)
ttk.Checkbutton(root, text="Deep Trauma", variable=deepTrauma).grid(
    column=1, row=2, sticky=W)

ttk.Button(mainframe, text="Calculate", command=fsaveDataLimit).grid(
    column=2, row=2, sticky=W)

saveDataLimit = StringVar()
ttk.Label(mainframe, textvariable=saveDataLimit).grid(
    column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Save Data Limit: ").grid(
    column=1, row=3, sticky=(W, E))


root.bind("<Return>", fsaveDataLimit)
root.mainloop()
