import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def localidades_dashboard(localidades_df):
    # Filtros para Localidades
    selected_provincia = st.sidebar.selectbox('Seleccionar Provincia', localidades_df['Provincia'].unique())
    localidades = localidades_df[localidades_df['Provincia'] == selected_provincia]['Localidad'].unique()
    selected_localidad = st.sidebar.selectbox('Seleccionar Localidad', localidades)

    # Filtrar los datos por las selecciones
    filtered_data = localidades_df[
        (localidades_df['Provincia'] == selected_provincia) &
        (localidades_df['Localidad'] == selected_localidad)
    ]

    # Mostrar gráficos
    if not filtered_data.empty:
        st.subheader('Distribución de Accesos por Localidad')
        tech_columns = ['ADSL', 'CABLEMODEM', 'DIAL UP', 'FIBRA OPTICA', 'OTROS', 'SATELITAL', 'WIMAX', 'WIRELESS']
        
        # Preparar los datos para el gráfico de barras agrupadas
        grouped_data = filtered_data.groupby('Localidad')[tech_columns].sum().reset_index()

        # Verificar el DataFrame agrupado
        st.write(grouped_data)

        # Transformar los datos para barras agrupadas
        grouped_data_melted = grouped_data.melt(id_vars=['Localidad'], value_vars=tech_columns, 
                                                var_name='Tecnología', value_name='Accesos')

        plt.figure(figsize=(12, 6))
        sns.barplot(data=grouped_data_melted, x='Localidad', y='Accesos', hue='Tecnología', ci=None)
        plt.title('Distribución de Accesos por Tecnología')
        plt.xlabel('Localidad')
        plt.ylabel('Número de accesos')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
        plt.close()

        st.subheader('Comparación por Tipo de Tecnología')
        # Comparar el total de accesos para cada tipo de tecnología
        tech_totals = filtered_data[tech_columns].sum().reset_index()
        tech_totals.columns = ['Tecnología', 'Total Accesos']

        plt.figure(figsize=(10, 6))
        sns.barplot(data=tech_totals, y='Tecnología', x='Total Accesos', orient='h')
        plt.title('Comparación Total de Accesos por Tecnología')
        plt.xlabel('Número de accesos')
        plt.ylabel('Tecnología')
        st.pyplot(plt.gcf())
        plt.close()

        st.subheader('Proporción de Accesos por Tecnología en la Localidad Seleccionada')
        # Total de accesos por tecnología en la localidad seleccionada
        locality_tech_totals = filtered_data[tech_columns].sum()
        locality_tech_totals = locality_tech_totals.reset_index()
        locality_tech_totals.columns = ['Tecnología', 'Total Accesos']

        plt.figure(figsize=(8, 8))  # Ajustar el tamaño del gráfico de torta
        plt.pie(locality_tech_totals['Total Accesos'], labels=locality_tech_totals['Tecnología'], autopct='%1.1f%%', startangle=140)
        plt.title('Proporción de Accesos por Tecnología en la Localidad')
        st.pyplot(plt.gcf())
        plt.close()

    else:
        st.write("No hay datos disponibles para la localidad seleccionada.")
