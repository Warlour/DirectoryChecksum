import os
import tkinter as tk
import hashlib as hl
from threading import Timer
from pathlib import Path

def timerpackunpack(widget, output):
    widget.configure(text=output, fg = "#ff0000")
    Timer(1, lambda: widget.configure(fg = "#000000")).start()
    widget.pack()
    Timer(2, lambda: widget.pack_forget()).start()

"""
Returns a `dict` mapping hashes to sets of filenames.

`files` is an iterable over something supported by `open()` (e.g. `files`
can be a `list` of `str`s).

`hashes` and `duplicates` are intended for internal use only (recursing on
subdirectories).
"""
def find_duplicates(files, duplicates = {}):
    for file in files:
        sha256_hash = hl.sha256()
        with open(file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        hash = sha256_hash.hexdigest()

        # Add this hash occurrence to the `duplicates` dict. It will be
        # removed later if no other duplicates are found.
        if hash in duplicates:
            duplicates[hash].add(file)
        else:
            duplicates[hash] = {file}

    nonduplicates = []

    # Remove non-duplicates from 
    for key in duplicates:
        if len(duplicates[key]) < 2:
            nonduplicates.append(key)
    
    for key in nonduplicates:
        del duplicates[key]

    return duplicates

def comparechecksums():
    files = [] # All file names
    hashes = [] # SHA256-hash of all file names
    duplicates = {} # Duplicate files
    listbox.delete(0, tk.END)
    listbox.pack_forget()
    label.pack_forget()

    path = pathbox.get("1.0", 'end-1c')
    if not os.path.exists(os.path.dirname(path)) or not os.path.isdir(path):
        timerpackunpack(label, "Not a path to a directory")
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            # Check if it is a file
            if os.path.isfile(f):
                files.append(f)
        if files:
            duplicates = find_duplicates(files, duplicates)
            
            idx = 1
            for duplicateset in duplicates.values():
                listbox.insert(idx, "These files share the same checksum: ")
                idx += 1
                for element in duplicateset:
                    listbox.insert(idx, element)
                    idx += 1
                listbox.insert(idx, "")
                idx += 1
            label.configure(text = "List of files with the same checksum")
            label.pack()
            listbox.pack()
        else:
            timerpackunpack(label, "No duplicates found within the directory")

            

window = tk.Tk()
window.title("Directory compare")
window.iconbitmap("icon.ico")
window.geometry("500x250")
window.configure(bg = "#F2F2F2")
pathlabel = tk.Label(window, text="Path to compare checksum", justify = "left")
pathbox = tk.Text(window, height = 2, width = window.winfo_screenwidth(), bg = "#CDCDCD")
listbox = tk.Listbox(window, width = window.winfo_screenwidth())

label = tk.Label(window, text="", justify="center")
pathlabel.pack()
pathbox.pack()

calc = tk.Button(window, text="Get checksum", command = comparechecksums)
calc.pack()

window.mainloop()