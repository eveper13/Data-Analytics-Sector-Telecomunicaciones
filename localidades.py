import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def localidades_dashboard(localidades_df):



    # Filtros para Localidades
    selected_provincia = st.sidebar.selectbox('Seleccionar Provincia', localidades_df['Provincia'].unique())
    localidades = localidades_df[localidades_df['Provincia'] == selected_provincia]['Localidad'].unique()
    selected_localidad = st.sidebar.selectbox('Seleccionar Localidad', ['Todos'] + list(localidades))

    # Filtrar los datos por las selecciones
    filtered_data = localidades_df[
        (localidades_df['Provincia'] == selected_provincia) &
        ((localidades_df['Localidad'] == selected_localidad) | (selected_localidad == 'Todos'))
    ]

    # Mostrar gráficos
    if not filtered_data.empty:
        st.subheader('Distribución de Accesos por Provincia y Localidad')
        tech_columns = ['ADSL', 'CABLEMODEM', 'DIAL UP', 'FIBRA OPTICA', 'OTROS', 'SATELITAL', 'WIMAX', 'WIRELESS']
        
        # Preparar los datos para el gráfico de barras agrupadas
        if selected_localidad == 'Todos':
            grouped_data = filtered_data.groupby(['Provincia', 'Localidad'])[tech_columns].sum().reset_index()
        else:
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

        st.subheader('Pie de Proporción de Accesos por Tecnología en la Provincia Seleccionada')
        # Total de accesos por tecnología en la provincia seleccionada
        province_tech_totals = filtered_data[tech_columns].sum()
        province_tech_totals = province_tech_totals.reset_index()
        province_tech_totals.columns = ['Tecnología', 'Total Accesos']

        plt.figure(figsize=(10, 6))
        plt.pie(province_tech_totals['Total Accesos'], labels=province_tech_totals['Tecnología'], autopct='%1.1f%%', startangle=140)
        plt.title('Proporción de Accesos por Tecnología en la Provincia')
        st.pyplot(plt.gcf())
        plt.close()

    else:
        st.write("No hay datos disponibles para las selecciones realizadas.")
