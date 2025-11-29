import streamlit as st
import plotly.express as px
from utils.insights import analyze_distribution, analyze_performance, display_insight_box

def show(data):
    st.title("Gestión de Clientes")
    
    if "ventas_enriched" not in data:
        st.error("Datos no disponibles.")
        return
        
    df = data["ventas_enriched"]
    
    # --- Filters ---
    with st.expander("Filtros", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            segments = ["Todos"] + sorted(list(df["segmento"].dropna().unique()))
            selected_seg = st.selectbox("Seleccionar Segmento", segments)
            
        if selected_seg != "Todos":
            df = df[df["segmento"] == selected_seg]
            
    st.markdown("---")
    
    # --- Insights ---
    st.subheader("💡 Insights Automáticos")
    insight_seg = analyze_distribution(df, 'segmento', 'subtotal_cop')
    insight_city = analyze_distribution(df, 'ciudad', 'subtotal_cop')
    
    content = f"""
    *   {insight_seg}
    *   {insight_city}
    """
    display_insight_box("Perfil del Cliente", content)
    
    st.markdown("---")
    
    # 1. Sales by Segment (Pie Chart)
    st.subheader("Participación de Ingresos por Segmento")
    segment_sales = df.groupby("segmento")['subtotal_cop'].sum().reset_index()
    fig_segment = px.pie(
        segment_sales, 
        values='subtotal_cop', 
        names='segmento', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'subtotal_cop': 'Ingresos', 'segmento': 'Segmento'}
    )
    st.plotly_chart(fig_segment, use_container_width=True)
    
    # 2. Top Customers Leaderboard
    st.subheader("Ranking de Mejores Clientes")
    
    # Check for client name column
    client_name_col = 'nombre_cliente'
    if client_name_col not in df.columns:
        # Fallback if name is missing
        client_name_col = 'cliente_id'
        
    top_customers = df.groupby(['cliente_id', client_name_col]).agg({
        'subtotal_cop': 'sum',
        'margen_total_cop': 'sum',
        'venta_id': 'count'
    }).reset_index().rename(columns={'venta_id': 'transacciones'})
    
    # Calculate profit margin per customer
    top_customers['profit_margin'] = (top_customers['margen_total_cop'] / top_customers['subtotal_cop']) * 100
    
    top_customers = top_customers.sort_values("subtotal_cop", ascending=False).head(20)
    
    st.dataframe(
        top_customers,
        column_config={
            "cliente_id": "ID Cliente",
            "nombre_cliente": "Cliente",
            "transacciones": "Transacciones",
            "subtotal_cop": st.column_config.NumberColumn("Ingresos Totales", format="$%.0f"),
            "margen_total_cop": st.column_config.NumberColumn("Utilidad Total", format="$%.0f"),
            "profit_margin": st.column_config.NumberColumn("Margen %", format="%.1f%%"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # 3. Geographic Distribution
    st.subheader("Top Ciudades por Ingresos")
    city_sales = df.groupby("ciudad")['subtotal_cop'].sum().reset_index().sort_values("subtotal_cop", ascending=False).head(15)
    
    fig_city = px.bar(
        city_sales, 
        x='ciudad', 
        y='subtotal_cop',
        text_auto='.2s',
        labels={'subtotal_cop': 'Ingresos (COP)', 'ciudad': 'Ciudad'},
        template="plotly_white"
    )
    st.plotly_chart(fig_city, use_container_width=True)
