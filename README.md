# NASA-API-to-CSV
# Recopilador de Datos NEO de NASA

Este script de Python permite recopilar y analizar datos sobre Objetos Cercanos a la Tierra (Near Earth Objects - NEO) utilizando la API pública de NASA. El programa descarga, procesa y almacena información detallada sobre asteroides, incluyendo sus características orbitales y físicas.

## Características

- Descarga automática de datos de la API de NASA
- Manejo de paginación automático
- Sistema de reintentos con retroceso exponencial
- Procesamiento y limpieza de datos
- Generación de informes estadísticos
- Registro detallado de operaciones
- Almacenamiento en formato CSV
- Soporte para múltiples idiomas (español/inglés)

## Requisitos Previos

- Python 3.7 o superior
- Conexión a Internet
- Clave de API de NASA (opcional, se puede usar DEMO_KEY)

## Instalación

1. Clone este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd nasa-neo-data
```

2. Instale las dependencias requeridas:
```bash
pip install -r requirements.txt
```

O instale las dependencias manualmente:
```bash
pip install pandas requests
```

## Configuración

1. (Opcional) Obtenga una clave de API de NASA:
   - Visite [NASA API Portal](https://api.nasa.gov)
   - Regístrese para obtener una clave gratuita
   - Reemplace `"DEMO_KEY"` en el script con su clave

2. (Opcional) Ajuste los parámetros de configuración:
   - `limite_peticiones`: Tiempo entre peticiones a la API
   - `directorio_salida`: Ubicación de los archivos de salida
   - `max_intentos`: Número máximo de reintentos por petición

## Uso

1. Ejecute el script:
```bash
python recopilador_nasa_neo.py
```

2. El script creará automáticamente:
   - Directorio `registros/` con logs de ejecución
   - Directorio `datos/` con:
     - Archivo CSV con datos completos
     - Informe de resumen en formato TXT

## Estructura de Datos

El script recopila los siguientes datos para cada asteroide:

| Columna | Descripción |
|---------|-------------|
| id_asteroide | Identificador único del asteroide |
| nombre | Nombre o designación del asteroide |
| magnitud_absoluta | Magnitud absoluta (H) |
| diametro_min_km | Diámetro mínimo estimado en kilómetros |
| diametro_max_km | Diámetro máximo estimado en kilómetros |
| es_peligroso | Indicador de si es potencialmente peligroso |
| id_orbita | Identificador de la órbita |
| semi_eje_mayor | Semi-eje mayor de la órbita |
| excentricidad | Excentricidad de la órbita |
| diametro_promedio_km | Promedio calculado del diámetro |

## Gestión de Errores

El script incluye:
- Reintentos automáticos para fallos de API
- Registro detallado de errores
- Validación de datos
- Manejo de excepciones

## Limitaciones

- La API de NASA tiene límites de velocidad (rate limits):
  - Para DEMO_KEY: 30 peticiones por hora
  - Para clave registrada: 1000 peticiones por hora
- Los datos se actualizan diariamente en la API de NASA

## Solución de Problemas

1. Error "API rate limit exceeded":
   - Espere una hora para que se restablezca el límite
   - Obtenga una clave de API propia
   
2. Error de conexión:
   - Verifique su conexión a Internet
   - El script reintentará automáticamente

## Desarrollo Futuro

Áreas planificadas para mejoras:
- Soporte para filtrado de datos
- Visualizaciones automáticas
- Exportación a otros formatos
- Análisis estadístico avanzado

## Contribución

Las contribuciones son bienvenidas:
1. Fork del repositorio
2. Cree una rama para su característica
3. Envíe un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o sugerencias, por favor abra un issue en el repositorio.