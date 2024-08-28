import streamlit as st
from utils import load_data
from kpis import kpi_1, kpi2
import plotly.express as px
import base64
from provincias import provincias_dashboard
from localidades import localidades_dashboard 

# Define la URL de la imagen de fondo
image_url = '/img/fondo.jpg'  # Asegúrate de que la ruta sea correcta

# Estilo CSS para establecer la imagen de fondo
css = f"""
    <style>
    .main {{
        background-image: url("{image_url}");
        background-size: cover; /* Ajusta la imagen para cubrir todo el fondo */
        background-position: center; /* Centra la imagen */
        color: #ffffff; /* Texto blanco */
    }}
    .streamlit-expanderHeader {{
        color: #ffffff; /* Color del texto en los encabezados de los expanders */
    }}
    .stButton>button {{
        background-color: #0056b3; /* Fondo de los botones */
        color: white; /* Texto de los botones */
    }}
    .stTextInput>div>input {{
        background-color: #ffffff; /* Fondo de los campos de entrada */
        color: #000000; /* Texto en los campos de entrada */
    }}
    </style>
"""

# Agregar el CSS a la aplicación
st.markdown(css, unsafe_allow_html=True)


# Menú principal

st.title("Dashboard De Telecomunicaciones")

menu = st.sidebar.radio("Selecciona una opción", ["Análisis de KPIs", "Dashboard Global", "Dashboard de Provincias", "Dashboard de Localidades"])


if menu == "Análisis de KPIs":

    st.subheader("Análisis de KPIs")

    # Botones para seleccionar KPI
    selected_kpi = st.radio("Selecciona el KPI a mostrar", ["KPI 1", "KPI 2"])

    if selected_kpi == "KPI 1":
        st.subheader("KPI 1: Crecimiento de Accesos")
        df_provincias = load_data('Dataset_procesados/Penetracion_hogares.csv')

        kpi1_result = kpi_1(df_provincias)  # Asegúrate de que kpi_1 devuelva un valor
        st.metric(label="KPI 1: Crecimiento de Accesos", value=kpi1_result)

        # Descripcion
        st.write("Aumentar en un 2% el acceso al servicio de internet para el próximo trimestre, cada 100 hogares, por provincia")
        
    elif selected_kpi == "KPI 2":
        st.subheader("KPI 2: Crecimiento de Velocidades Promedio")
        df_velocidades = load_data('Dataset_procesados/Accesos_velocidad_Provincia.csv')

        kpi2_result = kpi2(df_velocidades)  # Asegúrate de que kpi2 devuelva un valor
        st.metric(label="KPI 2: Crecimiento de Velocidades Promedio", value=kpi2_result)

        # Descripcion
        st.write("Este valor representa el crecimiento promedio en las velocidades de acceso a internet a nivel provincial")

elif menu == "Dashboard Global":
    st.subheader("Dashboard Global")

    # Seleccionar Tecnología
    tecnologias = ['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', '+ 1 Mbps - 6 Mbps', 
                   '+ 6 Mbps - 10 Mbps', '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', 
                   '+ 30 Mbps', 'OTROS']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología", tecnologias)

    # Cargar datasets necesarios para el Dashboard Global
    df_accesos_velocidad = load_data('Dataset_procesados/Accesos_velocidad_Provincia.csv')
    df_ingresos = load_data('Dataset_procesados/Ingresos.csv')
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

    # Columna para gráficos Top 10 y Menor Acceso
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_provincias, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_accesos, use_container_width=True)

    # Gráfico de Ingresos
    df_ingresos_grouped = df_ingresos_filtered.groupby(['Año', 'Trimestre'])['Ingresos (miles de pesos)'].sum().reset_index()
    fig_ingresos = px.line(df_ingresos_grouped, x='Trimestre', y='Ingresos (miles de pesos)', color='Año',
                           title="Ingresos por Año y Trimestre (2018-2024)",
                           height=400)  # Ajusta la altura del gráfico

    # Nuevo gráfico en lugar de líneas de velocidades
    df_velocidad_grouped = df_velocidad.groupby(['Año', 'Trimestre', 'Provincia'])['Mbps (Media de bajada)'].mean().reset_index()
    top_provincias = df_velocidad_grouped['Provincia'].value_counts().head(10).index
    df_velocidad_top = df_velocidad_grouped[df_velocidad_grouped['Provincia'].isin(top_provincias)]
    fig_velocidad = px.bar(df_velocidad_top, x='Trimestre', y='Mbps (Media de bajada)', color='Provincia',
                           title="Velocidad Media por Provincia (Top 10)",
                           height=400)  # Cambiar a gráfico de barras

    # Gráfico de Torta para 6 provincias
    top_provincias_for_pie = df_velocidad['Provincia'].value_counts().head(6).index
    df_velocidad_pie = df_velocidad[df_velocidad['Provincia'].isin(top_provincias_for_pie)]
    df_pie = df_velocidad_pie.groupby('Provincia')['Mbps (Media de bajada)'].mean().reset_index()
    fig_pie = px.pie(df_pie, names='Provincia', values='Mbps (Media de bajada)', 
                     title="Distribución de Velocidad Media por Provincia (Top 6)",
                     height=400)  # Ajusta la altura del gráfico

    # Mostrar gráficos adicionales
    st.subheader("Otros Gráficos")

    # Gráficos distribuidos en una columna
    st.plotly_chart(fig_ingresos, use_container_width=True)
    st.plotly_chart(fig_velocidad, use_container_width=True)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Agregar un resumen o insights clave con formato bonito
    st.markdown("""
    <div style="background-color:#f1f1f1; padding:20px; border-radius:10px; color:#2c3e50;">
        <h2 style="color:#2c3e50;">Resumen e Insights Clave</h2>
        <p><strong>Resumen:</strong> Este dashboard proporciona una visión integral del acceso a internet en diferentes provincias.</p>
        <ul>
            <li><strong>Top 10 Provincias por Tecnología:</strong> Muestra las provincias con el mejor acceso a diferentes tecnologías de internet.</li>
            <li><strong>Provincias con Menor Promedio:</strong> Identifica las provincias con el menor acceso promedio a las tecnologías seleccionadas.</li>
            <li><strong>Ingresos:</strong> Detalla cómo los ingresos están cambiando a lo largo del tiempo, analizando los ingresos por año y trimestre.</li>
            <li><strong>Velocidad Media por Provincia:</strong> Muestra la velocidad media de acceso a internet en las provincias principales.</li>
            <li><strong>Distribución de Velocidad Media:</strong> Representa la distribución de la velocidad media en las seis provincias principales.</li>
        </ul>
        <p><strong>Insights Clave:</strong></p>
        <ul>
            <li>Identifica áreas de mejora en el acceso a internet y áreas donde se está logrando un buen rendimiento.</li>
            <li>Analiza cómo los ingresos están cambiando a lo largo del tiempo y cómo esto puede correlacionarse con el acceso a internet.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Dashboard de Provincias":
    st.subheader("Dashboard de Provincias")

    # Cargar dataset para el dashboard de provincias
    df_provincias = load_data('Dataset_procesados/Accesos_Tecnología_Provincia.csv')
    
    # Llamar a la función para mostrar el dashboard de provincias
    provincias_dashboard(df_provincias)

elif menu == "Dashboard de Localidades":
    st.subheader("Dashboard de Localidades")

    # Cargar dataset para el dashboard de localidades
    df_localidades = load_data('Dataset_procesados/Accesos_tecnologia_localidades.csv')
    
    # Llamar a la función para mostrar el dashboard de localidades
    localidades_dashboard(df_localidades)
