"""Sale model - Represents a single sale transaction."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Sale:
    """
    Represents a single sale transaction.
    
    Attributes:
        id: Unique identifier for the sale
        date: Date of the sale
        product_id: ID of the product sold
        product_name: Name of the product
        category: Product category
        quantity: Number of units sold
        unit_price: Price per unit
        total_amount: Total sale amount (quantity * unit_price)
    """
    id: str
    date: datetime
    product_id: str
    product_name: str
    category: str
    quantity: int
    unit_price: float
    total_amount: float

    @property
    def revenue(self) -> float:
        """Returns the total revenue from this sale."""
        return self.total_amount

    def __repr__(self) -> str:
        return (
            f"Sale(id={self.id}, date={self.date.strftime('%Y-%m-%d')}, "
            f"product={self.product_name}, amount={self.total_amount:.2f})"
        )