import re

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