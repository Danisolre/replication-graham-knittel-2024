# Replicación de la Figura 1A — Graham & Knittel (2024)

## Artículo seleccionado

Graham, K., & Knittel, C. R. (2024). *Assessing the distribution of employment vulnerability to the energy transition using employment carbon footprints.* Proceedings of the National Academy of Sciences, 121(7), e2314773121. [https://doi.org/10.1073/pnas.2314773121](https://doi.org/10.1073/pnas.2314773121)

## Integrantes del equipo

| Integrante | Rol | GitHub |
|---|---|---|
| Daniela Solano Restrepo | [Por definir] | [@Danisolre](https://github.com/Danisolre) |
| Jonathan Melo | [Por definir] | [@jonathanmelosa](https://github.com/jonathanmelosa) |
| Natalia Suescún | [Por definir] | [@NataliaSFernandez](https://github.com/NataliaSFernandez) |

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
│   ├── raw/                  # Datos originales del repositorio de replicación
│   │   └── README.md         # Descripción de los datos fuente (ECF_final.csv, shapefiles)
│   └── processed/            # Datos procesados y listos para visualización
│       └── README.md         # Descripción de los datos generados
│
├── code/
│   ├── 01_load_data.py       # Carga y validación de ECF_final.csv
│   ├── 02_merge_geo.py       # Unión del ECF con geometría de condados (shapefile)
│   └── 03_plot_figure1A.py   # Generación de la Figura 1A (mapa coroplético)
│
├── output/
│   └── figures/              # Figura replicada
│       └── README.md         # Descripción de los outputs generados
│
├── docs/                     # Documentación adicional y referencias
│   └── README.md
│
├── .gitignore
├── requirements.txt          # Dependencias de Python
└── README.md                 # Este archivo
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

- **ECF_final.csv** — Indicador de huella de carbono laboral por condado. Disponible en el [repositorio de replicación del artículo](https://github.com/MIT-CEEPR/ecf).
- **Shapefile de condados de EE.UU.** — Geometría para la visualización. Fuente: U.S. Census Bureau (TIGER/Line Shapefiles).

## Repositorio original de replicación

Los datos y código del artículo están disponibles en: [https://github.com/MIT-CEEPR/ecf](https://github.com/MIT-CEEPR/ecf)

## Instrucciones de ejecución

*(Se actualizará en los siguientes avances con el procedimiento paso a paso para replicar la Figura 1A.)*

```bash
# 1. Clonar el repositorio
git clone https://github.com/Danisolre/replication-graham-knittel-2024.git
cd replication-graham-knittel-2024

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar scripts (próximamente)
python code/01_load_data.py
python code/02_merge_geo.py
python code/03_plot_figure1A.py
```
