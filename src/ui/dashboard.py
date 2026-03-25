"""Dashboard - Main dashboard view and orchestration."""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple

from ..services.data_service import DataService
from ..services.forecast_service import ForecastService
from ..services.metrics_service import MetricsService
from .components import (
    render_kpi_cards,
    render_filters,
    render_metric_selector,
    render_section_header,
    render_period_selector
)
from .charts import (
    render_trend_chart,
    render_category_chart,
    render_forecast_chart,
    render_product_table,
    render_pie_chart
)


class Dashboard:
    """
    Main dashboard for the sales forecast application.
    
    Orchestrates data services, metrics, and UI components.
    """
    
    def __init__(self):
        """Initialize the dashboard with services."""
        self.data_service = DataService()
        self.forecast_service = ForecastService()
        self.metrics_service = MetricsService()
        
        # Initialize session state
        if "sales_data" not in st.session_state:
            st.session_state.sales_data = None
    
    def load_data(self, months: int = 24) -> pd.DataFrame:
        """
        Load or generate sales data.
        
        Args:
            months: Number of months of data
            
        Returns:
            Sales DataFrame
        """
        if st.session_state.sales_data is None:
            st.session_state.sales_data = self.data_service.get_sales_data(months=months)
        return st.session_state.sales_data
    
    def apply_filters(
        self,
        df: pd.DataFrame,
        category: str,
        product: str,
        months: int
    ) -> pd.DataFrame:
        """
        Apply filters to the data.
        
        Args:
            df: Sales DataFrame
            category: Category filter
            product: Product filter
            months: Period filter
            
        Returns:
            Filtered DataFrame
        """
        # Apply period filter
        df = self.data_service.filter_by_period(df, months)
        
        # Apply category filter
        df = self.data_service.filter_by_category(df, category)
        
        # Apply product filter
        df = self.data_service.filter_by_product(df, product)
        
        return df
    
    def render(self) -> None:
        """Render the complete dashboard."""
        # Page configuration
        st.set_page_config(
            page_title="Dashboard de Forecast de Ventas",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.title("📊 Dashboard de Forecast de Ventas")
        st.markdown("---")
        
        # Load data
        sales_data = self.load_data(months=24)
        
        # Get filter options
        categories = self.data_service.get_categories()
        products = self.data_service.get_products()
        
        # Render filters
        selected_category, selected_product, selected_months = render_filters(
            categories=categories,
            products=products
        )
        
        st.markdown("---")
        
        # Apply filters
        filtered_data = self.apply_filters(
            sales_data,
            selected_category,
            selected_product,
            selected_months
        )
        
        # Calculate metrics
        monthly_data = self.data_service.get_monthly_data(filtered_data)
        metrics = self.metrics_service.calculate_all_metrics(
            filtered_data,
            monthly_data
        )
        
        # Render KPI cards
        render_section_header("Métricas Clave", "💡")
        render_kpi_cards(metrics)
        
        st.markdown("---")
        
        # Render trend chart
        render_section_header("Análisis de Tendencias", "📈")
        metric = render_metric_selector()
        render_trend_chart(monthly_data, metric=metric)
        
        st.markdown("---")
        
        # Render category charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_section_header("Ventas por Categoría", "📊")
            category_data = self.data_service.get_category_data(filtered_data)
            render_category_chart(category_data, metric=metric)
        
        with col2:
            render_section_header("Distribución", "🥧")
            render_pie_chart(category_data)
        
        st.markdown("---")
        
        # Render forecast
        render_section_header("Forecast de Ventas", "🔮")
        forecast_period = render_period_selector()
        
        # Generate forecast
        forecast_result = self.forecast_service.generate_forecast(
            monthly_data,
            forecast_months=forecast_period
        )
        
        # Display forecast metrics
        fc_metrics = forecast_result.metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📊 Promedio Histórico",
                value=f"${fc_metrics['historical_avg']:,.2f}"
            )
        with col2:
            st.metric(
                label="🔮 Promedio Forecast",
                value=f"${fc_metrics['forecast_avg']:,.2f}"
            )
        with col3:
            trend_icon = "📈" if fc_metrics['trend_direction'] == "up" else "📉"
            st.metric(
                label=f"{trend_icon} Tendencia",
                value=fc_metrics['trend_direction'].upper(),
                delta=f"{fc_metrics['growth_rate']:.1f}%"
            )
        
        # Render forecast chart
        render_forecast_chart(forecast_result)
        
        st.markdown("---")
        
        # Render product table
        render_section_header("Top Productos", "🏆")
        product_data = self.data_service.get_product_data(filtered_data)
        render_product_table(product_data, metric=metric)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        ---
        ### 📝 Acerca de este Dashboard
        
        Este dashboard genera datos ficticios de ventas con los siguientes parámetros:
        - **Período**: 24 meses de datos históricos
        - **Productos**: 10 productos en 3 categorías
        - **Estacionalidad**: Patrones estacionales realistas
        - **Tendencia**: Crecimiento gradual del 8% anual
        
        El forecast utiliza regresión lineal con factores estacionales para proyectar ventas futuras.
        """)


def render_dashboard() -> None:
    """Render the dashboard (entry point for main.py)."""
    dashboard = Dashboard()
    dashboard.render()