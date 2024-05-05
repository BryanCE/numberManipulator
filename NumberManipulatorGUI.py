import tkinter as tk
from tkinter import *
import ctypes
from help_utils import *
from areaCodes import stateByAreaCode
from dedupe import deDupe, feed_next_number, full_list_to_clipboard
from badnumdel import badNumDel


def on_return(event):
    # Call your function to process the area code
    badNumDel(inEntryDelete, onOff, root)
    deDupe(inEntryDeDup, possibleStatesLbl, onOff, root)
    stateByAreaCode(inEntryAreaCode)
    return 'break'  # Prevents the default behavior of the Enter key

# Help window
def show_instructions():
    help_window = tk.Toplevel(root)
    create_instructions_notebook(help_window)

def show_hotkeys():
    hotkey_window = tk.Toplevel(root)
    create_hotkeys_notebook(hotkey_window)


# Create the main window
root = tk.Tk()
root.title("NumberManipulator GUI")

# binding for number feed
root.bind('<Control-f>', feed_next_number)

# binding for control + f + a to feed all numbers
root.bind('<Control-Shift-F>', full_list_to_clipboard)

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a "Help" menu
help_menu = tk.Menu(menu_bar)
help_menu.add_command(label="Instructions", command=show_instructions)
help_menu.add_command(label="HotKeys", command=show_hotkeys)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the root window to use the menu bar
root.config(menu=menu_bar)

# frame for area code and auto minimize check box
areaCodeAndMinFrame = tk.Frame(root)

# Text input field for Area Code Checker
inLabelAreaCode = tk.Label(areaCodeAndMinFrame, text="Check Area Code")
inEntryAreaCode = tk.Text(areaCodeAndMinFrame, height=1, width=10)
inEntryAreaCode.bind("<Return>", on_return)
outLabelAreaCode = tk.Label(areaCodeAndMinFrame)


# Text input field for DeDupe
inLabelDeDup = tk.Label(root, text="DeDupe")
#inLabelDeDup.pack(padx=5, pady=2)

inEntryDeDup = tk.Text(root, height=10)
inEntryDeDup.bind("<Return>", on_return)

#Label to display all possible states with area codes from DeDup
possibleStatesLbl = tk.Label(root)


# Text input field for bad number Deleter
inLabelDelete = tk.Label(root, text="Clean Numbers")


inEntryDelete = tk.Text(root, height=10)
inEntryDelete.bind("<Return>", on_return)


# make a check box to turn auto minimizing on and off
onOff = tk.IntVar()
autoMin = tk.Checkbutton(
    root, text="Auto Minimize ON/OFF", variable=onOff, onvalue=1, offvalue=0
)


# Create a frame to contain the button
exitBtnFrame = tk.Frame(root)
exitBtn = tk.Button(exitBtnFrame, text="Exit", height=2, width=30, command=root.destroy)
exitBtn.pack(expand=True, fill="both")


# inLabelAreaCode
# inEntryAreaCode 
# outLabelAreaCode 

# Layout in frame using grid
inLabelAreaCode.grid(row=0, column=0, padx=10, pady=2, sticky="w")
inEntryAreaCode.grid(row=0, column=1, padx=10, pady=5, sticky="w")
autoMin.grid(row=0, column=2, columnspan=1, padx=(0, 30), pady=(0, 30), sticky="w")
outLabelAreaCode.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="e")


inLabelDeDup.grid(row=2, column=0, padx=10, pady=2, sticky="w")
inEntryDeDup.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
possibleStatesLbl.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

inLabelDelete.grid(row=4, column=0, padx=10, pady=2, sticky="w")
inEntryDelete.grid(row=4, column=1, padx=10, columnspan=3, pady=5, sticky="ew")

#Frame to hold the area code and auto minimize check box
areaCodeAndMinFrame.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")
exitBtnFrame.grid(row=6, column=0, columnspan=3, pady=10)


# Configure column and row weights for resizing
areaCodeAndMinFrame.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)


# auto minimized the console window
ctypes.windll.user32.ShowWindow(
    ctypes.windll.kernel32.GetConsoleWindow(), 6
)  # 6 = SW_MINIMIZE
# info on .ShowWindow here:
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN


root.mainloop()