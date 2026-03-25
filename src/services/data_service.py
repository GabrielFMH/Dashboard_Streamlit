"""Data Service - Retrieves and filters sales data."""

import pandas as pd
from typing import List, Optional, Dict, Tuple
from datetime import datetime

from ..data.generator import DataGenerator


class DataService:
    """
    Service for retrieving and filtering sales data.
    
    Responsibilities:
    - Generate and manage sales data
    - Apply filters (period, category, product)
    - Provide aggregated views
    """
    
    def __init__(self, data_generator: Optional[DataGenerator] = None):
        """
        Initialize the data service.
        
        Args:
            data_generator: Optional data generator instance
        """
        self.data_generator = data_generator or DataGenerator()
        self.sales_data: Optional[pd.DataFrame] = None
    
    def get_sales_data(self, months: int = 24) -> pd.DataFrame:
        """
        Get or generate sales data.
        
        Args:
            months: Number of months of data to generate
            
        Returns:
            DataFrame with sales data
        """
        if self.sales_data is None:
            self.sales_data = self.data_generator.generate_sales_data(months=months)
        return self.sales_data
    
    def filter_by_period(
        self,
        df: pd.DataFrame,
        months: int
    ) -> pd.DataFrame:
        """
        Filter data by time period.
        
        Args:
            df: Sales DataFrame
            months: Number of months to include (from end)
            
        Returns:
            Filtered DataFrame
        """
        if months >= 24:
            return df
        
        # Get the last date in the data
        max_date = df["date"].max()
        min_date = max_date - pd.DateOffset(months=months)
        
        return df[df["date"] >= min_date].copy()
    
    def filter_by_category(
        self,
        df: pd.DataFrame,
        category: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filter data by category.
        
        Args:
            df: Sales DataFrame
            category: Category to filter by (None = all)
            
        Returns:
            Filtered DataFrame
        """
        if category is None or category == "Todas":
            return df
        return df[df["category"] == category].copy()
    
    def filter_by_product(
        self,
        df: pd.DataFrame,
        product_id: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filter data by product.
        
        Args:
            df: Sales DataFrame
            product_id: Product ID to filter by (None = all)
            
        Returns:
            Filtered DataFrame
        """
        if product_id is None or product_id == "Todos":
            return df
        return df[df["product_id"] == product_id].copy()
    
    def get_monthly_data(
        self,
        df: pd.DataFrame,
        metric: str = "revenue"
    ) -> pd.DataFrame:
        """
        Get monthly aggregated data.
        
        Args:
            df: Sales DataFrame
            metric: Metric to aggregate ('revenue' or 'units')
            
        Returns:
            Monthly aggregated DataFrame
        """
        df_copy = df.copy()
        df_copy["year_month"] = df_copy["date"].dt.to_period("M")
        
        if metric == "revenue":
            agg_col = "total_amount"
        else:
            agg_col = "quantity"
        
        monthly = df_copy.groupby("year_month").agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        monthly["year_month"] = monthly["year_month"].astype(str)
        monthly["date"] = pd.to_datetime(monthly["year_month"] + "-01")
        
        return monthly.sort_values("date")
    
    def get_category_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get category aggregated data.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Category aggregated DataFrame
        """
        return self.data_generator.get_category_sales(df)
    
    def get_product_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get product aggregated data.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Product aggregated DataFrame
        """
        return self.data_generator.get_product_sales(df)
    
    def get_categories(self) -> List[str]:
        """Get list of available categories."""
        return ["Todas"] + self.data_generator.get_categories()
    
    def get_products(self) -> List[Dict[str, str]]:
        """Get list of available products."""
        products = self.data_generator.get_products()
        return [
            {"id": p.id, "name": p.name, "category": p.category}
            for p in products
        ]
    
    def get_date_range(self, df: pd.DataFrame) -> Tuple[datetime, datetime]:
        """
        Get the date range of the data.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Tuple of (min_date, max_date)
        """
        return (df["date"].min(), df["date"].max())