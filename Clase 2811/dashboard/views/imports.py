import streamlit as st
import plotly.express as px
import pandas as pd
from utils.insights import analyze_trend, analyze_performance, display_insight_box

def show(data):
    st.title("Importaciones y Costos")
    
    if "importaciones" not in data:
        st.error("Datos no disponibles.")
        return
        
    df = data["importaciones"].copy()
    
    # Ensure dates
    df['fecha_orden'] = pd.to_datetime(df['fecha_orden'])
    df['fecha_llegada'] = pd.to_datetime(df['fecha_llegada'])
    
    # Calculate Lead Time
    df['lead_time_days'] = (df['fecha_llegada'] - df['fecha_orden']).dt.days
    
    # --- KPIs ---
    total_imports_usd = df['costo_mercancia_usd'].sum()
    avg_lead_time = df['lead_time_days'].mean()
    total_shipments = len(df)
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Importaciones (USD)", f"${total_imports_usd:,.0f}")
    kpi2.metric("Tiempo Promedio Entrega", f"{avg_lead_time:.1f} días")
    kpi3.metric("Total Envíos", f"{total_shipments}")
    
    st.markdown("---")
    
    # --- Insights ---
    st.subheader("💡 Insights Automáticos")
    insight_trend = analyze_trend(df, 'fecha_orden', 'costo_mercancia_usd')
    insight_supp = analyze_performance(df, 'proveedor', 'costo_mercancia_usd', label="Proveedor")
    
    content = f"""
    *   {insight_trend}
    *   {insight_supp}
    """
    display_insight_box("Análisis de Importaciones", content)
    
    st.markdown("---")
    
    # 1. Cost Trend
    st.subheader("Tendencia de Costos de Importación (USD)")
    monthly_costs = df.groupby(df['fecha_orden'].dt.to_period("M"))['costo_mercancia_usd'].sum().reset_index()
    monthly_costs['fecha_orden'] = monthly_costs['fecha_orden'].dt.to_timestamp()
    
    fig_trend = px.line(monthly_costs, x='fecha_orden', y='costo_mercancia_usd', markers=True, labels={'fecha_orden': 'Fecha Orden', 'costo_mercancia_usd': 'Costo (USD)'})
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 2. Top Suppliers
    st.subheader("Mejores Proveedores")
    col1, col2 = st.columns(2)
    
    with col1:
        # By Value
        top_suppliers_val = df.groupby("proveedor")['costo_mercancia_usd'].sum().reset_index().sort_values("costo_mercancia_usd", ascending=False).head(10)
        fig_supp_val = px.bar(
            top_suppliers_val, 
            x='costo_mercancia_usd', 
            y='proveedor', 
            orientation='h', 
            title="Por Valor (USD)", 
            text_auto='.2s',
            labels={'costo_mercancia_usd': 'Costo (USD)', 'proveedor': 'Proveedor'}
        )
        st.plotly_chart(fig_supp_val, use_container_width=True)
        
    with col2:
        # By Volume (count of imports)
        top_suppliers_vol = df.groupby("proveedor")['importacion_id'].count().reset_index().rename(columns={'importacion_id': 'count'}).sort_values("count", ascending=False).head(10)
        fig_supp_vol = px.bar(
            top_suppliers_vol, 
            x='count', 
            y='proveedor', 
            orientation='h', 
            title="Por Volumen (Envíos)", 
            text_auto=True,
            labels={'count': 'Cantidad Envíos', 'proveedor': 'Proveedor'}
        )
        st.plotly_chart(fig_supp_vol, use_container_width=True)
        
    # 3. Lead Time Analysis
    st.subheader("Análisis de Tiempos de Entrega")
    st.caption("Días entre Fecha de Orden y Fecha de Llegada")
    
    fig_hist = px.histogram(df, x='lead_time_days', nbins=20, title="Distribución de Tiempos de Entrega", labels={'lead_time_days': 'Días'})
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Average Lead Time by Supplier
    avg_lead_time_supp = df.groupby("proveedor")['lead_time_days'].mean().reset_index().sort_values("lead_time_days", ascending=False).head(10)
    st.write("Tiempo Promedio de Entrega por Proveedor (Top 10 Más Lentos)")
    st.dataframe(
        avg_lead_time_supp, 
        column_config={
            "proveedor": "Proveedor",
            "lead_time_days": st.column_config.NumberColumn("Días Promedio", format="%.1f")
        },
        use_container_width=True
    )
