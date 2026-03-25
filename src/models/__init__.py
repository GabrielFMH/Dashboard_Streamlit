"""Models package - Data structures for the sales forecast application."""

from .sale import Sale
from .product import Product
from .forecast import Forecast

__all__ = ["Sale", "Product", "Forecast"]