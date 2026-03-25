"""Charts - Interactive visualizations using Plotly."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List


def render_trend_chart(
    monthly_data: pd.DataFrame,
    metric: str = "revenue",
    title: str = "Evolución de Ventas"
) -> None:
    """
    Render a line chart showing sales trend over time.
    
    Args:
        monthly_data: Monthly aggregated data
        metric: Metric to display ('revenue' or 'units')
        title: Chart title
    """
    df = monthly_data.copy()
    
    # Determine column name
    if metric == "revenue":
        y_col = "total_amount"
        y_label = "Ingresos ($)"
    else:
        y_col = "quantity"
        y_label = "Unidades"
    
    # Create figure
    fig = go.Figure()
    
    # Add line chart
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df[y_col],
        mode="lines+markers",
        name="Ventas",
        line=dict(color="#4F46E5", width=2),
        marker=dict(size=6, color="#4F46E5")
    ))
    
    # Add moving average
    df["ma_3"] = df[y_col].rolling(window=3, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["ma_3"],
        mode="lines",
        name="Media Móvil (3 meses)",
        line=dict(color="#F59E0B", width=2, dash="dash")
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"📈 {title}",
            font=dict(size=20)
        ),
        xaxis_title="Fecha",
        yaxis_title=y_label,
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_category_chart(
    category_data: pd.DataFrame,
    metric: str = "revenue",
    title: str = "Ventas por Categoría"
) -> None:
    """
    Render a bar chart showing sales by category.
    
    Args:
        category_data: Category aggregated data
        metric: Metric to display ('revenue' or 'units')
        title: Chart title
    """
    df = category_data.copy()
    
    # Determine column
    if metric == "revenue":
        y_col = "revenue"
        y_label = "Ingresos ($)"
    else:
        y_col = "units_sold"
        y_label = "Unidades"
    
    # Color palette
    colors = ["#4F46E5", "#10B981", "#F59E0B"]
    
    # Create figure
    fig = go.Figure(data=[
        go.Bar(
            x=df["category"],
            y=df[y_col],
            marker_color=colors[:len(df)],
            text=df[y_col].apply(lambda x: f"${x:,.0f}" if metric == "revenue" else f"{x:,.0f}"),
            textposition="auto"
        )
    ])
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"📊 {title}",
            font=dict(size=20)
        ),
        xaxis_title="Categoría",
        yaxis_title=y_label,
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_forecast_chart(
    forecast_result,
    title: str = "Forecast de Ventas"
) -> None:
    """
    Render a chart showing historical data and forecast.
    
    Args:
        forecast_result: ForecastResult object
        title: Chart title
    """
    # Create figure
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=forecast_result.historical_dates,
        y=forecast_result.historical_values,
        mode="lines+markers",
        name="Histórico",
        line=dict(color="#4F46E5", width=2),
        marker=dict(size=5)
    ))
    
    # Add forecast
    fig.add_trace(go.Scatter(
        x=forecast_result.forecast_dates,
        y=forecast_result.forecast_values,
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#10B981", width=2, dash="dash"),
        marker=dict(size=8, symbol="diamond")
    ))
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_result.forecast_dates + forecast_result.forecast_dates[::-1],
        y=forecast_result.upper_bounds + forecast_result.lower_bounds[::-1],
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Intervalo de Confianza",
        showlegend=True
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"🔮 {title}",
            font=dict(size=20)
        ),
        xaxis_title="Fecha",
        yaxis_title="Ingresos ($)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_product_table(
    product_data: pd.DataFrame,
    metric: str = "revenue",
    title: str = "Top Productos"
) -> None:
    """
    Render a table showing product performance.
    
    Args:
        product_data: Product aggregated data
        metric: Metric to sort by
        title: Table title
    """
    df = product_data.copy()
    
    # Sort by metric
    if metric == "revenue":
        df = df.sort_values("revenue", ascending=False)
    else:
        df = df.sort_values("units_sold", ascending=False)
    
    # Format columns
    display_df = df.copy()
    display_df["revenue"] = display_df["revenue"].apply(lambda x: f"${x:,.2f}")
    display_df["units_sold"] = display_df["units_sold"].apply(lambda x: f"{x:,}")
    
    # Rename columns for display
    display_df.columns = ["ID", "Producto", "Categoría", "Ingresos", "Unidades"]
    
    # Render table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


def render_pie_chart(
    category_data: pd.DataFrame,
    title: str = "Distribución por Categoría"
) -> None:
    """
    Render a pie chart showing category distribution.
    
    Args:
        category_data: Category aggregated data
        title: Chart title
    """
    fig = go.Figure(data=[
        go.Pie(
            labels=category_data["category"],
            values=category_data["revenue"],
            hole=0.4,
            marker=dict(colors=["#4F46E5", "#10B981", "#F59E0B"]),
            textinfo="label+percent",
            textposition="outside"
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"🥧 {title}",
            font=dict(size=20)
        ),
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_heatmap(
    daily_data: pd.DataFrame,
    title: str = "Patrón de Ventas Semanal"
) -> None:
    """
    Render a heatmap showing weekly patterns.
    
    Args:
        daily_data: Daily aggregated data
        title: Chart title
    """
    df = daily_data.copy()
    
    # Add day of week
    df["day_of_week"] = df["date"].dt.dayofweek
    df["week"] = df["date"].dt.isocalendar().week
    
    # Pivot data
    pivot = df.pivot_table(
        values="total_amount",
        index="day_of_week",
        columns="week",
        aggfunc="sum"
    ).fillna(0)
    
    # Day names
    day_names = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    pivot.index = day_names
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Blues",
        colorbar=dict(title="Ingresos")
    ))
    
    fig.update_layout(
        title=dict(
            text=f"🔥 {title}",
            font=dict(size=20)
        ),
        xaxis_title="Semana",
        yaxis_title="Día",
        template="plotly_white",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)