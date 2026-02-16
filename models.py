from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str
    type: str  # 'income' or 'expense'

@dataclass
class Transaction:
    id: int
    date: str
    amount: float
    category_id: int
    description: str
