"""
02_explore_data.py
---------------
Exploración y análisis descriptivo del archivo ECF_final.csv.
Tareas planificadas:
- Cargar el dataset ECF_total.csv desde data/raw/
- Inspeccionar la estructura: columnas, tipos de datos, valores faltantes
- Validar que el campo de identificación de condado (FIPS) sea consistente
- Realizar análisis descriptivo: distribución de burden_avg, estadísticas de población

Fuente de datos: https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials
FUENTE: https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials/blob/main/Analysis/overallFootprintCalc/Output/ECF_total.csv
"""

import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde la carpeta del proyecto
df = pd.read_csv("data/raw/ECF_total.csv")

# Mostrar primeras filas
print("Primeras filas del dataset:")
print(df.head())

# Número total de registros
print("\nNúmero total de registros:")
print(len(df))

# Estadísticas descriptivas
print("\nEstadísticas descriptivas:")
print(df[['burden_avg', 'POP']].describe())

# Verificar valores faltantes
print("\nValores faltantes por columna:")
print(df.isnull().sum())

# Estadísticas adicionales para validar la distribución
print("\nValor mínimo de burden_avg:", df['burden_avg'].min())
print("Valor máximo de burden_avg:", df['burden_avg'].max())
print("Promedio de burden_avg:", df['burden_avg'].mean())

# Distribución de la carga promedio de carbono
plt.figure(figsize=(8,5))
plt.hist(df['burden_avg'], bins=50)
plt.title("Distribución de la carga promedio de carbono")
plt.xlabel("burden_avg")
plt.ylabel("Frecuencia")
OUTPUT_PATH = "output/Distribucion_burden_avg.png"
plt.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor="white")
plt.close()
plt.show()

# Validación final del número de condados analizados
print("\nNúmero total de condados analizados:", len(df))

# Mostrar columnas del dataset
print("\nColumnas disponibles en el dataset:")
print(df.columns.tolist())

# Estadísticas de población
print("\nEstadísticas de población:")
print(df['POP'].describe())








