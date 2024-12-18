# Bikes-API

Este proyecto permite integrar datos de una API de bicicletas públicas en una base de datos MongoDB y exportar los datos almacenados en formatos CSV y Parquet para su análisis. Los scripts están organizados para simplificar su ejecución y manejo.

## Estructura del Proyecto

- `scripts/`
  - `script_1.py`: Este script conecta a la API de Citybik, obtiene los datos de las estaciones de bicicletas y los inserta en una base de datos MongoDB.
  - `script_2.py`: Este script recupera los datos de la base de datos MongoDB y los exporta en formato CSV y Parquet.
  - `db_config.example.json`: Archivo de ejemplo para configurar las credenciales de conexión a MongoDB. **El usuario debe crear su propio archivo de configuración `db_config.json` basado en este ejemplo.**

- `environment.yml`: Archivo que define el entorno Conda necesario para ejecutar los scripts. Contiene todas las dependencias requeridas.

## Requisitos Previos

1. **Python**:
   Asegúrate de tener instalado Python (3.9 o superior recomendado).
   
2. **MongoDB**:
   Un servidor MongoDB accesible (puede ser local o en la nube, como MongoDB Atlas).

3. **Conda**:
   Necesitarás Conda para crear el entorno de ejecución.

## Configuración del Entorno

1. **Crear el entorno Conda**:
   Ejecuta el siguiente comando en tu terminal para crear el entorno desde el archivo `environment.yml`:

   ```bash
   conda env create -f environment.yml

2. **Activar el entorno: Una vez creado el entorno, actívalo con:**:
   ```bash
   conda activate rag

## Configuración de Credenciales

  1. Crear el archivo db_config.json: Basándote en el archivo de ejemplo scripts/db_config.example.json, crea un archivo llamado db_config.json en el directorio scripts/. Este archivo debe contener tus credenciales de conexión a MongoDB.

    Ejemplo de archivo db_config.json:
    ```bash
    {
    "MONGO_URI": "mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/<nombre_base_de_datos>?tls=true&tlsAllowInvalidHostnames=true",
    "DATABASE_NAME": "bikes",
    "COLLECTION_NAME": "biciscorunha"
    }

Nota: No subas este archivo al repositorio si contiene credenciales reales.

## Uso de los Scripts

   1. Ejecutar script_1.py: Este script se encarga de obtener los datos de la API de Citybik y almacenarlos en MongoDB. Ejecútalo desde el directorio scripts/:
    ```bash
    python scripts/script_1.py

    Este script realiza una solicitud a la API y guarda los datos en la colección especificada en el archivo db_config.json.

   2. Ejecutar script_2.py: Este script recupera los datos almacenados en MongoDB y los exporta en formatos CSV y Parquet. Ejecútalo desde el directorio scripts/:
   ```bash
    python scripts/script_2.py

    Los archivos generados serán nombrados dinámicamente en función de la fecha y hora de ejecución, por ejemplo:

    stations_data_YYYYMMDD_HHMMSS.csv
    stations_data_YYYYMMDD_HHMMSS.parquet
