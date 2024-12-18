from pymongo import MongoClient
import requests
import json
import time

# Carga las credenciales de la conexión desde un archivo
with open("db_config.json", "r") as file:
    config = json.load(file)

# Conexión a MongoDB
try:
    client = MongoClient(config["MONGO_URI"])
    db = client[config["DATABASE_NAME"]]
    collection = db[config["COLLECTION_NAME"]]
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# URL de la API de Citybik
url = "https://api.citybik.es/v2/networks/bicicorunha"

# Bucle para insertar datos cada minuto
while True:
    try:
        # Descarga de datos desde la API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Convierte la respuesta en un diccionario
        print("Datos obtenidos de la API exitosamente.")
        
        # Inserción de datos en MongoDB
        if "network" in data:
            # Agrega un timestamp para diferenciar las entradas
            data["network"]["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            collection.insert_one(data["network"])
            print(f"Datos insertados en la colección de MongoDB exitosamente a las {data['network']['timestamp']}.")
        else:
            print("No se encontró la clave 'network' en los datos obtenidos.")

    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error con la solicitud: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
    except Exception as e:
        print(f"Error al insertar los datos en MongoDB: {e}")
    
    # Espera un minuto antes de la siguiente iteración
    print("Esperando 1 minuto antes de la siguiente iteración...")
    time.sleep(60)
