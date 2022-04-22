import os
import tkinter as tk
import hashlib as hl
from threading import Timer

def timerpackunpack(widget, output):
    widget.configure(text=output)
    widget.pack()
    Timer(2, lambda: widget.pack_forget()).start()

def comparechecksums():
    files = [] # All file names
    hashes = [] # SHA256-hash of all file names
    duplicates = [] # Duplicate files
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
        if (files):
            label.configure(text = "List of files with the same checksum")
            label.pack()
            for file in files:
                sha256_hash = hl.sha256()
                with open(file, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                hashes.append(sha256_hash.hexdigest())
            # If there are any duplicates
            if len(hashes) != len(set(hashes)):
                # if duplicate append filename to duplicates list
                    # duplicates.append(files[idx])
                    '''Duplicate list should consist of all the files who shares a checksum, i.e: 
                    [[1stDuplicateOfChecksum1, 2ndDuplicateOfChecksum1], [1stDuplicateOfChecksum2, 
                    2ndDuplicateOfChecksum2]]
                    From this there should be inserted a single index of the first list in the list to the ListBox widget like this:
                    "1stDuplicateOfChecksum1 <-> 2ndDuplicateOfChecksum1 <-> 3rd... <-> 4th....",
                    "1stDuplicateOfChecksum2 <-> 2ndDuplicateOfChecksum2"
                    etc.

                    This should, however, not be the full path but only "filename"
                    '''

                listbox.pack()
            else:
                timerpackunpack(label, "No duplicates found within the directory")

            

window = tk.Tk()
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