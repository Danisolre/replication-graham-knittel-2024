import requests
import os

def load_county_geojson():
    # URL del recurso GeoJSON (Dataset oficial de condados EE.UU.)
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    
    # Definición de la ruta de almacenamiento local
    output_path = "datos/raw/geojson-counties-fips.json"
    
    # Validación y creación del directorio de destino
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Ejecución de la petición HTTP para la adquisición de datos
        print(f"Descargando recurso desde: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Persistencia del archivo en el sistema de archivos local
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Proceso finalizado. Archivo guardado en: {output_path}")
        
    except Exception as e:
        print(f"Error en la fase de adquisición de datos: {e}")

if __name__ == "__main__":
    load_county_geojson()
