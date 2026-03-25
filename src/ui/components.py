"""Components - Reusable UI components for the dashboard."""

import streamlit as st
from typing import List, Dict, Optional, Tuple


def render_kpi_cards(
    metrics: Dict[str, float],
    previous_metrics: Optional[Dict[str, float]] = None
) -> None:
    """
    Render KPI metric cards.
    
    Args:
        metrics: Dictionary of metric values
        previous_metrics: Optional previous period metrics for comparison
    """
    # Define card configurations
    card_config = {
        "total_revenue": {
            "label": "Ingresos Totales",
            "format": "currency",
            "icon": "💰"
        },
        "total_units": {
            "label": "Unidades Vendidas",
            "format": "number",
            "icon": "📦"
        },
        "average_ticket": {
            "label": "Ticket Promedio",
            "format": "currency",
            "icon": "🛒"
        },
        "mom_growth": {
            "label": "Crecimiento MoM",
            "format": "percentage",
            "icon": "📈"
        },
        "yoy_growth": {
            "label": "Crecimiento YoY",
            "format": "percentage",
            "icon": "📊"
        },
    }
    
    # Create columns
    cols = st.columns(len(metrics))
    
    for idx, (key, value) in enumerate(metrics.items()):
        config = card_config.get(key, {"label": key, "format": "number", "icon": "📌"})
        
        # Format value
        if config["format"] == "currency":
            display_value = f"${value:,.2f}"
        elif config["format"] == "percentage":
            sign = "+" if value > 0 else ""
            display_value = f"{sign}{value:.1f}%"
        else:
            display_value = f"{value:,.0f}"
        
        # Calculate delta if previous metrics available
        delta = None
        if previous_metrics and key in previous_metrics:
            delta = value - previous_metrics[key]
        
        # Render card
        with cols[idx]:
            st.metric(
                label=f"{config['icon']} {config['label']}",
                value=display_value,
                delta=delta
            )


def render_filters(
    categories: List[str],
    products: List[Dict[str, str]],
    default_category: str = "Todas",
    default_product: str = "Todos"
) -> Tuple[str, str, int]:
    """
    Render filter controls.
    
    Args:
        categories: List of available categories
        products: List of products with id, name, category
        default_category: Default category selection
        default_product: Default product selection
        
    Returns:
        Tuple of (selected_category, selected_product, selected_months)
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox(
            "📁 Categoría",
            options=categories,
            index=categories.index(default_category) if default_category in categories else 0
        )
    
    with col2:
        # Filter products by selected category
        if selected_category != "Todas":
            filtered_products = [p for p in products if p["category"] == selected_category]
        else:
            filtered_products = products
        
        product_options = ["Todos"] + [p["name"] for p in filtered_products]
        selected_product_name = st.selectbox(
            "📦 Producto",
            options=product_options,
            index=0
        )
        
        # Get product ID from name
        if selected_product_name == "Todos":
            selected_product = "Todos"
        else:
            selected_product = next(
                p["id"] for p in filtered_products if p["name"] == selected_product_name
            )
    
    with col3:
        selected_months = st.selectbox(
            "📅 Período",
            options=[3, 6, 12, 24],
            index=3,
            format_func=lambda x: f"Últimos {x} meses"
        )
    
    return selected_category, selected_product, selected_months


def render_metric_selector() -> str:
    """
    Render metric selector.
    
    Returns:
        Selected metric ('revenue' or 'units')
    """
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.radio(
            "📊 Métrica principal",
            options=["revenue", "units"],
            format_func=lambda x: "Ingresos" if x == "revenue" else "Unidades",
            horizontal=True
        )
    
    return metric


def render_period_selector() -> int:
    """
    Render period selector for forecast.
    
    Returns:
        Selected forecast period in months
    """
    period = st.selectbox(
        "🔮 Período de Forecast",
        options=[3, 6, 9, 12],
        index=1,
        format_func=lambda x: f"{x} meses"
    )
    
    return period


def render_section_header(title: str, icon: str = "📈") -> None:
    """
    Render a section header.
    
    Args:
        title: Section title
        icon: Icon to display
    """
    st.markdown(f"## {icon} {title}")


def render_info_box(message: str, icon: str = "ℹ️") -> None:
    """
    Render an info box.
    
    Args:
        message: Message to display
        icon: Icon to display
    """
    st.info(f"{icon} {message}")


def render_warning_box(message: str, icon: str = "⚠️") -> None:
    """
    Render a warning box.
    
    Args:
        message: Message to display
        icon: Icon to display
    """
    st.warning(f"{icon} {message}")