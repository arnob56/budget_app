import tkinter as tk
from .database import init_db, add_category
from .gui import BudgetApp
from .utils import setup_logging

def seed_categories():
    add_category("Salary", "income")
    add_category("Food", "expense")
    add_category("Transport", "expense")
    add_category("Shopping", "expense")

def main():
    setup_logging()
    init_db()
    seed_categories()

    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
