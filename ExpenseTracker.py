import tkinter as tk
from tkinter import ttk
from tkinter import font
import sys

# Fix for high DPI displays to make UI sharp
if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)  # Make app DPI aware
    except:
        pass

# Create main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x400")
root.resizable(False, False)

# Configure root for better appearance
root.configure(bg='#f0f0f0')  # Light gray background like Windows

# Heading - properly centered with no width constraint
heading_font = font.Font(family="Arial", size=20, weight="bold")
head_label = tk.Label(root, text="EXPENSE TRACKER", font=heading_font, bg='#f0f0f0')
head_label.place(x=150, y=30)

# Amount - moved entry field further right
amount_label = tk.Label(root, text="Amount:", bg='#f0f0f0')
amount_label.place(x=30, y=90)
amount_entry = tk.Entry(root, relief='solid', borderwidth=1)
amount_entry.place(x=120, y=90, width=150, height=20)

# Category - moved entry field further right
category_label = tk.Label(root, text="Category:", bg='#f0f0f0')
category_label.place(x=30, y=120)
categories = ["Food", "Travel", "Shopping", "Education", "Entertainment", "Others"]
category_combo = ttk.Combobox(root, values=categories, state="readonly")
category_combo.place(x=120, y=120, width=150, height=20)
category_combo.set("Food")

# Description - moved entry field further right
description_label = tk.Label(root, text="Description:", bg='#f0f0f0')
description_label.place(x=30, y=150)
description_entry = tk.Entry(root, relief='solid', borderwidth=1)
description_entry.place(x=120, y=150, width=150, height=20)

# Date - moved entry field further right
date_label = tk.Label(root, text="Date:", bg='#f0f0f0')
date_label.place(x=30, y=180)
date_entry = tk.Entry(root, relief='solid', borderwidth=1)
date_entry.place(x=120, y=180, width=150, height=20)

# Display labels (right side) - moved further right
display_amount = tk.Label(root, text="", bg='#f0f0f0', anchor='w')
display_amount.place(x=320, y=90)

display_category = tk.Label(root, text="", bg='#f0f0f0', anchor='w')
display_category.place(x=320, y=120)

display_description = tk.Label(root, text="", bg='#f0f0f0', anchor='w')
display_description.place(x=320, y=150)

display_date = tk.Label(root, text="", bg='#f0f0f0', anchor='w')
display_date.place(x=320, y=180)

# Function to add expense
def add_expense():
    try:
        # Get values from input fields
        amount = float(amount_entry.get())
        category = category_combo.get()
        description = description_entry.get()
        date = date_entry.get()

        # Display the values on the right side
        display_amount.config(text=f"Amount: {amount}")
        display_category.config(text=f"Category: {category}")
        display_description.config(text=f"Description: {description}")
        display_date.config(text=f"Date: {date}")

    except ValueError:
        # Handle invalid amount input
        display_amount.config(text="Invalid amount!")
        display_category.config(text="")
        display_description.config(text="")
        display_date.config(text="")

# Add Expense Button - aligned with entry fields
add_button = tk.Button(root, text="ADD EXPENSE", command=add_expense,
                      relief='raised', borderwidth=2,
                      bg='#e1e1e1', activebackground='#d1d1d1')
add_button.place(x=120, y=250, width=150, height=25)

# Start the application
root.mainloop()