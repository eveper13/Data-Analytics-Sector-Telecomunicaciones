import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster

def provincias_dashboard(provincias_df):
    st.title('Por Provincias')

    # Filtros para Provincia, Año, y Trimestre
    selected_provincia = st.sidebar.selectbox('Seleccionar Provincia', provincias_df['Provincia'].unique())
    selected_ano = st.sidebar.selectbox('Seleccionar Año', provincias_df['Año'].unique())
    selected_trimestre = st.sidebar.selectbox('Seleccionar Trimestre', provincias_df['Trimestre'].unique())

    # Filtros para la tecnología
    tech_columns = ['ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless', 'Otros']
    selected_technology = st.sidebar.selectbox('Seleccionar Tecnología', tech_columns)

    # Filtrar los datos por las selecciones
    filtered_data = provincias_df[
        (provincias_df['Año'] == selected_ano) &
        (provincias_df['Trimestre'] == selected_trimestre)
    ]

    if not filtered_data.empty:
        st.subheader(f'Tecnología {selected_technology}')

        # Obtener las 10 provincias principales por tecnología
        top_provincias = filtered_data.groupby('Provincia')[selected_technology].sum().reset_index()
        top_provincias = top_provincias.sort_values(by=selected_technology, ascending=False).head(10)

        # Filtrar los datos para las 10 principales provincias
        top_filtered_data = filtered_data[filtered_data['Provincia'].isin(top_provincias['Provincia'])]

        # Gráfico de líneas
        st.write("Gráfico de Líneas")
        plt.figure(figsize=(5, 3))
        sns.lineplot(data=top_filtered_data, x='Trimestre', y=selected_technology, hue='Provincia')
        plt.title(f'Evolución de la Tecnología {selected_technology} en las 10 Principales Provincias')
        plt.xlabel('Trimestre')
        plt.ylabel(f'Número de accesos de {selected_technology}')
        st.pyplot(plt.gcf())
        plt.close()

        # Gráfico de barras
        st.write("Gráfico de Barras")
        plt.figure(figsize=(5, 3))
        sns.barplot(data=top_provincias, x='Provincia', y=selected_technology)
        plt.title(f'Accesos de Tecnología {selected_technology} en las 10 Principales Provincias')
        plt.xlabel('Provincia')
        plt.ylabel(f'Número de accesos de {selected_technology}')
        st.pyplot(plt.gcf())
        plt.close()

        # Gráfico en Mapa
        st.write("Mapa de Accesos por Tecnología")
        map = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)  # Coordenadas centradas en Argentina

        # Asegúrate de tener las coordenadas lat y lon en tu DataFrame
        if 'lat' in top_filtered_data.columns and 'lon' in top_filtered_data.columns:
            marker_cluster = MarkerCluster().add_to(map)
            for _, row in top_filtered_data.iterrows():
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=f"Provincia: {row['Provincia']}<br>{selected_technology}: {row[selected_technology]}",
                    icon=folium.Icon(color='blue')
                ).add_to(marker_cluster)
        else:
            st.write("El DataFrame no contiene columnas de latitud y longitud para mostrar en el mapa.")

        st.write(map._repr_html_(), unsafe_allow_html=True)
        
    else:
        st.write(f"No hay datos disponibles para la tecnología {selected_technology}.")
