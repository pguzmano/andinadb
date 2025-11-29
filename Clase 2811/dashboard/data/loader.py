import pandas as pd
import streamlit as st
import os

# Configuration
DATA_PATH = "c:/Users/Pedro Luis/Downloads/Clase 2811/Data/"

@st.cache_data
def load_data():
    """
    Loads all necessary data from Supabase.
    Falls back to CSV files if connection fails.
    Returns a dictionary of DataFrames.
    """
    # Map keys to table names
    tables = {
        "ventas": "ventas_andina",
        "clientes": "clientes_andina",
        "productos": "productos_andina",
        "cartera": "cartera_andina",
        "inventario": "inventario_andina",
        "importaciones": "importaciones_andina"
    }
    
    # Fallback file mapping
    files = {
        "ventas": "ventas_andina.csv",
        "clientes": "clientes_andina.csv",
        "productos": "productos_andina.csv",
        "cartera": "cartera_andina.csv",
        "inventario": "inventario_andina.csv",
        "importaciones": "importaciones_andina.csv"
    }
    
    data = {}
    
    try:
        # Try to connect to Supabase
        conn = st.connection("supabase", type="sql")
        
        for key, table_name in tables.items():
            try:
                # Try loading from Supabase
                df = conn.query(f"SELECT * FROM {table_name}", ttl=600)
                data[key] = df
            except Exception as e:
                # Fallback to CSV for this specific table
                st.warning(f"⚠️ No se pudo cargar '{table_name}' desde Supabase. Usando CSV local.")
                file_path = os.path.join(DATA_PATH, files[key])
                try:
                    if key == "importaciones":
                        df = pd.read_csv(file_path, sep=';', decimal=',')
                    else:
                        df = pd.read_csv(file_path)
                    data[key] = df
                except Exception as csv_e:
                    st.error(f"Error cargando CSV para {key}: {csv_e}")
                    data[key] = pd.DataFrame()
    
    except Exception as conn_error:
        # If connection itself fails, use all CSVs
        st.warning(f"⚠️ No se pudo conectar a Supabase. Usando todos los archivos CSV locales.")
        
        for key, filename in files.items():
            file_path = os.path.join(DATA_PATH, filename)
            try:
                if key == "importaciones":
                    df = pd.read_csv(file_path, sep=';', decimal=',')
                else:
                    df = pd.read_csv(file_path)
                data[key] = df
            except Exception as e:
                st.error(f"Error loading {filename}: {e}")
                data[key] = pd.DataFrame()
            
    return data
