import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .database import (
    add_transaction,
    get_categories,
)
from .reports import show_expense_pie, show_balance_line
from .utils import validate_date

class BudgetApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Simple Budget App")

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Amount").grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Category").grid(row=2, column=0)
        self.category_combo = ttk.Combobox(self.root)
        self.category_combo.grid(row=2, column=1)
        self.load_categories()

        tk.Label(self.root, text="Description").grid(row=3, column=0)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Transaction",
                  command=self.save_transaction).grid(row=4, columnspan=2)

        tk.Button(self.root, text="Expense Pie Chart",
                  command=show_expense_pie).grid(row=5, columnspan=2)

        tk.Button(self.root, text="Balance Line Chart",
                  command=show_balance_line).grid(row=6, columnspan=2)

    def load_categories(self):
        categories = get_categories()
        self.categories_map = {name: id_ for id_, name, _ in categories}
        self.category_combo["values"] = list(self.categories_map.keys())

    def save_transaction(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category_name = self.category_combo.get()
        desc = self.desc_entry.get()

        if not validate_date(date):
            messagebox.showerror("Error", "Invalid date format")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be numeric")
            return

        if category_name not in self.categories_map:
            messagebox.showerror("Error", "Invalid category")
            return

        category_id = self.categories_map[category_name]

        add_transaction(date, amount, category_id, desc)

        messagebox.showinfo("Success", "Transaction Added")
