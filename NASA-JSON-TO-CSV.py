import pandas as pd
import requests
import json
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import Optional, List, Dict, Any


class RecopiladorDatosNASANeo:
    """Clase para recopilar y procesar datos de Objetos Cercanos a la Tierra (NEO) de la API de NASA."""

    def __init__(self, clave_api: str = "DEMO_KEY", limite_peticiones: int = 1):
        """
        Inicializa el recopilador de datos NEO.

        Args:
            clave_api: Clave de la API de NASA (predeterminado: "DEMO_KEY")
            limite_peticiones: Tiempo de espera entre llamadas a la API en segundos (predeterminado: 1)
        """
        self.url_api = "https://api.nasa.gov/neo/rest/v1/neo/browse"
        self.clave_api = clave_api
        self.limite_peticiones = limite_peticiones

        # Configuración de registro
        self._configurar_registro()

    def _configurar_registro(self) -> None:
        """Configura el registro con marca de tiempo y nivel de registro."""
        directorio_logs = Path("registros")
        directorio_logs.mkdir(exist_ok=True)

        archivo_log = directorio_logs / f"nasa_neo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(archivo_log),
                logging.StreamHandler()
            ]
        )

    def obtener_datos(self, parametros: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos de la API de NASA con manejo de errores y lógica de reintentos.

        Args:
            parametros: Diccionario de parámetros de consulta

        Returns:
            Datos de respuesta de la API o None si la petición falla
        """
        max_intentos = 3
        for intento in range(max_intentos):
            try:
                respuesta = requests.get(self.url_api, params=parametros, timeout=10)
                respuesta.raise_for_status()
                return respuesta.json()
            except requests.exceptions.RequestException as e:
                logging.error(f"Intento {intento + 1}/{max_intentos} falló: {str(e)}")
                if intento < max_intentos - 1:
                    time.sleep(2 ** intento)  # Retroceso exponencial
                    continue
                return None

    def obtener_todos_datos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los datos paginados de NEO desde la API.

        Returns:
            Lista de diccionarios con datos NEO
        """
        todos_datos = []
        pagina = 0

        while True:
            parametros = {'api_key': self.clave_api, 'page': pagina}
            logging.info(f"Obteniendo página {pagina}...")

            datos = self.obtener_datos(parametros)
            if not datos or 'near_earth_objects' not in datos or not datos['near_earth_objects']:
                break

            todos_datos.extend(datos['near_earth_objects'])
            logging.info(f"Recuperados {len(datos['near_earth_objects'])} objetos de la página {pagina}")

            pagina += 1
            time.sleep(self.limite_peticiones)

        logging.info(f"Total de objetos recuperados: {len(todos_datos)}")
        return todos_datos

    def procesar_datos(self, datos: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Procesa y limpia los datos NEO.

        Args:
            datos: Lista de diccionarios con datos NEO

        Returns:
            DataFrame de pandas procesado
        """
        if not datos:
            raise ValueError("No hay datos para procesar")

        df = pd.json_normalize(datos)

        # Seleccionar y renombrar columnas
        mapeo_columnas = {
            "id": "id_asteroide",
            "name": "nombre",
            "absolute_magnitude_h": "magnitud_absoluta",
            "estimated_diameter.kilometers.estimated_diameter_min": "diametro_min_km",
            "estimated_diameter.kilometers.estimated_diameter_max": "diametro_max_km",
            "is_potentially_hazardous_asteroid": "es_peligroso",
            "orbital_data.orbit_id": "id_orbita",
            "orbital_data.semi_major_axis": "semi_eje_mayor",
            "orbital_data.eccentricity": "excentricidad"
        }

        df = df[mapeo_columnas.keys()].rename(columns=mapeo_columnas)

        # Convertir columnas numéricas
        columnas_numericas = ['magnitud_absoluta', 'diametro_min_km', 'diametro_max_km',
                              'semi_eje_mayor', 'excentricidad']
        for col in columnas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Agregar columnas derivadas
        df['diametro_promedio_km'] = (df['diametro_min_km'] + df['diametro_max_km']) / 2

        return df

    def guardar_datos(self, df: pd.DataFrame, directorio_salida: str = "datos") -> None:
        """
        Guarda los datos procesados en CSV y genera un informe resumen.

        Args:
            df: DataFrame procesado
            directorio_salida: Directorio para guardar archivos de salida
        """
        # Crear directorio de salida
        ruta_salida = Path(directorio_salida)
        ruta_salida.mkdir(exist_ok=True)

        # Guardar conjunto de datos principal
        marca_tiempo = datetime.now().strftime('%Y%m%d_%H%M%S')
        ruta_csv = ruta_salida / f"nasa_neo_datos_{marca_tiempo}.csv"
        df.to_csv(ruta_csv, index=False)
        logging.info(f"Datos guardados en {ruta_csv}")

        # Generar y guardar informe resumen
        ruta_informe = ruta_salida / f"nasa_neo_resumen_{marca_tiempo}.txt"
        with open(ruta_informe, 'w', encoding='utf-8') as f:
            f.write("Resumen de Datos NEO de NASA\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Total de objetos: {len(df)}\n")
            f.write(f"Objetos peligrosos: {df['es_peligroso'].sum()}\n\n")

            f.write("Resumen Estadístico:\n")
            f.write(df.describe().to_string())

        logging.info(f"Informe resumen guardado en {ruta_informe}")


def main():
    """Función principal de ejecución."""
    try:
        # Inicializar recopilador
        recopilador = RecopiladorDatosNASANeo()

        # Obtener datos
        datos_crudos = recopilador.obtener_todos_datos()

        if datos_crudos:
            # Procesar datos
            df = recopilador.procesar_datos(datos_crudos)

            # Guardar resultados
            recopilador.guardar_datos(df)

            # Mostrar estadísticas básicas
            print("\nResumen de Datos:")
            print("-" * 50)
            print(df.describe())
        else:
            logging.error("No se recuperaron datos de la API")

    except Exception as e:
        logging.error(f"Ocurrió un error: {str(e)}")
        raise


if __name__ == "__main__":
    main()