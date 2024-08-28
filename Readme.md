# Análisis Completo del Sector de Telecomunicaciones

## Introducción

Este repositorio contiene un análisis exhaustivo del comportamiento del sector de telecomunicaciones en el ámbito nacional. La empresa prestadora de servicios de telecomunicaciones ha encargado este proyecto para obtener una visión clara sobre el acceso a internet y otros servicios de comunicación. El objetivo es identificar oportunidades de crecimiento, mejorar la calidad de los servicios y ofrecer soluciones personalizadas a los clientes.

## Contenido del Repositorio

El repositorio está organizado de la siguiente manera:

- **`main.py`**: Archivo principal que contiene el código para la aplicación Streamlit. Aquí se definen las secciones del dashboard y los análisis de KPIs.
- **`utils.py`**: Archivo que contiene funciones auxiliares, como `load_data`, que carga los datasets necesarios para el análisis.
- **`kpis.py`**: Contiene las funciones `kpi_1` y `kpi2` que calculan los indicadores clave de rendimiento (KPIs) para la evaluación de los datos.
- **`provincias.py`**: Define la función `provincias_dashboard`, que genera el dashboard para analizar los datos a nivel provincial.
- **`localidades.py`**: Define la función `localidades_dashboard`, que crea el dashboard para el análisis a nivel de localidades.
- **`img/`**: Carpeta que contiene imágenes usadas en el dashboard, como el fondo y el logo.
- **`Dataset_procesados/`**: Carpeta que contiene los datasets procesados utilizados en los análisis.

## Análisis de Dashboards

### Dashboard Global

El Dashboard Global proporciona una visión integral de los datos de telecomunicaciones a nivel nacional. Incluye los siguientes componentes:

- **Top 10 Provincias por Tecnología**: Gráfico de barras que muestra las diez provincias con el mejor acceso a diferentes tecnologías de internet.
- **Provincias con Menor Promedio de Acceso**: Gráfico de barras que identifica las provincias con el menor acceso promedio a las tecnologías seleccionadas.
- **Ingresos por Año y Trimestre**: Gráfico de líneas que detalla los ingresos generados a lo largo del tiempo.
- **Velocidad Media por Provincia (Top 10)**: Gráfico de barras que muestra la velocidad media de acceso a internet en las diez provincias principales.
- **Distribución de Velocidad Media por Provincia (Top 6)**: Gráfico de torta que representa la distribución de la velocidad media en las seis provincias principales.

**Predomina**: La visualización que predomina en el Dashboard Global es el gráfico de barras de **"Top 10 Provincias por Tecnología"**, ya que proporciona una visión clara y comparativa del acceso a internet en diferentes provincias.

### Dashboard de Provincias

El Dashboard de Provincias ofrece un análisis detallado de los datos a nivel provincial. Incluye gráficos y KPIs específicos para evaluar el comportamiento en cada provincia.

### Dashboard de Localidades

El Dashboard de Localidades proporciona un análisis a nivel de localidades, permitiendo una evaluación detallada del acceso a internet y otras métricas en áreas más específicas.

## Análisis de KPIs

### KPI 1: Crecimiento de Accesos

**Descripción**: Mide el incremento en el acceso al servicio de internet por provincia. Este KPI es crucial para identificar áreas con mayor potencial de crecimiento.

**Visualización**: La métrica se presenta en el Dashboard Global para proporcionar una visión rápida del crecimiento.

### KPI 2: Crecimiento de Velocidades Promedio

**Descripción**: Representa el aumento promedio en las velocidades de acceso a internet a nivel provincial. Este KPI ayuda a evaluar el rendimiento de las conexiones a internet en diferentes provincias.

**Visualización**: También se presenta en el Dashboard Global, permitiendo una evaluación rápida del crecimiento en velocidades.

## Conclusiones y Recomendaciones

El análisis realizado muestra un panorama claro sobre el acceso a internet y otros servicios de telecomunicaciones en el país. Las visualizaciones destacan áreas clave para la mejora y oportunidades de crecimiento:

- **Áreas de Mejora**: Provincias con menor acceso a tecnologías de internet y velocidades promedio bajas.
- **Oportunidades de Crecimiento**: Provincias con un buen crecimiento en el acceso y velocidades, que podrían ser objetivo de estrategias de expansión.

Se recomienda a la empresa utilizar estos insights para ajustar sus estrategias de servicio y orientación a los clientes.

Realizado por: Evelyn Perez- Analista de Datos 