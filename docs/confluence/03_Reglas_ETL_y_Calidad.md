# Reglas de Limpieza de Datos y Calidad

## Reglas de Transformación Aplicadas
| ID | Regla | Descripción |
|---|---|---|
| **R01** | Corrección de Encoding | Repara caracteres e inconsistencias por doble codificación en nombres de estaciones. |
| **R02** | Estandarización de Texto | Normaliza espacios adicionales y convierte texto a formato estándar. |
| **R03** | Formato de Fechas | Convierte fechas a estándar ISO `YYYY-MM-DD` y genera la llave numérica `id_fecha` en formato `YYYYMMDD`. |
| **R04** | Normalización de Líneas | Mapea cadenas variantes (`Línea 1`, `L1`, `Linea A`) a un código único estandarizado. |
| **R05** | Desduplicación | Elimina registros exactamente idénticos en la combinación de Fecha, Estación y Línea. |
| **R06** | Datos Simulados | Asigna llave base a métricas no públicas a menos que se ejecute la bandera `--simulate`. |