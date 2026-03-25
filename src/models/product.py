"""Product model - Represents a product in the catalog."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Represents a product in the catalog.
    
    Attributes:
        id: Unique identifier for the product
        name: Product name
        category: Product category (Electrónica, Ropa, Alimentos)
        base_price: Base price of the product
        cost: Cost of production/acquisition
        is_active: Whether the product is currently sold
    """
    id: str
    name: str
    category: str
    base_price: float
    cost: float = 0.0
    is_active: bool = True

    @property
    def margin(self) -> float:
        """Calculate profit margin percentage."""
        if self.base_price > 0:
            return ((self.base_price - self.cost) / self.base_price) * 100
        return 0.0

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, category={self.category}, price={self.base_price:.2f})"