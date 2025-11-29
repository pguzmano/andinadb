# Dashboard Comercializadora Andina SAS

Dashboard interactivo de análisis de negocios para Comercializadora Andina SAS, construido con Streamlit y conectado a Supabase.

## 🚀 Características

- **Vista General**: KPIs principales, tendencias de ventas y análisis regional
- **Rentabilidad**: Análisis detallado de márgenes por producto y categoría
- **Gestión de Clientes**: Segmentación y análisis geográfico
- **Importaciones**: Seguimiento de costos y proveedores
- **Inventario**: Control de stock por centro logístico
- **Riesgo Crediticio**: Análisis de cartera y morosidad

## 📋 Requisitos

- Python 3.9+
- Cuenta de Supabase (base de datos PostgreSQL)

## 🔧 Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/pguzmano/andinadb.git
cd andinadb
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar secretos de Supabase:
Crear archivo `.streamlit/secrets.toml`:
```toml
[connections.supabase]
dialect = "postgresql"
host = "your-pooler-host.supabase.com"
port = "5432"
database = "postgres"
username = "postgres.your-project-id"
password = "your-password"
```

4. Ejecutar la aplicación:
```bash
streamlit run dashboard/app.py
```

## 🌐 Despliegue

### Streamlit Cloud (Recomendado)

1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Conectar tu repositorio de GitHub
3. Configurar los secretos en la interfaz web
4. Desplegar

### Render

1. Crear cuenta en [render.com](https://render.com)
2. Crear nuevo "Web Service"
3. Conectar repositorio
4. Configurar variables de entorno
5. Desplegar

## 📊 Estructura del Proyecto

```
dashboard/
├── app.py                  # Aplicación principal
├── components/             # Componentes UI reutilizables
│   └── sidebar.py
├── data/                   # Carga y procesamiento de datos
│   ├── loader.py
│   └── processor.py
├── views/                  # Vistas del dashboard
│   ├── overview.py
│   ├── profitability.py
│   ├── customers.py
│   ├── imports.py
│   ├── inventory.py
│   └── credit_risk.py
└── utils/                  # Utilidades
    └── insights.py
```

## 🔒 Seguridad

- Los secretos de base de datos NO están incluidos en el repositorio
- Configure las variables de entorno en su plataforma de despliegue
- Los archivos CSV locales están excluidos del control de versiones

## 📝 Licencia

Proyecto privado - Comercializadora Andina SAS
