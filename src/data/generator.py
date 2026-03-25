"""Data Generator - Generates realistic fictional sales data."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

from ..models.sale import Sale
from ..models.product import Product


class DataGenerator:
    """
    Generates realistic fictional sales data for the forecast application.
    
    Features:
    - 24 months of historical data
    - 10 products across 3 categories
    - Seasonal patterns
    - Growth trends
    - Random variability
    """
    
    # Product definitions by category
    PRODUCTS_CONFIG = {
        "Electrónica": [
            {"name": "Laptop Pro 15", "base_price": 1299.99, "cost": 800.00},
            {"name": "Smartphone X", "base_price": 899.99, "cost": 550.00},
            {"name": "Tablet Mini", "base_price": 449.99, "cost": 280.00},
            {"name": "Auriculares BT", "base_price": 149.99, "cost": 75.00},
        ],
        "Ropa": [
            {"name": "Camisa Algodón", "base_price": 49.99, "cost": 20.00},
            {"name": "Pantalón Jeans", "base_price": 79.99, "cost": 35.00},
            {"name": "Zapatillas Sport", "base_price": 119.99, "cost": 55.00},
            {"name": "Chaqueta Invierno", "base_price": 159.99, "cost": 70.00},
        ],
        "Alimentos": [
            {"name": "Café Premium 1kg", "base_price": 24.99, "cost": 12.00},
            {"name": "Aceite Oliva 1L", "base_price": 14.99, "cost": 7.00},
            {"name": "Chocolate Artesano", "base_price": 9.99, "cost": 4.00},
            {"name": "Vino Tinto Reserva", "base_price": 29.99, "cost": 12.00},
        ],
    }
    
    # Seasonal factors by month (1.0 = baseline)
    SEASONAL_FACTORS = {
        1: 0.85,   # January - low
        2: 0.80,   # February - low
        3: 0.95,   # March
        4: 1.00,   # April
        5: 1.05,   # May
        6: 1.15,   # June - summer start
        7: 1.25,   # July - peak summer
        8: 1.20,   # August
        9: 1.10,   # September
        10: 1.05,  # October
        11: 1.15,  # November - Black Friday effect
        12: 1.30,  # December - holiday peak
    }
    
    def __init__(self, seed: int = 42):
        """
        Initialize the data generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
        self.products: List[Product] = []
        self.sales: List[Sale] = []
        self._initialize_products()
    
    def _initialize_products(self) -> None:
        """Initialize product catalog."""
        product_id = 1
        for category, products in self.PRODUCTS_CONFIG.items():
            for prod_config in products:
                product = Product(
                    id=f"P{product_id:03d}",
                    name=prod_config["name"],
                    category=category,
                    base_price=prod_config["base_price"],
                    cost=prod_config["cost"],
                    is_active=True
                )
                self.products.append(product)
                product_id += 1
    
    def generate_sales_data(
        self,
        months: int = 24,
        daily_variation: float = 0.15,
        growth_rate: float = 0.08
    ) -> pd.DataFrame:
        """
        Generate realistic sales data.
        
        Args:
            months: Number of months of historical data
            daily_variation: Random noise factor (0.0-1.0)
            growth_rate: Annual growth rate (0.0-1.0)
            
        Returns:
            DataFrame with sales data
        """
        # Calculate start date (go back 'months' months)
        end_date = datetime.now()
        start_date = end_date.replace(day=1) - timedelta(days=months * 30)
        
        # Generate sales for each day in the period
        all_sales = []
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends for more realism
            if current_date.weekday() < 5:
                # Generate sales for each product
                for product in self.products:
                    # Base quantity with some randomness
                    base_quantity = np.random.randint(1, 10)
                    
                    # Apply seasonal factor
                    seasonal = self.SEASONAL_FACTORS.get(current_date.month, 1.0)
                    
                    # Apply growth trend (gradual increase over time)
                    days_elapsed = (current_date - start_date).days
                    months_elapsed = days_elapsed / 30
                    trend = 1 + (growth_rate * months_elapsed / 12)
                    
                    # Apply random noise
                    noise = 1 + np.random.uniform(-daily_variation, daily_variation)
                    
                    # Calculate final quantity
                    quantity = int(base_quantity * seasonal * trend * noise)
                    quantity = max(1, quantity)  # At least 1 sale
                    
                    # Calculate total amount
                    total_amount = quantity * product.base_price
                    
                    # Create sale record
                    sale = Sale(
                        id=str(uuid.uuid4())[:8],
                        date=current_date,
                        product_id=product.id,
                        product_name=product.name,
                        category=product.category,
                        quantity=quantity,
                        unit_price=product.base_price,
                        total_amount=total_amount
                    )
                    all_sales.append(sale)
            
            current_date += timedelta(days=1)
        
        self.sales = all_sales
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                "id": sale.id,
                "date": sale.date,
                "product_id": sale.product_id,
                "product_name": sale.product_name,
                "category": sale.category,
                "quantity": sale.quantity,
                "unit_price": sale.unit_price,
                "total_amount": sale.total_amount
            }
            for sale in all_sales
        ])
        
        return df
    
    def get_products(self) -> List[Product]:
        """Get the list of products."""
        return self.products
    
    def get_categories(self) -> List[str]:
        """Get the list of product categories."""
        return list(self.PRODUCTS_CONFIG.keys())
    
    def get_monthly_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sales data by month.
        
        Args:
            df: Daily sales DataFrame
            
        Returns:
            Monthly aggregated DataFrame
        """
        df_copy = df.copy()
        df_copy["year_month"] = df_copy["date"].dt.to_period("M")
        
        monthly = df_copy.groupby("year_month").agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        monthly["year_month"] = monthly["year_month"].astype(str)
        monthly["date"] = pd.to_datetime(monthly["year_month"])
        
        return monthly
    
    def get_category_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sales data by category.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Category aggregated DataFrame
        """
        category_sales = df.groupby("category").agg({
            "total_amount": "sum",
            "quantity": "sum",
            "product_name": "count"
        }).reset_index()
        
        category_sales.columns = ["category", "revenue", "units_sold", "num_products"]
        
        return category_sales
    
    def get_product_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sales data by product.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Product aggregated DataFrame
        """
        product_sales = df.groupby(["product_id", "product_name", "category"]).agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        product_sales.columns = ["product_id", "product_name", "category", "revenue", "units_sold"]
        
        return product_sales