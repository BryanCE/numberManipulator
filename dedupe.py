import pyperclip
from areaCodes import statesByCodes
from chars import remove_chars, rm_duplicates_in_order

#globals for number feeding
feedNums = []
current_index = 0
cycled = True


def deDupe(inEntryDeDup, possibleStatesLbl, onOff, root):
    if inEntryDeDup.get("1.0", "end-1c") != "":
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

def extractAreaCode(number):
    return number[:3]

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