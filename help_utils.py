from tkinter import ttk
import tkinter as tk

def get_help_data():
    help_data = [
        ("Check Area Code", "Enter a 3 digit Area Code to check what State it's from."),
        ("DeDupe", "Enter the list of numbers you want to use separated by spaces or on new lines.\n\nHit <Enter> and the list will be deduped and formatted for you to paste into your notes.\nThe numbers will disappear, don't worry they haven't been lost.\n\nThey are loaded into your computer's clipboard in a convenient format.\n\nThe format puts each number on a new line with a - after each. \nThis gives you a space to add notes next to each when logging calls in Salesforce or other CRM."),
        ("Clean Numbers", "After calling all the numbers and leaving notes after each in Salesforce or another CRM,\n\nYou can copy your whole list of numbers along with the notes after each and paste them into the Clean Numbers input.\n\nThe notes are an important part of this, if your notes contain any variation of\nthe word Bad or wrong, it will be considered a bad number and removed from the list.\n\nThe cleaned list will be copied to your clipboard and ready to be pasted back into Salesforce or another CRM to save."),
        ("Auto Minimize", "This option gives you the ability to automatically minimize the application after you've pasted your numbers into DeDupe and hit <Enter>. \nAnd after pasting numbers into Clean Numbers and hit <Enter>.\n\nThis is useful if you don't want this application blocking your view of your CRM while you're making calls.\n\nIf you would like to keep it open, simply uncheck the box. The application will stay open until you manually minimize it or you close it."),
        ("Exit", "Close the application.\n\nDUH!!! Haha!!!\n\nJust kidding, but seriously, this button closes the application.")
    ]
    return help_data

def get_hotkey_data():
    hotkey_data = [
        ("Control + f", "Feeding Individual Numbers to Clipboard:\n\nAfter pasting numbers into DeDupe, all the numbers will be formatted and ready to be pasted into your notes.\n\nWhen ready to dial numbers, you can Press Control+f to feed one phone number at a time to your clipboard.\n\nIf needed you can paste this single number multiple times, when you want the next number fed, simply press Control+f again.\n\nThe next time you press Control+v the next number will be pasted."),
        ("Control + Shift + F", "Feeding All Numbers to Clipboard:\n\nIf at any time you want to feed all the numbers to your clipboard at once, you can press Control+Shift+F. This loads the clipboard with all the original numbers, making them ready to paste.\n\nKeep in mind this is the original list containing numbers you may have called that were wrong or bad.\n\nIf wrong or bad numbers need to be removed, paste your numbers with notes into the Clean Numbers input.\n\nThis is useful if when you're ready to move to another list of numbers and want to paste all the original numbers back into Salesforce or another CRM."),
    ]
    return hotkey_data

def create_help_tab(notebook, title, content):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=title)

    help_text = tk.Text(tab, wrap=tk.WORD)
    help_text.pack(fill='both', expand=True, padx=10, pady=10)
    help_text.insert(tk.END, content)
    help_text.configure(state='disabled')

def create_instructions_notebook(parent_window):
    parent_window.title("Help")
    help_notebook = ttk.Notebook(parent_window)
    help_notebook.pack(fill='both', expand=True, padx=10, pady=10)

    for title, content in get_help_data():
        create_help_tab(help_notebook, title, content)

def create_hotkeys_notebook(parent_window):
    parent_window.title("Hotkeys")
    hotkey_notebook = ttk.Notebook(parent_window)
    hotkey_notebook.pack(fill='both', expand=True, padx=10, pady=10)

    for title, content in get_hotkey_data():
        create_help_tab(hotkey_notebook, title, content)