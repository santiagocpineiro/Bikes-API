import pandas as pd
from pymongo import MongoClient
import json
from datetime import datetime

# Carga las credenciales de la conexión desde un archivo
try:
    with open("db_config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'db_config.json'.")
    exit()
except json.JSONDecodeError as e:
    print(f"Error al decodificar el archivo 'db_config.json': {e}")
    exit()

# Conexión a MongoDB
try:
    client = MongoClient(config["MONGO_URI"], tls=True, tlsAllowInvalidCertificates=True)
    db = client[config["DATABASE_NAME"]]
    collection = db[config["COLLECTION_NAME"]]
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Leer los datos desde MongoDB
try:
    documents = list(collection.find({}, {
        "_id": 0,  # Excluye el campo _id
        "network.stations.id": 1,
        "network.stations.name": 1,
        "network.stations.timestamp": 1,
        "network.stations.free_bikes": 1,
        "network.stations.empty_slots": 1,
        "network.stations.extra.uid": 1,
        "network.stations.extra.last_updated": 1,
        "network.stations.extra.slots": 1,
        "network.stations.extra.normal_bikes": 1,
        "network.stations.extra.ebikes": 1
    }))
    print(f"Se recuperaron {len(documents)} documentos.")
except Exception as e:
    print(f"Error al leer los datos de MongoDB: {e}")
    exit()

# Procesar los datos
try:
    stations_data = []
    for doc in documents:
        for station in doc.get("network", {}).get("stations", []):
            stations_data.append({
                "id": station.get("id"),
                "name": station.get("name"),
                "timestamp": station.get("timestamp"),
                "free_bikes": station.get("free_bikes"),
                "empty_slots": station.get("empty_slots"),
                "uid": station.get("extra", {}).get("uid"),
                "last_updated": station.get("extra", {}).get("last_updated"),
                "slots": station.get("extra", {}).get("slots"),
                "normal_bikes": station.get("extra", {}).get("normal_bikes"),
                "ebikes": station.get("extra", {}).get("ebikes"),
            })
    print("Datos procesados correctamente.")
except Exception as e:
    print(f"Error al procesar los datos: {e}")
    exit()

# Crear un DataFrame de pandas
try:
    df = pd.DataFrame(stations_data)
    print("DataFrame creado correctamente.")
except Exception as e:
    print(f"Error al crear el DataFrame: {e}")
    exit()

# Exportar a CSV
try:
    csv_filename = f"stations_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"Datos exportados a CSV: {csv_filename}")
except Exception as e:
    print(f"Error al exportar los datos a CSV: {e}")
    exit()

# Exportar a Parquet
try:
    parquet_filename = f"stations_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(parquet_filename, index=False)
    print(f"Datos exportados a Parquet: {parquet_filename}")
except Exception as e:
    print(f"Error al exportar los datos a Parquet: {e}")
    exit()

