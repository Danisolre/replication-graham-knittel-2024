import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde la carpeta del proyecto
df = pd.read_csv("datos/crudo/ECF_total.csv")

# Mostrar primeras filas
print(df.head())

# Estadísticos descriptivos
print("\nEstadísticos descriptivos:")
print(df[['burden_avg','POP']].describe())

# Verificar valores faltantes
print("\nValores faltantes por columna:")
print(df.isnull().sum())

# Distribución de burden_avg
plt.figure(figsize=(8,5))
plt.hist(df['burden_avg'], bins=50)
plt.title("Distribución de la carga promedio de carbono")
plt.xlabel("burden_avg")
plt.ylabel("Frecuencia")
plt.show()

