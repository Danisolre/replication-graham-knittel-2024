#!/bin/bash
# =============================================================================
# run_pipeline.sh — Ejecuta el pipeline completo de replicación
# Replicación de la Figura 1A — Graham & Knittel (2024)
# =============================================================================
#
# Uso:
#   chmod +x run_pipeline.sh
#   ./run_pipeline.sh
#
# Requisitos:
#   - Python 3.10+
#   - Dependencias instaladas: pip install -r requirements.txt
# =============================================================================

set -e  # Detener ejecución si algún script falla

echo "============================================="
echo " Pipeline de Replicación — Figura 1A"
echo " Graham & Knittel (2024)"
echo "============================================="
echo ""

echo "[1/4] Cargando y validando datos..."
python code/01_load_data.py
echo ""

echo "[2/4] Análisis exploratorio y estadísticas descriptivas..."
python code/02_explore_data.py
echo ""

echo "[3/4] Merge geoespacial (ECF + geometría de condados)..."
python code/03_merge_geo.py
echo ""

echo "[4/4] Generando Figura 1A (mapa coroplético)..."
python code/04_plot_figure1A.py
echo ""

echo "============================================="
echo " Pipeline completado exitosamente."
echo " Figura guardada en: output/figures/fig1A_ecf_county.png"
echo "============================================="
