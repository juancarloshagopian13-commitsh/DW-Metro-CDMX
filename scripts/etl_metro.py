import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# 1. Configuración de conexión a MySQL
USER = 'root'
PASSWORD = 'root'  # Tu contraseña de MySQL
HOST = 'localhost'
PORT = '3306'
DATABASE = 'dw_metro_cdmx'

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

print("=== INICIANDO PROCESO ETL METRO CDMX ===")

# --- 2. CARGA DE DIMENSIONES BASE ---

# DIM_ALCALDIA
df_alcaldia = pd.DataFrame([
    {'id_alcaldia': 1, 'alcaldia': 'Cuauhtémoc', 'municipio': 'CDMX'},
    {'id_alcaldia': 2, 'alcaldia': 'Iztapalapa', 'municipio': 'CDMX'},
    {'id_alcaldia': 3, 'alcaldia': 'Gustavo A. Madero', 'municipio': 'CDMX'},
    {'id_alcaldia': 4, 'alcaldia': 'Venustiano Carranza', 'municipio': 'CDMX'}
])
df_alcaldia.to_sql('DIM_ALCALDIA', con=engine, if_exists='append', index=False)
print("✔ DIM_ALCALDIA poblada.")

# DIM_LINEA
df_linea = pd.DataFrame([
    {'id_linea': 1, 'nombre_linea': 'Línea 1', 'color': 'Rosa'},
    {'id_linea': 2, 'nombre_linea': 'Línea 2', 'color': 'Azul'},
    {'id_linea': 3, 'nombre_linea': 'Línea 3', 'color': 'Verde Olivo'},
    {'id_linea': 9, 'nombre_linea': 'Línea 9', 'color': 'Café'}
])
df_linea.to_sql('DIM_LINEA', con=engine, if_exists='append', index=False)
print("✔ DIM_LINEA poblada.")

# DIM_ESTACION
df_estacion = pd.DataFrame([
    {'id_estacion': 1, 'nombre_estacion': 'Pantitlán', 'id_linea': 1},
    {'id_estacion': 2, 'nombre_estacion': 'Pino Suárez', 'id_linea': 1},
    {'id_estacion': 3, 'nombre_estacion': 'Zócalo/Tenochtitlan', 'id_linea': 2},
    {'id_estacion': 4, 'nombre_estacion': 'Hidalgo', 'id_linea': 3},
    {'id_estacion': 5, 'nombre_estacion': 'Indios Verdes', 'id_linea': 3}
])
df_estacion.to_sql('DIM_ESTACION', con=engine, if_exists='append', index=False)
print("✔ DIM_ESTACION poblada.")

# CAT_MODELO_TREN
df_modelo = pd.DataFrame([
    {'id_modelo': 1, 'modelo_tren': 'NM-02', 'capacidad_pasajeros': 1500, 'num_wagones': 9, 'velocidad_diseno_kmh': 80.0},
    {'id_modelo': 2, 'modelo_tren': 'NM-16', 'capacidad_pasajeros': 1500, 'num_wagones': 9, 'velocidad_diseno_kmh': 80.0},
    {'id_modelo': 3, 'modelo_tren': 'FE-07', 'capacidad_pasajeros': 1400, 'num_wagones': 7, 'velocidad_diseno_kmh': 75.0}
])
df_modelo.to_sql('CAT_MODELO_TREN', con=engine, if_exists='append', index=False)
print("✔ CAT_MODELO_TREN poblada.")

# DIM_TREN
df_tren = pd.DataFrame([
    {'id_tren': 101, 'id_modelo': 1},
    {'id_tren': 102, 'id_modelo': 2},
    {'id_tren': 103, 'id_modelo': 3}
])
df_tren.to_sql('DIM_TREN', con=engine, if_exists='append', index=False)
print("✔ DIM_TREN poblada.")

# DIM_CLIMA
df_clima = pd.DataFrame([
    {'id_clima': 1, 'clima_estado': 'Despejado', 'aplica_marcha_seguridad': 0},
    {'id_clima': 2, 'clima_estado': 'Lluvia Moderada', 'aplica_marcha_seguridad': 1},
    {'id_clima': 3, 'clima_estado': 'Lluvia Intensa', 'aplica_marcha_seguridad': 1}
])
df_clima.to_sql('DIM_CLIMA', con=engine, if_exists='append', index=False)
print("✔ DIM_CLIMA poblada.")

# DIM_INCIDENCIA
df_incidencia = pd.DataFrame([
    {'id_incidencia': 1, 'tipo_incidencia': 'Sin Incidencia', 'descripcion': 'Operación normal', 'gravedad': 'Ninguna'},
    {'id_incidencia': 2, 'tipo_incidencia': 'Falla Puertas', 'descripcion': 'Obstrucción mecánica en cierre de puertas', 'gravedad': 'Media'},
    {'id_incidencia': 3, 'tipo_incidencia': 'Falla Señalización', 'descripcion': 'Pérdida de código de velocidad', 'gravedad': 'Alta'}
])
df_incidencia.to_sql('DIM_INCIDENCIA', con=engine, if_exists='append', index=False)
print("✔ DIM_INCIDENCIA poblada.")

# --- 3. DIMENSIÓN TIEMPO (DIM_AÑO, DIM_MES, DIM_FECHA) ---

df_anio = pd.DataFrame([{'anio': 2026, 'tipo_periodo': 'Regular'}])
df_anio.to_sql('DIM_AÑO', con=engine, if_exists='append', index=False)

df_mes = pd.DataFrame([
    {'id_mes': 1, 'nombre_mes': 'Enero', 'trimestre': 1, 'anio': 2026},
    {'id_mes': 2, 'nombre_mes': 'Febrero', 'trimestre': 1, 'anio': 2026},
    {'id_mes': 3, 'nombre_mes': 'Marzo', 'trimestre': 1, 'anio': 2026}
])
df_mes.to_sql('DIM_MES', con=engine, if_exists='append', index=False)

fechas = []
start_date = datetime(2026, 1, 1)
for i in range(90):
    current_date = start_date + timedelta(days=i)
    fechas.append({
        'id_fecha': int(current_date.strftime('%Y%m%d')),
        'fecha': current_date.strftime('%Y-%m-%d'),
        'dia_semana': current_date.strftime('%A'),
        'es_festivo': 1 if current_date.day == 1 and current_date.month == 1 else 0,
        'id_mes': current_date.month
    })
df_fecha = pd.DataFrame(fechas)
df_fecha.to_sql('DIM_FECHA', con=engine, if_exists='append', index=False)
print("✔ DIM_FECHA, DIM_MES y DIM_AÑO pobladas.")

# --- 4. CARGA MASIVA A FACT_OPERACION ---

np.random.seed(42)
num_records = 1000

fact_records = []
date_ids = df_fecha['id_fecha'].tolist()
station_ids = df_estacion['id_estacion'].tolist()
tren_ids = df_tren['id_tren'].tolist()
clima_ids = df_clima['id_clima'].tolist()
incidencia_ids = df_incidencia['id_incidencia'].tolist()

for _ in range(num_records):
    afluencia = int(np.random.randint(5000, 45000))
    afluencia_pico = int(afluencia * np.random.uniform(0.35, 0.50))
    
    fact_records.append({
        'id_fecha': np.random.choice(date_ids),
        'id_estacion': np.random.choice(station_ids),
        'id_tren': np.random.choice(tren_ids),
        'id_clima': np.random.choice(clima_ids),
        'id_incidencia': np.random.choice(incidencia_ids),
        'afluencia_pasajeros': afluencia,
        'afluencia_hora_pico': afluencia_pico,
        'porcentaje_ocupacion': round(float(np.random.uniform(60.0, 98.0)), 2),
        'velocidad_operativa_real_kmh': round(float(np.random.uniform(35.0, 75.0)), 2),
        'intervalo_headway_seg': int(np.random.randint(120, 360)),
        'distancia_intertren_m': round(float(np.random.uniform(400.0, 1200.0)), 2),
        'tiempo_retraso_min': int(np.random.randint(0, 18)),
        'alerta_dosificacion': int(np.random.choice([0, 1], p=[0.7, 0.3]))
    })

df_fact = pd.DataFrame(fact_records)
df_fact.to_sql('FACT_OPERACION', con=engine, if_exists='append', index=False)
print(f"✔ FACT_OPERACION poblada exitosamente con {num_records} registros operacionales.")
print("=== PROCESO ETL FINALIZADO CON ÉXITO ===")