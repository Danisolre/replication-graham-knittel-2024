# Replicación de la Figura 1A — Graham & Knittel (2024)

## Artículo seleccionado

Graham, K., & Knittel, C. R. (2024). *Assessing the distribution of employment vulnerability to the energy transition using employment carbon footprints.* Proceedings of the National Academy of Sciences, 121(7), e2314773121. [https://doi.org/10.1073/pnas.2314773121](https://doi.org/10.1073/pnas.2314773121)

## Integrantes del equipo

| Integrante | Rol | GitHub |
|---|---|---|
| Daniela Solano Restrepo | Gestión de datos | [@Danisolre](https://github.com/Danisolre) |
| Jonathan Melo | Código y visualización | [@jonathanmelosa](https://github.com/jonathanmelosa) |
| Natalia Suescún | Documentación y gestión | [@NataliaSFernandez](https://github.com/NataliaSFernandez) |
| Carlos Molina | Control de calidad y validación empírica | [@camolina2026](https://github.com/camolina2026) |

**Profesor:** Gustavo Castillo — [@guscastilloa](https://github.com/guscastilloa)

## Descripción del proyecto

Este proyecto busca replicar la **Figura 1A** del artículo de Graham y Knittel (2024), que presenta un mapa coroplético de la **huella de carbono laboral total (overall employment carbon footprint, ECF)** por condado en Estados Unidos.

El ECF es un indicador que mide la vulnerabilidad laboral ante la transición energética, integrando información de empleo, consumo energético y emisiones (Scopes 1, 2 y 3) a nivel sectorial y geográfico. La figura utiliza una escala logarítmica para visualizar la distribución espacial del indicador.

### Resultado a reproducir

**Conclusión seleccionada:** La vulnerabilidad laboral ante la transición energética, medida a través del ECF, se distribuye de forma heterogénea entre condados de EE.UU., con concentraciones elevadas en regiones con alta dependencia de industrias intensivas en carbono.

**Evidencia:** Mapa coroplético de la Figura 1A — *Overall employment carbon footprints, by county.*

## Estructura de directorios

```
replication-graham-knittel-2024/
│
├── data/
│   ├── raw/                            # Datos originales
│   │   ├── ECF_total.csv               # Indicador ECF por condado
│   │   └── geojson-counties-fips.json  # Geometría de condados (GeoJSON)
│   └── processed/                      # Datos procesados
│       └── counties_ecf_merged.geojson # ECF + geometría unidos
│
├── code/
│   ├── 01_load_data.py                 # Carga y validación de datos
│   ├── 02_explore_data.py              # Análisis exploratorio y estadísticas descriptivas
│   ├── 03_merge_geo.py                 # Unión ECF + geometría de condados
│   └── 04_plot_figure1A.py             # Generación del mapa coroplético (Figura 1A)
│
├── output/
│   └── figures/
│       └── fig1A_ecf_county.png        # Figura 1A replicada
│
├── docs/                               # Documentación y decisiones metodológicas
│
├── .gitignore
├── environment.yml               # Entorno reproducible (Conda)
├── requirements.txt              # Dependencias de Python (pip)
├── run_pipeline.sh               # Script de ejecución end-to-end del pipeline
└── README.md                     # Este archivo
```

## Requisitos técnicos

### Software

- Python 3.10+
- Git

### Librerías de Python

Las dependencias se instalan con:

```bash
pip install -r requirements.txt
```

Librerías principales:

- `pandas` — manipulación de datos tabulares
- `geopandas` — manejo de datos geoespaciales
- `matplotlib` — visualización y generación de figuras
- `numpy` — operaciones numéricas (escala logarítmica)

### Datos

- **ECF_total.csv** — Indicador de huella de carbono laboral por condado. Disponible en el [repositorio de replicación](https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials).
- **geojson-counties-fips.json** — Geometría de condados de EE.UU. con códigos FIPS.

## Repositorio original de replicación

Los datos y código del artículo están disponibles en: [https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials](https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials)

## Instrucciones de ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Danisolre/replication-graham-knittel-2024.git
cd replication-graham-knittel-2024

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el pipeline de replicación
python code/01_load_data.py          # Carga y valida ECF_total.csv
python code/02_explore_data.py       # Análisis exploratorio y estadísticas descriptivas
python code/03_merge_geo.py          # Merge ECF + geometría de condados
python code/04_plot_figure1A.py      # Genera la Figura 1A replicada
```

La figura replicada se guardará en `output/figures/fig1A_ecf_county.png`.

## Decisiones metodológicas

| Decisión | Detalle |
|---|---|
| Proyección cartográfica | Albers Equal Area Conic (ESRI:102003), estándar para mapas de EE.UU. continental |
| Escala del mapa | Logarítmica (log10), consistente con el artículo original |
| Paleta de colores | YlOrRd (amarillo → rojo), secuencial para valores positivos |
| Formato geoespacial | GeoJSON de condados con códigos FIPS |
| Ámbito geográfico | EE.UU. continental (CONUS), incluyendo Alaska y Hawaii como insets reposicionados |
| Tratamiento Alaska/Hawaii | Para Alaska (02) y Hawaii (15), si la geometría es MultiPolygon, se conserva únicamente el polígono principal |
| Columna ECF utilizada | `eff_emiss_per_emp_avg` (emisiones efectivas por empleado, valor promedio) |
| Herramienta original | La figura del paper fue generada en Tableau; esta réplica usa Python (matplotlib + geopandas) |
