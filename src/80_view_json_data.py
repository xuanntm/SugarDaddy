import json
import tkinter as tk
from tkinter import ttk, messagebox

def load_data():
    try:
        filepath = filepath_entry.get()  # Get the file path from the entry field
        with open(filepath, 'r') as f:
            data = json.load(f)
            display_data(data)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format.")
    except Exception as e:  # Catch other potential errors
        messagebox.showerror("Error", f"An error occurred: {e}")


def display_data(data):
    # Clear previous data (if any)
    for child in data_tree.get_children():
        data_tree.delete(child)

    if isinstance(data, dict):
        for key, value in data.items():
            data_tree.insert("", tk.END, values=(key, value))  # Display key-value pairs
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):  # Handle dictionaries within a list
                for key, value in item.items():
                     data_tree.insert("", tk.END, values=(key, value))
            else:
                data_tree.insert("", tk.END, values=("", item)) # Display list items directly
    else:  # Handle other data types (strings, numbers, etc.)
        data_tree.insert("", tk.END, values=("", data))



# --- UI Setup ---
root = tk.Tk()
root.title("JSON Data Viewer")

# File Path Input
filepath_label = ttk.Label(root, text="File Path:")
filepath_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Sticky aligns to the left (west)

filepath_entry = ttk.Entry(root, width=50)
filepath_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # Sticky makes it expand


load_button = ttk.Button(root, text="Load Data", command=load_data)
load_button.grid(row=1, column=0, columnspan=2, pady=(5, 10)) # Span across both columns

# Data Display (Treeview)
data_tree = ttk.Treeview(root, columns=("Key", "Value"), show="headings")
data_tree.heading("Key", text="Key")
data_tree.heading("Value", text="Value")

# Make the treeview scrollable
tree_scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=data_tree.yview)
data_tree.configure(yscrollcommand=tree_scrollbar_y.set)
tree_scrollbar_y.grid(row=2, column=2, sticky='ns') # Sticky makes it expand vertically
data_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="nsew") # Sticky makes it expand


root.columnconfigure(1, weight=1)  # Make the entry field expand horizontally
root.rowconfigure(2, weight=1) # Make the treeview expand vertically

root.mainloop()