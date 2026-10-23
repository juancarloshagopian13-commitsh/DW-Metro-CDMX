# Arquitectura del Data Warehouse y Modelo Dimensional

## Flujo de Datos (Pipeline ETL)
1. **Extracción:** Lectura de archivos fuente de afluencia del Metro CDMX.
2. **Transformación y Limpieza:**
   * Normalización de nombres de estaciones y líneas (codificación UTF-8).
   * Eliminación de registros duplicados y manejo de valores nulos.
   * Generación de variables simuladas con semilla controlada (clima, retrasos, incidencias).
3. **Carga (Load):** Generación automatizada de archivos CSV dimensionales en `data/`.

---

## Esquema Dimensional (Copo de Nieve / Estrella)

### Tabla de Hechos
* **`FACT_OPERACION`**: Contiene las métricas numéricas de afluencia total, tiempos de retraso (min) y bandera de simulación.

### Tablas de Dimensiones
* **`DIM_LINEA`**: Catálogo de líneas del Metro.
* **`DIM_ESTACION`**: Estaciones de la red.
* **`DIM_ALCALDIA`**: Ubicación geográfica de la estación.
* **`DIM_FECHA`**, **`DIM_MES`**, **`DIM_AÑO`**: Jerarquía temporal para análisis histórico.
* **`DIM_INCIDENCIA`**: Clasificación de fallas y retrasos técnicos y operativos.
* **`DIM_CLIMA`**: Condición meteorológica asociada a la fecha.
* **`CAT_MODELO_TREN`**: Modelos de trenes operativos por línea.