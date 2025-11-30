import pandas as pd
import streamlit as st

def display_insight_box(title, content):
    """
    Displays insights using a stable Markdown blockquote to avoid Streamlit frontend errors.
    """
    st.markdown(f"""
    > **{title}**
    >
    {content}
    """)

def format_value(value):
    """Formats large numbers into readable strings (K, M, B)."""
    if value >= 1e9:
        return f"${value/1e9:,.1f}B" # Billions (Miles de Millones)
    elif value >= 1e6:
        return f"${value/1e6:,.1f}M" # Millions
    elif value >= 1e3:
        return f"${value/1e3:,.1f}K" # Thousands
    else:
        return f"${value:,.0f}"

def analyze_trend(df, date_col, value_col, period="M"):
    """
    Analyzes the trend of a value column over time.
    Returns a string describing the trend.
    """
    if df.empty:
        return "No hay datos suficientes para analizar la tendencia."
        
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Group by period
    trend = df.groupby(df[date_col].dt.to_period(period))[value_col].sum().sort_index()
    
    if len(trend) < 2:
        return "Se necesitan al menos dos periodos para calcular una tendencia."
        
    last_val = trend.iloc[-1]
    prev_val = trend.iloc[-2]
    
    if prev_val == 0:
        return "El valor anterior fue 0, no se puede calcular el cambio porcentual."
        
    pct_change = ((last_val - prev_val) / prev_val) * 100
    sign = "+" if pct_change > 0 else ""
    
    return f"📉 **Tendencia:** **{sign}{pct_change:.1f}%** vs periodo anterior ({format_value(last_val)} vs {format_value(prev_val)})."

def analyze_distribution(df, category_col, value_col, top_n=1):
    """
    Analyzes the distribution of a value across categories.
    Returns a string identifying the top category.
    """
    if df.empty:
        return "No hay datos."
        
    dist = df.groupby(category_col)[value_col].sum().sort_values(ascending=False)
    total = dist.sum()
    
    if total == 0:
        return "Total es 0."
        
    top_cat = dist.index[0]
    top_val = dist.iloc[0]
    share = (top_val / total) * 100
    
    return f"📊 **Principal:** **'{top_cat}'** concentra el **{share:.1f}%** del total ({format_value(top_val)})."

def analyze_performance(df, entity_col, value_col, label="Rentabilidad"):
    """
    Identifies top and bottom performers.
    """
    if df.empty:
        return "No hay datos."
        
    perf = df.groupby(entity_col)[value_col].sum().sort_values(ascending=False)
    
    top = perf.index[0]
    bottom = perf.index[-1]
    
    return f"🏆 **{label}:** Líder: **'{top}'** | Menor: **'{bottom}'**."
