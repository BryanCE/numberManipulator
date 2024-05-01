import tkinter as tk
from tkinter import *
import pyperclip
import re
import ctypes
import csv

# CSV file path
csvAreaCodes = r"NpasInSvcByLocRpt.csv"


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


def remove_duplicates_preserve_order(numbers):
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
    input_text = inEntryDeDup.get("1.0", "end-1c")
    lines = input_text.split("\n")

    # clear out the input
    inEntryDeDup.delete("1.0", "end")

    cleanNums = []
    for line in lines:
        line = remove_chars(line)
        numbers = line.split()
        cleanNums.extend(numbers)

    uniqNums = remove_duplicates_preserve_order(cleanNums)
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






    outPut = "\n".join(f"{num} - " for num in uniqNums)

    pyperclip.copy(outPut)
    # try to make auto minimize only happen when check box is clicked
    if onOff.get() == 1:
        root.wm_state("iconic")


# Create the main window
root = tk.Tk()
root.title("NumberManipulator GUI")

# Text input field for Area Code Checker
inLabelAreaCode = tk.Label(root, text="Enter an Area Code to check what State it's from.")
inLabelAreaCode.pack(padx=5, pady=2)

inEntryAreaCode = tk.Text(root, height=1)
inEntryAreaCode.bind("<Return>", stateByAreaCode)
inEntryAreaCode.pack(fill=BOTH, expand=YES, padx=5, pady=5)
outLabelAreaCode = tk.Label(root)
outLabelAreaCode.pack(fill=BOTH, expand=YES, padx=5, pady=5)
# Text input field for DeDupe
inLabelDeDup = tk.Label(root, text="DeDupe - Enter the list of numbers separated by spaces:")
inLabelDeDup.pack(padx=5, pady=2)

inEntryDeDup = tk.Text(root, height=10)
inEntryDeDup.bind("<Return>", deDupe)
inEntryDeDup.pack(fill=BOTH, expand=YES, padx=5, pady=5)

#Label to display all possible states with area codes from DeDup
possibleStatesLbl = tk.Label(root)
possibleStatesLbl.pack(fill=BOTH, expand=YES, padx=5, pady=5)


# Text input field for bad number Deleter
inLabelDelete = tk.Label(root, text="Bad Number Deleter - Enter Numbers with Notes")
inLabelDelete.pack(padx=5, pady=2)

inEntryDelete = tk.Text(root, height=10)
inEntryDelete.bind("<Return>", badNumDel)
inEntryDelete.pack(fill=BOTH, expand=YES, padx=5, pady=5)


# make a check box to turn auto minimizing on and off
onOff = tk.IntVar()
autoMin = tk.Checkbutton(
    root, text="Auto Minimize ON/OFF", variable=onOff, onvalue=1, offvalue=0
)
autoMin.pack(fill=BOTH, expand=YES, padx=2, pady=1)

# Create an exit button
exitBtn = tk.Button(root, text="Exit", height=2, width=30, command=root.destroy)
exitBtn.pack(expand=YES, padx=5, pady=1)

# auto minimized the console window to make things even more efficient
ctypes.windll.user32.ShowWindow(
    ctypes.windll.kernel32.GetConsoleWindow(), 6
)  # 6 = SW_MINIMIZE
# info on .ShowWindow here:
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN

root.mainloop()
