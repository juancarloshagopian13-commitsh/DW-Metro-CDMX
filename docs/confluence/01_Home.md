# Sistema Analítico Data Warehouse — Metro CDMX

**Instituto Politécnico Nacional (IPN)**  
**Unidad Profesional Interdisciplinaria de Ingeniería y Ciencias Sociales y Administrativas (UPIICSA)**  

**Materia:** Analítica de Datos  
**Secuencia:** 6CM62  
**Maestro:** Entzana Garduño Yventz  

**Integrantes del Equipo:**
* Pérez de León Hagopian Juan Carlos
* Lozada Celis Ernesto
* Gómez Vega Diego
* Bustillos Segindo Jazmin

**Repositorio:** `juancarloshagopian13-commitsh/DW-Metro-CDMX`  

---

## Objetivo General
Desarrollar e implementar un pipeline ETL en Python y un Data Warehouse con modelo dimensional (Copo de Nieve / Estrella) para almacenar, limpiar y analizar el histórico de afluencia e incidencias de la red del Metro de la Ciudad de México, permitiendo la toma de decisiones mediante tableros en **IBM Cognos Analytics**.

## Alcance del Proyecto
* **Fuentes de Datos:** Datos Abiertos de la CDMX (Afluencia histórica por línea y estación).
* **Procesamiento:** Script modular en Python (`scripts/etl_metro.py`).
* **Almacenamiento:** Modelo Dimensional en tablas CSV (`data/`) preparado para MySQL y Cognos.
* **Visualización:** Dashboard analítico interactivo con métricas de afluencia, líneas críticas y tiempos de retraso.
