import csv

# CSV file path
csvAreaCodes = r"NpasInSvcByLocRpt.csv"

def extractAreaCode(number):
    return number[:3]

# Function to check for a state based on an area code
def stateByAreaCode(inEntryAreaCode):
    if inEntryAreaCode.get("1.0", "end-1c") != "":
        with open(csvAreaCodes, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            areaCode = inEntryAreaCode.get("1.0", "end-1c")
            areaCode = areaCode.replace("\n", "").strip()
            state = ""
            for row in csv_reader:
                if row['NPA'] == areaCode:
                    state = row["Location"]
                    break
            if state == "":
                # clear out the input
                inEntryAreaCode.delete("1.0", "end")
                #outLabelAreaCode.config(text="No state with that Area Code")
                inEntryAreaCode.insert("1.0", "NONE")
                # Set the cursor position to the beginning of the first line
                end_index = "1.0 + {} chars".format(len("NONE"))
                inEntryAreaCode.tag_add("sel", "1.0", end_index)
            else:
                # Clear out the input
                inEntryAreaCode.delete("1.0", "end")

                # Insert the state into the text box
                inEntryAreaCode.insert("1.0", state)

                # Set the cursor position to the beginning of the first line
                inEntryAreaCode.see("1.0")
                end_index = "1.0 + {} chars".format(len(state))
                inEntryAreaCode.tag_add("sel", "1.0", end_index)

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