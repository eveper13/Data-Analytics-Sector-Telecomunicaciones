# kpis.py
import plotly.express as px
import pandas as pd
import streamlit as st


def kpi_1(df):
    # Verificar que la columna 'Accesos por cada 100 hogares' está presente
    if 'Accesos por cada 100 hogares' not in df.columns:
        st.error("La columna 'Accesos por cada 100 hogares' no está en el DataFrame.")
        return

    # Verificar que las columnas 'Año' y 'Trimestre' están presentes
    required_columns = ['Año', 'Trimestre', 'Provincia', 'Accesos por cada 100 hogares']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Las siguientes columnas necesarias no están en el DataFrame: {', '.join(missing_columns)}")
        return

    # Calcular el KPI: Crecimiento de Accesos
    # Ordenar por 'Provincia', 'Año', 'Trimestre'
    df = df.sort_values(by=['Provincia', 'Año', 'Trimestre'])

    # Crear columnas para el acceso actual y el nuevo acceso
    df['Accesoactual'] = df.groupby(['Provincia'])['Accesos por cada 100 hogares'].shift(1)
    df['Nuevoacceso'] = df['Accesos por cada 100 hogares']
    
    # Evitar división por cero y calcular el KPI
    df['KPI'] = ((df['Nuevoacceso'] - df['Accesoactual']) / df['Accesoactual']) * 100
    df['KPI'] = df['KPI'].fillna(0)  # Reemplazar NaN con 0 si no hay datos previos

    # Calcular el KPI promedio
    avg_kpi = df['KPI'].mean()

    # Mostrar el KPI como una tarjeta
    st.metric("KPI Promedio de Crecimiento de Accesos (%)", f"{avg_kpi:.2f}%")

    # Agrupar por provincia y calcular KPI promedio por provincia
    df_grouped = df.groupby('Provincia')['KPI'].mean().reset_index()
    
    # Obtener las 10 provincias con mayor promedio de KPI
    top_provincias = df_grouped.sort_values(by='KPI', ascending=False).head(10)

    # Crear gráfico de línea del KPI de Crecimiento de Accesos para las 10 provincias principales
    fig_line = px.line(df[df['Provincia'].isin(top_provincias['Provincia'])], x='Trimestre', y='KPI', color='Provincia',
                       title='Evolución del KPI de Crecimiento de Accesos (Top 10 Provincias)',
                       labels={'KPI': 'Crecimiento (%)', 'Trimestre': 'Trimestre'})
    st.plotly_chart(fig_line)

    # Crear gráfico de barras del KPI promedio por provincia
    fig_bar = px.bar(df_grouped, x='Provincia', y='KPI',
                     title='Promedio del KPI de Crecimiento de Accesos por Provincia',
                     labels={'KPI': 'Crecimiento (%)'})
    st.plotly_chart(fig_bar)

    # Crear gráfico de dispersión del KPI por trimestre para las 10 provincias principales
    fig_scatter = px.scatter(top_provincias, x='Provincia', y='KPI',
                            title='Dispersión del KPI de Crecimiento de Accesos para las 10 Provincias Principales',
                            labels={'KPI': 'Crecimiento (%)', 'Provincia': 'Provincia'})
    st.plotly_chart(fig_scatter)



def kpi2(df):
    velocidad_columns = ['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', '+ 1 Mbps - 6 Mbps', 
                         '+ 6 Mbps - 10 Mbps', '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', 
                         '+ 30 Mbps', 'OTROS']

    missing_columns = [col for col in velocidad_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Las siguientes columnas de velocidad no están en el DataFrame: {', '.join(missing_columns)}")
        return

    df['Promedio_Velocidad'] = df[velocidad_columns].mean(axis=1)
    
    df_provincias = df.groupby('Provincia')['Promedio_Velocidad'].mean().reset_index()
    provincias_menor_acceso = df_provincias.nsmallest(10, 'Promedio_Velocidad')

    # Mover el KPI promedio de crecimiento de velocidades aquí
    df_filtrado = df[df['Provincia'].isin(provincias_menor_acceso['Provincia'])]

    df_grouped = df_filtrado.groupby(['Año', 'Trimestre', 'Provincia'])['Promedio_Velocidad'].mean().reset_index()
    df_grouped = df_grouped.sort_values(by=['Provincia', 'Año', 'Trimestre'])

    df_grouped['Crecimiento_Velocidad'] = df_grouped.groupby('Provincia')['Promedio_Velocidad'].pct_change() * 100
    df_grouped['Crecimiento_Velocidad'] = df_grouped['Crecimiento_Velocidad'].fillna(0)

    avg_growth_velocity = df_grouped['Crecimiento_Velocidad'].mean()
    st.metric("KPI Promedio de Crecimiento de Velocidades (%)", f"{avg_growth_velocity:.2f}%")

    # Mostrar la tabla después del KPI
    st.write("Provincias con menor acceso:")
    st.dataframe(provincias_menor_acceso)

    # Crear gráficos después de la tarjeta KPI
    fig_growth = px.line(df_grouped, x='Trimestre', y='Crecimiento_Velocidad', color='Provincia',
                        title='Evolución del Crecimiento de Velocidades Promedio en Provincias con Menor Acceso',
                        labels={'Crecimiento_Velocidad': 'Crecimiento (%)', 'Trimestre': 'Trimestre'})
    st.plotly_chart(fig_growth)

    fig_avg_velocidad = px.bar(df_grouped, x='Provincia', y='Promedio_Velocidad',
                              title='Promedio de Velocidades por Provincia con Menor Acceso',
                              labels={'Promedio_Velocidad': 'Promedio de Velocidades (Mbps)'})
    st.plotly_chart(fig_avg_velocidad)