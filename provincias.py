import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def provincias_dashboard(provincias_df):
   

    # Filtrar columnas relevantes y eliminar columnas adicionales si es necesario
    columnas_relevantes = ['Provincia', 'Año', 'Trimestre', 'ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless', 'Otros']
    provincias_df = provincias_df[columnas_relevantes]
    
    # Filtrar filas con valores nulos o infinitos en columnas numéricas antes de la conversión
    provincias_df = provincias_df.replace([pd.NA, float('inf'), -float('inf')], pd.NA)
    provincias_df = provincias_df.dropna(subset=['Año'])

    # Convertir Año a int después de eliminar valores nulos e infinitos
    provincias_df['Año'] = provincias_df['Año'].astype(int)

    # Obtener el rango de años disponible
    min_year = provincias_df['Año'].min()
    max_year = provincias_df['Año'].max()

    # Filtros para Provincia, Rango de Año, Trimestre y Tecnologías
    selected_provincia = st.sidebar.selectbox('Seleccionar Provincia', provincias_df['Provincia'].unique())
    selected_years = st.sidebar.slider('Seleccionar Rango de Años', min_value=min_year, max_value=max_year, value=(min_year, max_year))
    selected_trimestre = st.sidebar.selectbox('Seleccionar Trimestre', provincias_df['Trimestre'].unique())
    
    tech_columns = ['ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless', 'Otros']
    selected_technologies = st.sidebar.multiselect('Seleccionar Tecnologías', tech_columns, default=tech_columns)

    # Filtrar los datos por las selecciones
    filtered_data = provincias_df[
        (provincias_df['Provincia'] == selected_provincia) &
        (provincias_df['Año'] >= selected_years[0]) &
        (provincias_df['Año'] <= selected_years[1]) &
        (provincias_df['Trimestre'] == selected_trimestre)
    ]

    if not filtered_data.empty:
        st.subheader(f'Tecnologías: {", ".join(selected_technologies)}')

        # 1. Gráfico de Tendencia Temporal
        st.write("Gráfico de Tendencia Temporal")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_data, x='Año', y='ADSL', label='ADSL', ci=None)
        sns.lineplot(data=filtered_data, x='Año', y='Cablemodem', label='Cablemodem', ci=None)
        sns.lineplot(data=filtered_data, x='Año', y='Fibra óptica', label='Fibra óptica', ci=None)
        sns.lineplot(data=filtered_data, x='Año', y='Wireless', label='Wireless', ci=None)
        sns.lineplot(data=filtered_data, x='Año', y='Otros', label='Otros', ci=None)
        plt.title('Evolución de Tipos de Acceso a lo Largo del Tiempo')
        plt.xlabel('Año')
        plt.ylabel('Número de Accesos')
        plt.legend()
        st.pyplot(plt.gcf())
        plt.close()

        # 2. Gráfico de Distribución por Provincia
        st.write("Gráfico de Distribución por Provincia")
        if selected_years[0] == selected_years[1]:  # Mostrar solo para un año específico
            year_data = filtered_data[filtered_data['Año'] == selected_years[0]]
            year_data = year_data.groupby('Provincia')[selected_technologies].sum().reset_index()
            year_data = year_data.set_index('Provincia')
            
            plt.figure(figsize=(10, 6))
            year_data.plot(kind='bar', stacked=True)
            plt.title(f'Distribución de Accesos por Provincia en {selected_years[0]}')
            plt.xlabel('Provincia')
            plt.ylabel('Número de Accesos')
            st.pyplot(plt.gcf())
            plt.close()
        else:
            st.write("Seleccione un solo año para ver la distribución por provincia.")

        # 3. Gráfico de Comparación de Tecnologías
        st.write("Gráfico de Comparación de Tecnologías")
        tech_comparison = filtered_data[selected_technologies].sum()
        tech_comparison_df = tech_comparison.reset_index()
        tech_comparison_df.columns = ['Tecnología', 'Total Accesos']

        plt.figure(figsize=(10, 6))
        sns.barplot(data=tech_comparison_df, x='Tecnología', y='Total Accesos')
        plt.title('Comparación de Accesos por Tecnología')
        plt.xlabel('Tecnología')
        plt.ylabel('Total de Accesos')
        st.pyplot(plt.gcf())
        plt.close()

        # Gráfico de Tortas
        st.write("Gráfico de Tortas")
        filtered_data_sum = filtered_data[selected_technologies].sum().reset_index()
        filtered_data_sum.columns = ['Tecnología', 'Total Accesos']

        if not filtered_data_sum.empty:
            fig_pie = px.pie(filtered_data_sum, names='Tecnología', values='Total Accesos',
                             title=f'Distribución de Accesos por Tecnología en {selected_provincia} ({selected_years[0]}-{selected_years[1]} - T{selected_trimestre})')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.write("No hay datos disponibles para las tecnologías seleccionadas.")

    else:
        st.write("No hay datos disponibles para las selecciones actuales.")
