import pandas as pd
import matplotlib.pyplot as plt
from .database import get_all_transactions

def generate_dataframe():
    data = get_all_transactions()

    if not data:
        return None

    df = pd.DataFrame(data, columns=[
        "id", "date", "amount", "category", "type", "description"
    ])
    df["date"] = pd.to_datetime(df["date"])
    return df

def show_expense_pie():
    df = generate_dataframe()
    if df is None:
        print("No data available.")
        return

    expenses = df[df["type"] == "expense"]
    summary = expenses.groupby("category")["amount"].sum()

    if summary.empty:
        print("No expense data.")
        return

    summary.plot.pie(autopct='%1.1f%%', title="Expenses by Category")
    plt.ylabel("")
    plt.show()

def show_balance_line():
    df = generate_dataframe()
    if df is None:
        print("No data available.")
        return

    df = df.sort_values("date")
    df["signed_amount"] = df.apply(
        lambda row: row["amount"] if row["type"] == "income"
        else -row["amount"],
        axis=1
    )

    df["balance"] = df["signed_amount"].cumsum()

    plt.plot(df["date"], df["balance"])
    plt.title("Balance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
