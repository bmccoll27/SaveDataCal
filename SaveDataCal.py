from tkinter import *
from tkinter import ttk
import deck
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


def create_deck():
    global current_deck, deck_count_label
    current_deck = deck.Deck()
    deck_count_label.config(
        text=f"Deck created with {current_deck.card_count()} cards")
    # enable the single Add Card button (created once below)
    try:
        add_card_button.config(state="normal")
    except NameError:
        pass
    refresh_card_list()


root = Tk()
root.title("Save Data Cal")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

tier = StringVar()
tier_entry = ttk.Entry(mainframe, width=7, textvariable=tier)
tier_entry.grid(column=2, row=1, sticky=(E, W))
ttk.Label(mainframe, text="Save Data Value: ").grid(column=1, row=1, sticky=E)

deepTrauma = tkinter.BooleanVar(value=False)
ttk.Checkbutton(mainframe, text="Deep Trauma", variable=deepTrauma).grid(
    column=1, row=2, sticky=W)

ttk.Button(mainframe, text="Calculate", command=fsaveDataLimit).grid(
    column=2, row=2, sticky=W)

saveDataLimit = StringVar()
ttk.Label(mainframe, textvariable=saveDataLimit).grid(
    column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Save Data Limit: ").grid(
    column=1, row=3, sticky=(W, E))


ttk.Label(mainframe, text="Deck Management: ").grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Create Deck", command=create_deck).grid(
    column=2, row=4, sticky=W)

# Card input controls
card_name = StringVar()
ttk.Label(mainframe, text="Card Name:").grid(column=1, row=5, sticky=E)
ttk.Entry(mainframe, width=7, textvariable=card_name).grid(
    column=2, row=5, sticky=(E, W))

card_cost = StringVar()
ttk.Label(mainframe, text="Card Cost:").grid(column=1, row=6, sticky=E)
ttk.Entry(mainframe, width=7, textvariable=card_cost).grid(
    column=2, row=6, sticky=(E, W))

card_tier = StringVar()
ttk.Label(mainframe, text="Card Tier:").grid(column=1, row=7, sticky=E)
ttk.Entry(mainframe, width=7, textvariable=card_tier).grid(
    column=2, row=7, sticky=(E, W))


card_flag = StringVar(value='None')
ttk.Label(mainframe, text="Epiphany:").grid(column=1, row=9, sticky=E)
ttk.Combobox(mainframe, values=["None", "Epiphany", "Divine Epiphany"], textvariable=card_flag, state="readonly").grid(
    column=2, row=9, columnspan=2, sticky=(W, E))
card_dupe = tkinter.BooleanVar(value=False)
ttk.Checkbutton(mainframe, text="Duplicate",
                variable=card_dupe).grid(column=4, row=9, sticky=W)

# Deck state and helper UI
current_deck = None
deck_count_label = ttk.Label(mainframe, text="No deck created")
deck_count_label.grid(column=1, row=11, columnspan=2, sticky=(W, E))
ttk.Label(mainframe, text="""Card Tiers: 
1 = Character Unique cards
2 = Common cards
3 = Monster cards 
4 = Forbidden cards""").grid(
    column=1, row=10, sticky=W)

# Single Add Card button (created once, enabled after deck creation)
add_card_button = ttk.Button(
    mainframe, text="Add Card", command=lambda: add_card_from_gui(), state="disabled")
add_card_button.grid(column=3, row=6, sticky=W)

# Edit / Delete / Remove buttons
edit_card_button = ttk.Button(
    mainframe, text="Edit Selected", command=lambda: edit_selected_card(), state="normal")
edit_card_button.grid(column=1, row=14, sticky=W)
convert_card_button = ttk.Button(
    mainframe, text="Convert Selected", command=lambda: convert_selected_card(), state="normal")
convert_card_button.grid(column=4, row=14, sticky=W)
delete_card_button = ttk.Button(
    mainframe, text="Delete Selected", command=lambda: delete_selected_card(), state="normal")
delete_card_button.grid(column=2, row=14, sticky=W)
remove_card_button = ttk.Button(
    mainframe, text="Remove Selected", command=lambda: remove_selected_card(), state="normal")
remove_card_button.grid(column=3, row=14, sticky=W)

# Listbox showing cards in current deck and average cost
card_listbox = Listbox(mainframe, height=8)
card_listbox.grid(column=1, row=12, columnspan=3, sticky=(W, E))

avg_cost_label = ttk.Label(mainframe, text="Avg cost: 0")
avg_cost_label.grid(column=1, row=13, columnspan=2, sticky=W)

faint_memory_label = ttk.Label(mainframe, text="Faint Memory: N/A")
faint_memory_label.grid(column=3, row=13, sticky=W)


def refresh_card_list():
    """Refresh the listbox and average cost label from the current deck."""
    if current_deck is None:
        card_listbox.delete(0, END)
        avg_cost_label.config(text="Avg cost: 0")
        return
    card_listbox.delete(0, END)
    for i, c in enumerate(current_deck.cards, 1):
        card_listbox.insert(
            END, f"{i}: {c.name} (cost {c.cost}, tier {c.tier})")
    avg = current_deck.get_avg_cost()
    try:
        avg_cost_label.config(text=f"Avg cost: {avg:.2f}")
        faint_memory_label.config(
            text=f"Faint Memory: {current_deck.saveDataValue}")
    except Exception:
        avg_cost_label.config(text=f"Avg cost: {avg}")


def add_card_from_gui():
    global current_deck
    if current_deck is None:
        deck_count_label.config(text="Create a deck first")
        return
    try:
        name = str(card_name.get())
        cost = int(card_cost.get())
        tier_val = int(card_tier.get())
        ep = (card_flag.get() == 'Epiphany')
        de = (card_flag.get() == 'Divine Epiphany')
    except ValueError:
        deck_count_label.config(text="Invalid card input")
        return
    dup = bool(card_dupe.get())
    try:
        current_deck.add_card(name, cost, tier_val, ep, de, duplicate=dup)
    except ValueError:
        deck_count_label.config(text="Tier 0 cards are not allowed")
        return
    deck_count_label.config(text=f"Deck has {current_deck.card_count()} cards")
    refresh_card_list()


def get_selected_card():
    """Return (index, card) for the currently selected listbox item, or (None, None)."""
    sel = card_listbox.curselection()
    if not sel:
        return None, None
    idx = sel[0]
    if current_deck is None or idx >= len(current_deck.cards):
        return None, None
    return idx, current_deck.cards[idx]


def delete_selected_card():
    """Delete a card due to user error (no deck penalty)."""
    global current_deck
    idx, card = get_selected_card()
    if card is None:
        deck_count_label.config(text="Select a card to delete")
        return
    # remove without calling Deck.remove_card (no penalty)
    try:
        if card.tier == 0:
            deck_count_label.config(text="Cannot delete tier 0 cards")
            return
        del current_deck.cards[idx]
    except Exception:
        deck_count_label.config(text="Failed to delete card")
        return
    deck_count_label.config(text=f"Deck has {current_deck.card_count()} cards")
    current_deck.reload_save_data()
    refresh_card_list()


def remove_selected_card():
    """Remove a card following deck policy (calls Deck.remove_card)."""
    global current_deck
    idx, card = get_selected_card()
    if card is None:
        deck_count_label.config(text="Select a card to remove")
        return
    try:
        current_deck.remove_card(card)
    except Exception:
        deck_count_label.config(text="Failed to remove card")
        return
    deck_count_label.config(text=f"Deck has {current_deck.card_count()} cards")
    refresh_card_list()


def edit_selected_card():
    """Open a popup to edit the selected card's properties."""
    idx, card = get_selected_card()
    if card is None:
        deck_count_label.config(text="Select a card to edit")
        return
    if card.tier == 0:
        deck_count_label.config(text="Cannot edit tier 0 cards")
        return
    win = Toplevel(root)
    win.title(f"Edit Card {idx+1}")

    e_name = StringVar(value=str(card.name))
    e_cost = StringVar(value=str(card.cost))
    e_tier = StringVar(value=str(card.tier))
    # use a combobox for mutually exclusive epiphany flags (display labels)
    e_flag = StringVar(value=('Epiphany' if card.epiphany else (
        'Divine Epiphany' if card.divineEpiphany else 'None')))
    # keep Duplicate as an independent Checkbutton to match main UI
    e_dup = tkinter.BooleanVar(value=bool(getattr(card, 'duplicate', False)))

    ttk.Label(win, text="Name:").grid(column=1, row=1, sticky=E)
    ttk.Entry(win, textvariable=e_name).grid(column=2, row=1, sticky=(W, E))
    ttk.Label(win, text="Cost:").grid(column=1, row=2, sticky=E)
    ttk.Entry(win, textvariable=e_cost).grid(column=2, row=2, sticky=(W, E))
    ttk.Label(win, text="Tier:").grid(column=1, row=3, sticky=E)
    ttk.Entry(win, textvariable=e_tier).grid(column=2, row=3, sticky=(W, E))
    ttk.Label(win, text="Epiphany:").grid(column=1, row=4, sticky=E)
    ttk.Combobox(win, values=["None", "Epiphany", "Divine Epiphany"], textvariable=e_flag, state="readonly").grid(
        column=2, row=4, sticky=(W, E))
    ttk.Checkbutton(win, text="Duplicate", variable=e_dup).grid(
        column=1, row=5, sticky=W)

    def save_edits():
        try:
            card.name = str(e_name.get())
            card.cost = int(e_cost.get())
            card.tier = int(e_tier.get())
            card.epiphany = (e_flag.get() == 'Epiphany')
            card.divineEpiphany = (e_flag.get() == 'Divine Epiphany')
            card.duplicate = bool(e_dup.get())
        except ValueError:
            deck_count_label.config(text="Invalid input in edit")
            return
        current_deck.reload_save_data()
        refresh_card_list()
        deck_count_label.config(text=f"Edited card {idx+1}")
        win.destroy()

    ttk.Button(win, text="Save", command=save_edits).grid(
        column=2, row=6, sticky=E)


def convert_selected_card():
    idx, card = get_selected_card()
    if card is None:
        deck_count_label.config(text="Select a card to convert")
        return
    win = Toplevel(root)
    win.title(f"Convert Card {idx+1}")
    c_name = StringVar(value=str(card.name))
    c_cost = StringVar(value=str(card.cost))
    c_flag = StringVar(value=('Epiphany' if card.epiphany else (
        'Divine Epiphany' if card.divineEpiphany else 'None')))
    c_dup = tkinter.BooleanVar(value=bool(getattr(card, 'duplicate', False)))
    ttk.Label(win, text="Name:").grid(column=1, row=1, sticky=E)
    ttk.Entry(win, textvariable=c_name).grid(column=2, row=1, sticky=(W, E))
    ttk.Label(win, text="Cost:").grid(column=1, row=2, sticky=E)
    ttk.Entry(win, textvariable=c_cost).grid(column=2, row=2, sticky=(W, E))
    ttk.Label(win, text="Epiphany:").grid(column=1, row=3, sticky=E)
    ttk.Combobox(win, values=["None", "Epiphany", "Divine Epiphany"], textvariable=c_flag, state="readonly").grid(
        column=2, row=3, sticky=(W, E))
    ttk.Checkbutton(win, text="Duplicate", variable=c_dup).grid(
        column=1, row=4, sticky=W)

    def save_conversion():
        try:
            card.name = str(c_name.get())
            card.cost = int(c_cost.get())
            card.epiphany = (c_flag.get() == 'Epiphany')
            card.divineEpiphany = (c_flag.get() == 'Divine Epiphany')
            card.duplicate = bool(c_dup.get())
        except ValueError:
            deck_count_label.config(text="Invalid input in conversion")
            return
        current_deck.card_conversion_points(card)
        refresh_card_list()
        deck_count_label.config(text=f"Converted card {idx+1}")
        win.destroy()
    ttk.Button(win, text="Convert", command=save_conversion).grid(
        column=2, row=5, sticky=E)


root.bind("<Return>", fsaveDataLimit)
root.mainloop()
