"""Forecast Service - Generates sales projections."""

import numpy as np
import pandas as pd
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

from ..models.forecast import ForecastResult


class ForecastService:
    """
    Service for generating sales forecasts.
    
    Uses simple statistical methods:
    - Linear regression for trend
    - Seasonal decomposition
    - Confidence intervals
    """
    
    def __init__(self):
        """Initialize the forecast service."""
        pass
    
    def generate_forecast(
        self,
        historical_data: pd.DataFrame,
        forecast_months: int = 6,
        confidence: float = 0.95
    ) -> ForecastResult:
        """
        Generate sales forecast based on historical data.
        
        Args:
            historical_data: DataFrame with 'date' and 'value' columns
            forecast_months: Number of months to forecast
            confidence: Confidence level for intervals (0-1)
            
        Returns:
            ForecastResult with historical data and projections
        """
        # Prepare data
        df = historical_data.copy()
        df = df.sort_values("date")
        
        # Extract arrays
        dates = df["date"].tolist()
        values = df["total_amount"].tolist() if "total_amount" in df.columns else df["value"].tolist()
        
        # Calculate trend using linear regression
        x = np.arange(len(values))
        y = np.array(values)
        
        # Fit linear regression
        slope, intercept = np.polyfit(x, y, 1)
        
        # Calculate residuals and standard error
        y_pred = slope * x + intercept
        residuals = y - y_pred
        std_error = np.std(residuals)
        
        # Calculate seasonal factors
        seasonal_factors = self._calculate_seasonal_factors(dates, values)
        
        # Generate forecast
        forecast_dates = []
        forecast_values = []
        lower_bounds = []
        upper_bounds = []
        
        z_score = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
        
        last_date = dates[-1]
        
        for i in range(forecast_months):
            # Next month
            next_date = last_date + timedelta(days=30 * (i + 1))
            forecast_dates.append(next_date)
            
            # Base forecast from trend
            x_forecast = len(values) + i
            base_value = slope * x_forecast + intercept
            
            # Apply seasonal factor
            month = next_date.month
            seasonal = seasonal_factors.get(month, 1.0)
            forecast_value = base_value * seasonal
            
            # Ensure non-negative
            forecast_value = max(0, forecast_value)
            
            # Calculate confidence interval
            margin = z_score * std_error * (1 + i * 0.1)  # Increase uncertainty over time
            
            lower = max(0, forecast_value - margin)
            upper = forecast_value + margin
            
            forecast_values.append(forecast_value)
            lower_bounds.append(lower)
            upper_bounds.append(upper)
        
        # Calculate metrics
        metrics = self._calculate_forecast_metrics(
            values, forecast_values, slope, seasonal_factors
        )
        
        return ForecastResult.from_arrays(
            historical_dates=dates,
            historical_values=values,
            forecast_dates=forecast_dates,
            forecast_values=forecast_values,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            metrics=metrics
        )
    
    def _calculate_seasonal_factors(
        self,
        dates: List[datetime],
        values: List[float]
    ) -> dict:
        """
        Calculate seasonal factors by month.
        
        Args:
            dates: List of dates
            values: List of values
            
        Returns:
            Dictionary of month -> seasonal factor
        """
        # Group by month
        monthly_values = {}
        for date, value in zip(dates, values):
            month = date.month
            if month not in monthly_values:
                monthly_values[month] = []
            monthly_values[month].append(value)
        
        # Calculate average for each month
        monthly_avg = {
            month: np.mean(vals) 
            for month, vals in monthly_values.items()
        }
        
        # Calculate overall average
        overall_avg = np.mean(values)
        
        # Calculate seasonal factors
        seasonal_factors = {
            month: avg / overall_avg 
            for month, avg in monthly_avg.items()
        }
        
        # Fill missing months with 1.0
        for month in range(1, 13):
            if month not in seasonal_factors:
                seasonal_factors[month] = 1.0
        
        return seasonal_factors
    
    def _calculate_forecast_metrics(
        self,
        historical_values: List[float],
        forecast_values: List[float],
        trend: float,
        seasonal_factors: dict
    ) -> dict:
        """
        Calculate forecast metrics.
        
        Args:
            historical_values: Historical values
            forecast_values: Forecasted values
            trend: Trend slope
            seasonal_factors: Seasonal factors
            
        Returns:
            Dictionary of metrics
        """
        hist_avg = np.mean(historical_values)
        forecast_avg = np.mean(forecast_values)
        
        # Growth rate
        if hist_avg > 0:
            growth_rate = ((forecast_avg - hist_avg) / hist_avg) * 100
        else:
            growth_rate = 0
        
        # Trend direction
        trend_direction = "up" if trend > 0 else "down"
        
        # Seasonality strength
        seasonal_strength = np.std(list(seasonal_factors.values()))
        
        return {
            "historical_avg": hist_avg,
            "forecast_avg": forecast_avg,
            "growth_rate": growth_rate,
            "trend_direction": trend_direction,
            "seasonal_strength": seasonal_strength,
            "trend_slope": trend
        }
    
    def calculate_moving_average(
        self,
        values: List[float],
        window: int = 3
    ) -> List[float]:
        """
        Calculate moving average.
        
        Args:
            values: List of values
            window: Window size
            
        Returns:
            List of moving averages
        """
        if len(values) < window:
            return values
        
        result = []
        for i in range(len(values)):
            if i < window - 1:
                result.append(values[i])
            else:
                avg = np.mean(values[i - window + 1:i + 1])
                result.append(avg)
        
        return result