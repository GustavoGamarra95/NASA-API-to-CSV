import pandas as pd
import requests
import json
import time

# Configuración básica de logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de pandas para mostrar todas las filas y columnas
pd.set_option("display.max_rows", None, "display.max_columns", None)

# URL de la API y clave de API (puedes cambiarla por tu propia clave)
API_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"
API_KEY = "DEMO_KEY"  # Usa tu propia clave si tienes una


# Función para obtener datos de la API
def fetch_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None


# Función para obtener todos los datos paginados
def fetch_all_data(base_url, params):
    all_data = []
    page = 0
    while True:
        params['page'] = page
        data = fetch_data(base_url, params)
        if not data or 'near_earth_objects' not in data or not data['near_earth_objects']:
            break
        all_data.extend(data['near_earth_objects'])
        page += 1
        time.sleep(1)  # Respeta el rate limiting de la API
    return all_data


# Función principal
def main():
    params = {
        'api_key': API_KEY,
        'page': 0
    }
    logging.info("Iniciando la extracción de datos...")
    all_data = fetch_all_data(API_URL, params)

    if all_data:
        # Normalizar los datos y crear un DataFrame
        df = pd.json_normalize(all_data)

        # Seleccionar las columnas deseadas
        columnas = [
            "id",
            "name",
            "absolute_magnitude_h",
            "estimated_diameter.kilometers.estimated_diameter_min",
            "estimated_diameter.kilometers.estimated_diameter_max",
            "is_potentially_hazardous_asteroid",
            "orbital_data.orbit_id",
            "orbital_data.semi_major_axis",
            "orbital_data.eccentricity"
        ]
        df = df[columnas]

        # Renombrar las columnas para mayor claridad
        df.rename(columns={
            "estimated_diameter.kilometers.estimated_diameter_min": "diametro_min_km",
            "estimated_diameter.kilometers.estimated_diameter_max": "diametro_max_km",
            "orbital_data.orbit_id": "id_orbita",
            "orbital_data.semi_major_axis": "semi_eje_mayor",
            "orbital_data.eccentricity": "excentricidad"
        }, inplace=True)

        # Mostrar un resumen de los datos
        logging.info("Resumen de los datos obtenidos:")
        print(df.describe(include='all'))

        # Exportar el DataFrame a un archivo CSV
        output_file = "NASA_API.csv"
        df.to_csv(output_file, index=False, header=True, encoding="utf-8")
        logging.info(f"Datos exportados exitosamente a {output_file}")
    else:
        logging.error("No se pudieron obtener datos para exportar.")


if __name__ == "__main__":
    main()