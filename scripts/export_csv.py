import pandas as pd
from sqlalchemy import create_engine, inspect

USER = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'dw_metro_cdmx'

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"Tablas encontradas en la base de datos: {tables}")

for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM `{table}`", con=engine)
    file_name = f"{table.upper()}.csv"
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"✔ Exportada {file_name}")

print("=== EXPORTACIÓN A CSV COMPLETADA EXITOSAMENTE ===")