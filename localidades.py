import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def localidades_dashboard(localidades_df):
    st.title('Dashboard de Localidades')

    # Filtros para Localidades
    selected_provincia = st.sidebar.selectbox('Seleccionar Provincia', localidades_df['Provincia'].unique())
    partidos = localidades_df[localidades_df['Provincia'] == selected_provincia]['Partido'].unique()
    selected_partido = st.sidebar.selectbox('Seleccionar Partido', ['Todos'] + list(partidos))

    if selected_partido == 'Todos':
        localidades = localidades_df[localidades_df['Provincia'] == selected_provincia]['Localidad'].unique()
    else:
        localidades = localidades_df[(localidades_df['Provincia'] == selected_provincia) & 
                                    (localidades_df['Partido'] == selected_partido)]['Localidad'].unique()
    
    selected_localidad = st.sidebar.selectbox('Seleccionar Localidad', ['Todos'] + list(localidades))

    # Filtrar los datos por las selecciones
    filtered_data = localidades_df[
        (localidades_df['Provincia'] == selected_provincia) &
        ((localidades_df['Partido'] == selected_partido) | (selected_partido == 'Todos')) &
        ((localidades_df['Localidad'] == selected_localidad) | (selected_localidad == 'Todos'))
    ]

    # Mostrar gráficos
    if not filtered_data.empty:
        st.subheader('Tecnología Más Usada por Localidad')
        tech_columns = ['ADSL', 'CABLEMODEM', 'DIAL UP', 'FIBRA OPTICA', 'OTROS', 'SATELITAL', 'WIMAX', 'WIRELESS']
        tech_usage = filtered_data[tech_columns].sum()
        most_used_tech = tech_usage.idxmax()  # Tecnología más utilizada

        if most_used_tech:
            plt.figure(figsize=(10, 5))
            tech_data = filtered_data.groupby('Localidad')[most_used_tech].sum().reset_index()
            sns.lineplot(data=tech_data, x='Localidad', y=most_used_tech)
            plt.title(f'Evolución de la Tecnología {most_used_tech}')
            plt.xlabel('Localidad')
            plt.ylabel('Número de accesos')
            st.pyplot(plt.gcf())
        else:
            st.write("No hay datos disponibles para las tecnologías seleccionadas.")

        st.subheader('Top 5 Localidades con Mayor Uso de Tecnología')
        selected_technology = st.sidebar.selectbox('Seleccionar Tecnología para Top 5', tech_columns)
        if selected_technology:
            top_5_data = filtered_data[['Localidad', selected_technology]].groupby('Localidad').sum().reset_index()
            top_5_data = top_5_data.sort_values(by=selected_technology, ascending=False).head(5)

            if not top_5_data.empty:
                plt.figure(figsize=(10, 5))
                sns.barplot(data=top_5_data, x='Localidad', y=selected_technology)
                plt.title(f'Top 5 Localidades con Mayor Uso de {selected_technology}')
                plt.xlabel('Localidad')
                plt.ylabel('Número de accesos')
                st.pyplot(plt.gcf())
            else:
                st.write("No hay datos disponibles para la tecnología seleccionada.")
    else:
        st.write("No hay datos disponibles para las selecciones realizadas.")
