import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime

# Fix for high DPI displays to make UI sharp
if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)  # Make app DPI aware
    except:
        pass

class ExpenseTrackerDB:
    def __init__(self):
        self.connection = None
        self.setup_gui()
        self.connect_database()
        self.create_table()
        self.refresh_expense_list()

    def connect_database(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='expense_tracker',
                user='root',  # Change this to your MySQL username
                password='ayush'   # Change this to your MySQL password
            )

            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.status_label.config(text="Database: Connected ✓", fg="green")

        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.status_label.config(text="Database: Not Connected ✗", fg="red")
            messagebox.showerror("Database Error",
                               f"Could not connect to database.\n\n"
                               f"Please ensure:\n"
                               f"1. MySQL is installed and running\n"
                               f"2. Database 'expense_tracker' exists\n"
                               f"3. Username/password are correct\n\n"
                               f"Error: {e}")

    def create_table(self):
        """Create expenses table if it doesn't exist"""
        if self.connection and self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                create_table_query = """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10, 2) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    description VARCHAR(255),
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                self.connection.commit()
                cursor.close()
                print("Table created successfully")

            except Error as e:
                print(f"Error creating table: {e}")
                messagebox.showerror("Database Error", f"Error creating table: {e}")

    def setup_gui(self):
        """Setup the GUI"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Expense Tracker with MySQL")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')

        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Title
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(main_frame, text="EXPENSE TRACKER", font=title_font, bg='#f0f0f0')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Input Frame
        input_frame = tk.LabelFrame(main_frame, text="Add New Expense", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        input_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=(0, 10), pady=(0, 10))

        # Amount
        tk.Label(input_frame, text="Amount:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Category
        tk.Label(input_frame, text="Category:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.categories = ["Food", "Travel", "Shopping", "Education", "Entertainment", "Others"]
        self.category_combo = ttk.Combobox(input_frame, values=self.categories, state="readonly", width=18)
        self.category_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.category_combo.set("Food")

        # Description
        tk.Label(input_frame, text="Description:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.description_entry = tk.Entry(input_frame, width=20)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Date
        tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg='#f0f0f0').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        # Set today's date as default
        today = datetime.now().strftime('%Y-%m-%d')
        self.date_entry.insert(0, today)

        # Buttons
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="ADD EXPENSE", command=self.add_expense,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="UPDATE", command=self.update_expense,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_expense,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="CLEAR", command=self.clear_fields,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        # Expense List Frame
        list_frame = tk.LabelFrame(main_frame, text="Expense List", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        list_frame.grid(row=1, column=2, rowspan=2, sticky='nsew', padx=(10, 0))

        # Treeview for expenses
        columns = ('ID', 'Amount', 'Category', 'Description', 'Date')
        self.expense_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # Define headings
        for col in columns:
            self.expense_tree.heading(col, text=col)
            if col == 'ID':
                self.expense_tree.column(col, width=50)
            elif col == 'Amount':
                self.expense_tree.column(col, width=80)
            elif col == 'Category':
                self.expense_tree.column(col, width=100)
            else:
                self.expense_tree.column(col, width=120)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)

        self.expense_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Bind double-click to load expense for editing
        self.expense_tree.bind('<Double-1>', self.on_expense_select)

        # Status bar
        self.status_label = tk.Label(main_frame, text="Database: Connecting...",
                                   bg='#f0f0f0', anchor='w')
        self.status_label.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        # Configure grid weights
        main_frame.grid_columnconfigure(2, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.selected_expense_id = None

    def add_expense(self):
        """Add expense to database"""
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "No database connection!")
            return

        try:
            amount = float(self.amount_entry.get())
            category = self.category_combo.get()
            description = self.description_entry.get()
            date = self.date_entry.get()

            if not all([amount, category, date]):
                messagebox.showwarning("Warning", "Please fill in all required fields!")
                return

            cursor = self.connection.cursor()
            query = "INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (amount, category, description, date))
            self.connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()
            self.refresh_expense_list()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding expense: {e}")

    def refresh_expense_list(self):
        """Refresh the expense list from database"""
        if not self.connection or not self.connection.is_connected():
            return

        try:
            # Clear existing items
            for item in self.expense_tree.get_children():
                self.expense_tree.delete(item)

            cursor = self.connection.cursor()
            cursor.execute("SELECT id, amount, category, description, date FROM expenses ORDER BY date DESC")
            records = cursor.fetchall()

            for record in records:
                self.expense_tree.insert('', 'end', values=record)

            cursor.close()

        except Error as e:
            messagebox.showerror("Database Error", f"Error loading expenses: {e}")

    def on_expense_select(self, event):
        """Load selected expense for editing"""
        selection = self.expense_tree.selection()
        if selection:
            item = self.expense_tree.item(selection[0])
            values = item['values']

            self.selected_expense_id = values[0]
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, values[1])
            self.category_combo.set(values[2])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, values[3])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, values[4])

    def update_expense(self):
        """Update selected expense"""
        if not self.selected_expense_id:
            messagebox.showwarning("Warning", "Please select an expense to update!")
            return

        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "No database connection!")
            return

        try:
            amount = float(self.amount_entry.get())
            category = self.category_combo.get()
            description = self.description_entry.get()
            date = self.date_entry.get()

            cursor = self.connection.cursor()
            query = "UPDATE expenses SET amount=%s, category=%s, description=%s, date=%s WHERE id=%s"
            cursor.execute(query, (amount, category, description, date, self.selected_expense_id))
            self.connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Expense updated successfully!")
            self.clear_fields()
            self.refresh_expense_list()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating expense: {e}")

    def delete_expense(self):
        """Delete selected expense"""
        if not self.selected_expense_id:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM expenses WHERE id = %s", (self.selected_expense_id,))
                self.connection.commit()
                cursor.close()

                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.clear_fields()
                self.refresh_expense_list()

            except Error as e:
                messagebox.showerror("Database Error", f"Error deleting expense: {e}")

    def clear_fields(self):
        """Clear all input fields"""
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("Food")
        self.description_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.selected_expense_id = None

    def run(self):
        """Start the application"""
        self.root.mainloop()
        # Close database connection when app closes
        if self.connection and self.connection.is_connected():
            self.connection.close()

def main():
    app = ExpenseTrackerDB()
    app.run()

if __name__ == "__main__":
    main()