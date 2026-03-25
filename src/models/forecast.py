"""Forecast model - Represents a sales projection/forecast."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import numpy as np


@dataclass
class Forecast:
    """
    Represents a sales forecast projection.
    
    Attributes:
        date: Date for which the forecast is made
        predicted_value: The predicted sales value
        lower_bound: Lower bound of confidence interval
        upper_bound: Upper bound of confidence interval
        confidence: Confidence level of the forecast (0-1)
        metric: The metric being forecasted (revenue, units, etc.)
    """
    date: datetime
    predicted_value: float
    lower_bound: float
    upper_bound: float
    confidence: float = 0.95
    metric: str = "revenue"

    @property
    def uncertainty(self) -> float:
        """Returns the range of uncertainty (upper - lower)."""
        return self.upper_bound - self.lower_bound

    @property
    def is_trend_up(self) -> bool:
        """Returns True if the forecast shows an upward trend."""
        return self.predicted_value > self.lower_bound

    def __repr__(self) -> str:
        return (
            f"Forecast(date={self.date.strftime('%Y-%m-%d')}, "
            f"value={self.predicted_value:.2f}, "
            f"range=[{self.lower_bound:.2f}, {self.upper_bound:.2f}])"
        )


@dataclass
class ForecastResult:
    """
    Container for a complete forecast result with historical data and projections.
    
    Attributes:
        historical_data: Historical sales data
        forecast: List of forecast points
        metrics: Dictionary of forecast metrics
    """
    historical_dates: List[datetime]
    historical_values: List[float]
    forecast_dates: List[datetime]
    forecast_values: List[float]
    lower_bounds: List[float]
    upper_bounds: List[float]
    metrics: dict

    @classmethod
    def from_arrays(
        cls,
        historical_dates: List[datetime],
        historical_values: List[float],
        forecast_dates: List[datetime],
        forecast_values: List[float],
        lower_bounds: List[float],
        upper_bounds: List[float],
        metrics: dict
    ) -> "ForecastResult":
        """Create a ForecastResult from arrays of data."""
        return cls(
            historical_dates=historical_dates,
            historical_values=historical_values,
            forecast_dates=forecast_dates,
            forecast_values=forecast_values,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            metrics=metrics
        )

    def to_dataframe(self) -> "pd.DataFrame":
        """Convert forecast result to a pandas DataFrame."""
        import pandas as pd
        
        # Combine historical and forecast data
        dates = self.historical_dates + self.forecast_dates
        values = self.historical_values + [np.nan] * len(self.forecast_dates)
        forecast_only_values = [np.nan] * len(self.historical_dates) + self.forecast_values
        lower = [np.nan] * len(self.historical_dates) + self.lower_bounds
        upper = [np.nan] * len(self.historical_dates) + self.upper_bounds
        
        df = pd.DataFrame({
            "date": dates,
            "actual": values,
            "forecast": forecast_only_values,
            "lower_bound": lower,
            "upper_bound": upper
        })
        
        return df