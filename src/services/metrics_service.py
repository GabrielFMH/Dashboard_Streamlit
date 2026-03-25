"""Metrics Service - Calculates KPIs and business metrics."""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class MetricsService:
    """
    Service for calculating business metrics and KPIs.
    
    Metrics calculated:
    - Total Revenue
    - Units Sold
    - Average Ticket
    - Month-over-Month Growth
    - Year-over-Year Growth
    """
    
    def __init__(self):
        """Initialize the metrics service."""
        pass
    
    def calculate_total_revenue(self, df: pd.DataFrame) -> float:
        """
        Calculate total revenue.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Total revenue
        """
        return df["total_amount"].sum()
    
    def calculate_total_units(self, df: pd.DataFrame) -> int:
        """
        Calculate total units sold.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Total units sold
        """
        return df["quantity"].sum()
    
    def calculate_average_ticket(self, df: pd.DataFrame) -> float:
        """
        Calculate average ticket (revenue / units).
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Average ticket value
        """
        total_revenue = self.calculate_total_revenue(df)
        total_units = self.calculate_total_units(df)
        
        if total_units > 0:
            return total_revenue / total_units
        return 0
    
    def calculate_mom_growth(
        self,
        monthly_data: pd.DataFrame
    ) -> float:
        """
        Calculate month-over-month growth.
        
        Args:
            monthly_data: Monthly aggregated DataFrame
            
        Returns:
            MoM growth percentage
        """
        if len(monthly_data) < 2:
            return 0
        
        # Get last two months
        last_month = monthly_data.iloc[-1]["total_amount"]
        prev_month = monthly_data.iloc[-2]["total_amount"]
        
        if prev_month > 0:
            return ((last_month - prev_month) / prev_month) * 100
        return 0
    
    def calculate_yoy_growth(
        self,
        monthly_data: pd.DataFrame
    ) -> float:
        """
        Calculate year-over-year growth.
        
        Args:
            monthly_data: Monthly aggregated DataFrame
            
        Returns:
            YoY growth percentage
        """
        if len(monthly_data) < 12:
            return 0
        
        # Get last month and same month last year
        last_month = monthly_data.iloc[-1]["total_amount"]
        
        # Find 12 months ago
        if len(monthly_data) >= 13:
            prev_year_month = monthly_data.iloc[-13]["total_amount"]
        else:
            return 0
        
        if prev_year_month > 0:
            return ((last_month - prev_year_month) / prev_year_month) * 100
        return 0
    
    def calculate_all_metrics(
        self,
        df: pd.DataFrame,
        monthly_data: Optional[pd.DataFrame] = None
    ) -> Dict[str, float]:
        """
        Calculate all key metrics.
        
        Args:
            df: Sales DataFrame
            monthly_data: Optional monthly aggregated data
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "total_revenue": self.calculate_total_revenue(df),
            "total_units": self.calculate_total_units(df),
            "average_ticket": self.calculate_average_ticket(df),
        }
        
        if monthly_data is not None:
            metrics["mom_growth"] = self.calculate_mom_growth(monthly_data)
            metrics["yoy_growth"] = self.calculate_yoy_growth(monthly_data)
        
        return metrics
    
    def get_top_products(
        self,
        df: pd.DataFrame,
        n: int = 5,
        by: str = "revenue"
    ) -> pd.DataFrame:
        """
        Get top N products by revenue or units.
        
        Args:
            df: Sales DataFrame
            n: Number of products to return
            by: Sort by 'revenue' or 'units'
            
        Returns:
            DataFrame with top products
        """
        product_data = df.groupby(["product_id", "product_name", "category"]).agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        product_data.columns = ["product_id", "product_name", "category", "revenue", "units"]
        
        if by == "revenue":
            return product_data.nlargest(n, "revenue")
        else:
            return product_data.nlargest(n, "units")
    
    def get_top_categories(
        self,
        df: pd.DataFrame,
        by: str = "revenue"
    ) -> pd.DataFrame:
        """
        Get categories ranked by revenue or units.
        
        Args:
            df: Sales DataFrame
            by: Sort by 'revenue' or 'units'
            
        Returns:
            DataFrame with categories
        """
        category_data = df.groupby("category").agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        category_data.columns = ["category", "revenue", "units"]
        
        if by == "revenue":
            return category_data.sort_values("revenue", ascending=False)
        else:
            return category_data.sort_values("units", ascending=False)
    
    def get_daily_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get daily summary of sales.
        
        Args:
            df: Sales DataFrame
            
        Returns:
            Daily aggregated DataFrame
        """
        daily = df.groupby("date").agg({
            "total_amount": "sum",
            "quantity": "sum"
        }).reset_index()
        
        daily.columns = ["date", "revenue", "units"]
        
        return daily.sort_values("date")
    
    def format_currency(self, value: float) -> str:
        """
        Format value as currency.
        
        Args:
            value: Numeric value
            
        Returns:
            Formatted currency string
        """
        return f"${value:,.2f}"
    
    def format_percentage(self, value: float) -> str:
        """
        Format value as percentage.
        
        Args:
            value: Numeric value
            
        Returns:
            Formatted percentage string
        """
        sign = "+" if value > 0 else ""
        return f"{sign}{value:.1f}%"