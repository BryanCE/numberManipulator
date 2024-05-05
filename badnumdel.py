import pyperclip
from chars import remove_chars


def badNumDel(inEntryDelete, onOff, root):
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