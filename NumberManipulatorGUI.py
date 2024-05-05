import tkinter as tk
from tkinter import *

import pyperclip
import re
import ctypes
import csv
from help_utils import *

# CSV file path
csvAreaCodes = r"NpasInSvcByLocRpt.csv"
feedNums = []
current_index = 0
cycled = True

def extractAreaCode(number):
    return number[:3]

# Function to check for a state based on an area code
def stateByAreaCode(arg):
    with open(csvAreaCodes, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        areaCode = inEntryAreaCode.get("1.0", "end-1c")
        areaCode = areaCode.replace("\n", "")
        state = ""
        for row in csv_reader:
            if row['NPA'] == areaCode:
                state = row["Location"]
                break
        if state == "":
            # clear out the input
            inEntryAreaCode.delete("1.0", "end")
            outLabelAreaCode.config(text="No state with that Area Code")
        else:
            # clear out the input
            inEntryAreaCode.delete("1.0", "end")
            outLabelAreaCode.config(text=state)

# Check for all states associated with ALL codes passed in
def statesByCodes(areaCodes):
    with open(csvAreaCodes, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        states = []
        for row in csvReader:
            for code in areaCodes:
                if row['NPA'] == code and row['Location'] not in states:
                    states.append(row['Location'])

    if len(states) == 0:
        return ["No state with that area code!\n"]
    else:
        return states


def rm_duplicates_in_order(numbers):
    unique_numbers = []
    seen_numbers = set()

    for number in numbers:
        if number not in seen_numbers:
            unique_numbers.append(number)
            seen_numbers.add(number)

    return unique_numbers


def remove_chars(input_string):
    # Trying to get rid of pesky spaces
    pattern = r"(\(\d+\)) (\d+)"
    input_string = re.sub(pattern, r"\1\2", input_string)
    # Then remove unneeded chars
    removeThese = ["-", "(", ")", ".", "Click to dial", "disabled"]
    for thing in removeThese:
        input_string = input_string.replace(thing, "")
    return input_string


def filter_notes(phone_numbers, words_to_remove):
    filtered_numbers = []

    # Iterate through the list of phone numbers with notes
    for entry in phone_numbers:
        # Split into phone number and note
        phone_parts = entry.split(" ", 1)

        if len(phone_parts) == 2:
            phone_number, note = phone_parts

            # Deletes any number that has a bad word in notes
            # Currently, it's "bad" and "wrong number"
            if not any(word in note.lower() for word in words_to_remove):
                filtered_numbers.append(phone_number)
        else:
            # If there is no note, add the number to the list
            filtered_numbers.append(entry)

    return filtered_numbers


def badNumDel(arg):
    # Keywords that remove numbers
    wordsToRemove = ["bad", "wrong"]

    inputText = inEntryDelete.get("1.0", "end-1c")
    inputText = remove_chars(inputText)
    inputText = inputText.replace("\\n", "\n")
    lines = inputText.split("\n")

    # clear out the input
    inEntryDelete.delete("1.0", "end")

    cleanNums = filter_notes(lines, wordsToRemove)

    filteredOutput = " ".join(f"{num}" for num in cleanNums)

    pyperclip.copy(filteredOutput)

    # try to make auto minimize only happen when check box is clicked
    if onOff.get() == 1:
        root.wm_state("iconic")


def deDupe(arg):
    global current_index, feedNums, cycled
    input_text = inEntryDeDup.get("1.0", "end-1c")
    lines = input_text.split("\n")

    # clear out the input
    inEntryDeDup.delete("1.0", "end")

    cleanNums = []
    for line in lines:
        line = remove_chars(line)
        numbers = line.split()
        cleanNums.extend(numbers)

    uniqNums = rm_duplicates_in_order(cleanNums)

    #globals to deal with feeding numbers to clipboard
    cycled = False
    feedNums = uniqNums
    current_index = 0

    # check states here for area code possibilities
    # Iterate through the list of phone numbers and find the regions
    allAreaCodes = []
    for num in uniqNums:
        code = extractAreaCode(num)
        #add only new area codes
        if code not in allAreaCodes:
            allAreaCodes.append(code)

    #send to check all the codes and display possible states
    possibleStates = statesByCodes(allAreaCodes)
    #add states to Label
    posStates = " ".join(f"{st}, " for st in possibleStates)
    possibleStatesLbl.config(text=("Possible States: " + posStates))

    outPut = format_hyphen(uniqNums)

    # copy the formatted list to the clipboard
    copy_formatted_list(outPut)

    # make auto minimize only happen when check box is clicked
    if onOff.get() == 1:
        root.wm_state("iconic")


def format_hyphen(nums):
    return "\n".join(f"{num} - " for num in nums)

def format_newline(nums):
    return "\n".join(f"{num}" for num in nums)

def copy_formatted_list(outPut):
    if outPut:
        pyperclip.copy(outPut)


def full_list_to_clipboard(arg):
    global feedNums
    if len(feedNums) > 0:
        pyperclip.copy(format_newline(feedNums))


def feed_next_number(arg):
    global current_index, feedNums, cycled
    if not cycled and current_index < len(feedNums):
        pyperclip.copy(feedNums[current_index])
        current_index += 1
    else:
        current_index = 0
        cycled = True
        pyperclip.copy('')

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
inEntryAreaCode = tk.Text(areaCodeAndMinFrame, height=1, width=20)
inEntryAreaCode.bind("<Return>", stateByAreaCode)
outLabelAreaCode = tk.Label(areaCodeAndMinFrame)


# Text input field for DeDupe
inLabelDeDup = tk.Label(root, text="DeDupe")
#inLabelDeDup.pack(padx=5, pady=2)

inEntryDeDup = tk.Text(root, height=10)
inEntryDeDup.bind("<Return>", deDupe)
#inEntryDeDup.pack(fill=BOTH, expand=YES, padx=10, pady=5)

#Label to display all possible states with area codes from DeDup
possibleStatesLbl = tk.Label(root)
#possibleStatesLbl.pack(fill=BOTH, expand=YES, padx=10, pady=5)


# Text input field for bad number Deleter
inLabelDelete = tk.Label(root, text="Clean Numbers")
#inLabelDelete.pack(padx=10, pady=2)

inEntryDelete = tk.Text(root, height=10)
inEntryDelete.bind("<Return>", badNumDel)
#inEntryDelete.pack(fill=BOTH, expand=YES, padx=10, pady=5)



# make a check box to turn auto minimizing on and off
onOff = tk.IntVar()
autoMin = tk.Checkbutton(
    root, text="Auto Minimize ON/OFF", variable=onOff, onvalue=1, offvalue=0
)

#autoMin.pack(fill=BOTH, expand=YES, padx=2, pady=1)


# Create a frame to contain the button
exitBtnFrame = tk.Frame(root)
exitBtn = tk.Button(exitBtnFrame, text="Exit", height=2, width=30, command=root.destroy)
exitBtn.pack(expand=True, fill="both")

# auto minimized the console window
ctypes.windll.user32.ShowWindow(
    ctypes.windll.kernel32.GetConsoleWindow(), 6
)  # 6 = SW_MINIMIZE
# info on .ShowWindow here:
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN

#Frame to hold the area code and auto minimize check box
areaCodeAndMinFrame.grid(row=0, column=0, columnspan=2, pady=5)

# Layout using grid
inLabelAreaCode.grid(row=0, column=0, padx=10, pady=2, sticky="w")
inEntryAreaCode.grid(row=0, column=1, padx=10, pady=5, sticky="w")
autoMin.grid(row=0, column=1, columnspan=1, padx=(0, 30), pady=1, sticky="w")


outLabelAreaCode.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

inLabelDeDup.grid(row=2, column=0, padx=10, pady=2, sticky="w")
inEntryDeDup.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
possibleStatesLbl.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

inLabelDelete.grid(row=4, column=0, padx=10, pady=2, sticky="w")
inEntryDelete.grid(row=4, column=1, padx=10, pady=5, sticky="ew")


#exitBtn.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

exitBtnFrame.grid(row=6, column=0, columnspan=2, pady=10)


# Configure column and row weights for resizing
#root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
#root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

root.mainloop()
