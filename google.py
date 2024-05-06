from googlesearch import search
import tkinter as tk


def googleSearch(inGoogleText):
    global googleResults
    # Clear out the list of results before starting a new search
    googleResults = []
    input = inGoogleText.get("1.0", "end-1c")
    if input != "":
        query = input
        for j in search(query, num=2, stop=5, pause=0.2):
            googleResults.append(j)

        # clear out the input
        inGoogleText.delete("1.0", "end")
    return googleResults


def displaySearchResults(root, googleResults):
    if googleResults:
        # Create a new window
        new_window = tk.Toplevel(root)
        new_window.title("Results")

        # Create a Listbox to display the results
        results_listbox = tk.Listbox(new_window, width=50)
        results_listbox.pack(pady=20)

        # Insert the results into the Listbox
        for result in googleResults:
            results_listbox.insert(tk.END, result)