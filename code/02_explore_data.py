import pandas as pd
import matplotlib.pyplot as plt

# cargar datos desde la carpeta del proyecto
df = pd.read_csv("data/raw/ECF_total.csv")

# mostrar primeras filas
print(df.head())

# estadísticos descriptivos
print(df[['burden_avg','POP']].describe())

# verificar valores faltantes
print(df.isnull().sum())

# distribución de burden_avg
plt.figure(figsize=(8,5))
plt.hist(df['burden_avg'], bins=50)
plt.title("Distribución de la carga promedio de carbono")
plt.xlabel("burden_avg")
plt.ylabel("Frecuencia")
plt.show()
