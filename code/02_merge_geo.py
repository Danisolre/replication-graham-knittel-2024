"""
02_merge_geo.py
---------------
Unión del dataset ECF con la geometría de condados de EE.UU.

Tareas planificadas:
- Cargar shapefile de condados (TIGER/Line, U.S. Census Bureau)
- Unir ECF_final.csv con la geometría usando el código FIPS como llave
- Verificar cobertura: identificar condados sin match
- Exportar GeoDataFrame consolidado a data/processed/

Desafío anticipado: Asegurar que las llaves FIPS del ECF y del shapefile
empaten correctamente (formato, ceros iniciales, etc.)
"""

# TODO: Implementar en Avance 2
