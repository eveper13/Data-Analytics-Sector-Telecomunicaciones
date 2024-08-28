import streamlit as st
from utils import load_data
from kpis import kpi_1, kpi2
import plotly.express as px
import base64
from provincias import provincias_dashboard
from localidades import localidades_dashboard 

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# función set_background()
set_background('img/fondo.jpg') 

# Menú principal
st.title("Dashboard Global")

menu = st.sidebar.radio("Selecciona una opción", ["Análisis de KPIs", "Dashboard Global", "Dashboard de Provincias", "Dashboard de Localidades"])

if menu == "Análisis de KPIs":
    st.subheader("Selecciona el KPI")

    # Cargar y mostrar KPI 1
    if st.button("Mostrar KPI 1: Crecimiento de Accesos"):
        df_provincias = load_data('Dataset_procesados/Penetracion_hogares.csv')
        kpi_1(df_provincias)

    # Cargar y mostrar KPI 2
    if st.button("Mostrar KPI 2: Crecimiento de Velocidades Promedio"):
        df_velocidades = load_data('Dataset_procesados/Accesos_velocidad_Provincia.csv')
        kpi2(df_velocidades)

elif menu == "Dashboard Global":
    st.subheader("Dashboard Global")

    # Seleccionar Tecnología
    tecnologias = ['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', '+ 1 Mbps - 6 Mbps', 
                   '+ 6 Mbps - 10 Mbps', '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', 
                   '+ 30 Mbps', 'OTROS']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología", tecnologias)

    # Cargar datasets necesarios para el Dashboard Global
    df_accesos_velocidad = load_data('Dataset_procesados/Accesos_velocidad_Provincia.csv')
    df_ingresos = load_data('Dataset_procesados/ingresos.csv')
    df_velocidad = load_data('Dataset_procesados/Velocidad % por prov.csv')

    # Filtrar datos de ingresos por año y trimestre
    df_ingresos_filtered = df_ingresos[(df_ingresos['Año'] >= 2018) & (df_ingresos['Año'] <= 2024)]

    # Gráfico de Top 10 Provincias por Tecnología
    df_provincias = df_accesos_velocidad.groupby('Provincia').mean().reset_index()
    df_provincias = df_provincias.sort_values(by=tecnologia_seleccionada, ascending=False).head(10)
    fig_provincias = px.bar(df_provincias, x='Provincia', y=tecnologia_seleccionada,
                            title=f"Top 10 Provincias por {tecnologia_seleccionada}",
                            height=400)  # Ajusta la altura del gráfico
    
    # Identificación de Provincias con Menor Acceso
    df_accesos = df_accesos_velocidad.groupby('Provincia').mean().reset_index()
    df_accesos = df_accesos.sort_values(by=tecnologia_seleccionada, ascending=True).head(10)
    fig_accesos = px.bar(df_accesos, x='Provincia', y=tecnologia_seleccionada,
                         title=f"Provincias con Menor Promedio de {tecnologia_seleccionada}",
                         height=400)  # Ajusta la altura del gráfico

    # Gráfico de Ingresos
    df_ingresos_grouped = df_ingresos_filtered.groupby(['Año', 'Trimestre'])['Ingresos (miles de pesos)'].sum().reset_index()
    fig_ingresos = px.line(df_ingresos_grouped, x='Trimestre', y='Ingresos (miles de pesos)', color='Año',
                           title="Ingresos por Año y Trimestre (2018-2024)",
                           height=400)  # Ajusta la altura del gráfico

    # Gráfico de Velocidad Media por Provincia (10 provincias)
    df_velocidad_grouped = df_velocidad.groupby(['Año', 'Trimestre', 'Provincia'])['Mbps (Media de bajada)'].mean().reset_index()
    top_provincias = df_velocidad_grouped['Provincia'].value_counts().head(10).index
    df_velocidad_top = df_velocidad_grouped[df_velocidad_grouped['Provincia'].isin(top_provincias)]
    fig_velocidad = px.line(df_velocidad_top, x='Trimestre', y='Mbps (Media de bajada)', color='Provincia',
                            title="Velocidad Media por Provincia (Top 10)",
                            height=400)  # Ajusta la altura del gráfico

    # Gráfico de Torta para 6 provincias
    top_provincias_for_pie = df_velocidad['Provincia'].value_counts().head(6).index
    df_velocidad_pie = df_velocidad[df_velocidad['Provincia'].isin(top_provincias_for_pie)]
    df_pie = df_velocidad_pie.groupby('Provincia')['Mbps (Media de bajada)'].mean().reset_index()
    fig_pie = px.pie(df_pie, names='Provincia', values='Mbps (Media de bajada)', 
                     title="Distribución de Velocidad Media por Provincia (Top 6)",
                     height=400)  # Ajusta la altura del gráfico

    # Mostrar gráficos distribuidos en una sola columna con tamaño ajustado
    st.plotly_chart(fig_provincias, use_container_width=True)
    st.plotly_chart(fig_accesos, use_container_width=True)
    st.plotly_chart(fig_ingresos, use_container_width=True)
    st.plotly_chart(fig_velocidad, use_container_width=True)
    st.plotly_chart(fig_pie, use_container_width=True)

elif menu == "Dashboard de Provincias":
    st.subheader("Dashboard de Provincias")

    # Cargar dataset para el dashboard de provincias
    df_provincias = load_data('Dataset_procesados/Accesos_Tecnología_Provincia.csv')
    
    # Llamar a la función para mostrar el dashboard de provincias
    provincias_dashboard(df_provincias)

elif menu == "Dashboard de Localidades":
    st.subheader("Dashboard de Localidades")

    # Cargar dataset para el dashboard de localidades
    df_localidades = load_data('Dataset_procesados/Accesos_tecnologia_localidades.csv')  # Cambia el nombre del archivo según corresponda
    
    # Llamar a la función para mostrar el dashboard de localidades
    localidades_dashboard(df_localidades)
