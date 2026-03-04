"""
02_figure1A.py
────────────────────────────────────────────────────────────────────────────────
Replicates Figure 1A from Graham & Knittel (2024) PNAS:
  Panel A - Overall employment carbon footprints, by county

Inputs  (produced by 03_merge_geo.py)
---------
  data/merged_ecf_counties.geojson  - county polygons + ECF attributes

Output
------
  figures/fig1A_county.png   – high-resolution county map  (≈ Fig 1A)
 
Usage
-----
  python 04_plot_figure1A.py

"""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# ── paths 
GEOJSON_PATH = "data/processed/counties_ecf_merged.geojson"
OUTPUT_PATH  = "output/fig1A_ecf_county.png"
ECF_COL_RAW  = "tonneCO2e_eff_peremp_avg"
LOG_COL      = "tonneCO2e_eff_peremp_avg_log10"
SCC          = 190   # $/tonne CO2e (EPA social cost of carbon used in paper)
DPI          = 200

# ── LOAD GEOJSON 
print("Loading GeoJSON …")
with open(GEOJSON_PATH) as f:
    gj = json.load(f)

features = gj["features"]

# ── COLLECT ECF VALUES FOR SCALE ──────────────────────────────────────────────
log_vals = []
for feat in features:
    p = feat["properties"]
    state = str(p.get("STATE", "99")).zfill(2)
    if int(state) > 56:
        continue
    v = p.get(LOG_COL)
    if v is not None:
        log_vals.append(v)

log_vals = np.array(log_vals)
log_min  = log_vals.min()
log_max  = log_vals.max()
log_mean = log_vals.mean()

print(f"log10 ECF → min={log_min:.3f}  mean={log_mean:.3f}  max={log_max:.3f}")
print(f"ECF (raw) → min={10**log_min:.1f}  mean={10**log_mean:.1f}  max={10**log_max:.1f}")

# ── COLORS: blue (below mean) → white → orange/red (above mean) 
colors_diverging = [
    "#2166AC",   # dark blue
    "#74ADD1",   # medium blue
    "#ABD9E9",   # light blue
    "#E0F3F8",   # very light blue
    "#FFFFBF",   # near-white/pale yellow (centre)
    "#FEE090",   # light orange
    "#FDAE61",   # orange
    "#F46D43",   # dark orange
    "#D73027",   # red
    "#A50026",   # deep red
]
cmap = LinearSegmentedColormap.from_list("ecf_div", colors_diverging, N=512)
norm = mcolors.TwoSlopeNorm(vmin=log_min, vcenter=log_mean, vmax=log_max)

# ── extract coordinates 
def get_rings(geometry):
    """Return list of numpy arrays (each an exterior ring), handling Polygon & MultiPolygon."""
    rings = []
    if geometry["type"] == "Polygon":
        rings.append(np.array(geometry["coordinates"][0]))
    elif geometry["type"] == "MultiPolygon":
        for poly in geometry["coordinates"]:
            rings.append(np.array(poly[0]))
    return rings

# build patch collection for a set of features 
def build_collection(feats, norm, cmap, transform=None):
    patches = []
    facecolors = []
    for feat in feats:
        p   = feat["properties"]
        geo = feat.get("geometry")
        if geo is None:
            continue
        v = p.get(LOG_COL)
        color = cmap(norm(v)) if v is not None else (0.85, 0.85, 0.85, 1.0)
        for ring in get_rings(geo):
            if transform is not None:
                ring = transform(ring)
            patch = MplPolygon(ring, closed=True)
            patches.append(patch)
            facecolors.append(color)
    col = PatchCollection(patches, facecolors=facecolors,
                          edgecolors="#999999", linewidths=0.15, zorder=2)
    return col

# ── SPLIT FEATURES ────────────────────────────────────────────────────────────
feats_cont = []
feats_ak   = []
feats_hi   = []

for feat in features:
    state = str(feat["properties"].get("STATE", "99")).zfill(2)
    si = int(state)
    if si > 56:
        continue
    if si == 2:
        feats_ak.append(feat)
    elif si == 15:
        feats_hi.append(feat)
    else:
        feats_cont.append(feat)

# ── FIGURE LAYOUT ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 9), facecolor="white", dpi=DPI)

# Main map axes (contiguous US)
ax = fig.add_axes([0.00, 0.12, 0.82, 0.82])
ax.set_facecolor("white")
ax.set_aspect("equal")
ax.axis("off")

# Alaska inset
ax_ak = fig.add_axes([0.00, 0.01, 0.20, 0.20])
ax_ak.set_facecolor("white")
ax_ak.set_aspect("equal")
ax_ak.axis("off")

# Hawaii inset
ax_hi = fig.add_axes([0.20, 0.01, 0.13, 0.10])
ax_hi.set_facecolor("white")
ax_hi.set_aspect("equal")
ax_hi.axis("off")

# ── DRAW CONTIGUOUS US 
print("Drawing contiguous US …")
col_cont = build_collection(feats_cont, norm, cmap)
ax.add_collection(col_cont)
ax.autoscale_view()

# ── DRAW ALASKA 
print("Drawing Alaska …")
col_ak = build_collection(feats_ak, norm, cmap)
ax_ak.add_collection(col_ak)
ax_ak.autoscale_view()

# ── DRAW HAWAII 
print("Drawing Hawaii …")
col_hi = build_collection(feats_hi, norm, cmap)
ax_hi.add_collection(col_hi)
ax_hi.autoscale_view()

# ── COLORBAR 
cbar_ax = fig.add_axes([0.84, 0.18, 0.025, 0.62])
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cb = fig.colorbar(sm, cax=cbar_ax, orientation="vertical", extend="neither")

# Ticks matching paper (raw ECF values)
tick_ecf    = [1.5, 5.5, 19, 66, 230, 780, 2000]
tick_log10  = [np.log10(v) for v in tick_ecf if log_min <= np.log10(v) <= log_max]
tick_labels = [f"{v:,.0f}" for v in tick_ecf if log_min <= np.log10(v) <= log_max]
cb.set_ticks(tick_log10)
cb.set_ticklabels(tick_labels)
cb.ax.tick_params(labelsize=7.5)
cb.set_label(
    "Employment carbon footprint\n(metric tonnes CO₂e per employee)",
    fontsize=8.5, labelpad=6
)

# Dashed line at national log mean
mean_norm = norm(log_mean)
cb.ax.axhline(mean_norm, color="black", linewidth=1.4, linestyle="--")

# Label mean
cbar_ax.text(
    1.15, mean_norm,
    f"  National\n  mean\n  ({10**log_mean:.0f})",
    fontsize=6.5, va="center", ha="left",
    transform=cbar_ax.transAxes, color="#222222"
)

# ── SECONDARY AXIS: Social cost ────────────────────────────────────────────────
ax2 = cbar_ax.twinx()
ax2.set_ylim(cbar_ax.get_ylim())

sc_ticks = []
sc_labels_right = []
for v in tick_ecf:
    lv = np.log10(v)
    if log_min <= lv <= log_max:
        sc = v * SCC
        sc_ticks.append(norm(lv))
        if sc >= 1_000_000:
            sc_labels_right.append(f"${sc/1e6:,.0f}M")
        elif sc >= 1_000:
            sc_labels_right.append(f"${sc/1e3:,.0f}k")
        else:
            sc_labels_right.append(f"${sc:,.0f}")

ax2.set_yticks(sc_ticks)
ax2.set_yticklabels(sc_labels_right, fontsize=6.5)
ax2.set_ylabel("Social cost per employee (USD)", fontsize=7.5, labelpad=6)

# ── HISTOGRAM (bottom, matching paper's distribution bar) ─────────────────────
ax_hist = fig.add_axes([0.05, 0.07, 0.56, 0.05])
ax_hist.set_facecolor("white")

# Colour each bar according to its log10 value
n_bins = 80
counts, bin_edges = np.histogram(log_vals, bins=n_bins)
bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
bar_colors = [cmap(norm(c)) for c in bin_centres]

for i, (left, right, count, color) in enumerate(
        zip(bin_edges[:-1], bin_edges[1:], counts, bar_colors)):
    ax_hist.bar(left, count, width=(right - left), color=color,
                edgecolor="none", align="edge")

ax_hist.axvline(log_mean, color="black", linewidth=1.2, linestyle="--")
ax_hist.set_xlim(log_min - 0.05, log_max + 0.05)
ax_hist.set_yticks([])
ax_hist.spines[["top", "right", "left"]].set_visible(False)
ax_hist.tick_params(axis="x", labelsize=7)

# Custom x-tick labels: show raw ECF values at log positions
nice_vals = [1.5, 5.5, 19, 66, 230, 780, 2000]
ax_hist.set_xticks([np.log10(v) for v in nice_vals])
ax_hist.set_xticklabels([f"{v:,}" for v in nice_vals], fontsize=7)

# Min / mean / max annotations
for xval, raw, va_ in [
    (log_min,  10**log_min,  "top"),
    (log_mean, 10**log_mean, "top"),
    (log_max,  10**log_max,  "top"),
]:
    ax_hist.axvline(xval, color="#444444", linewidth=0.7, linestyle=":")

ax_hist.set_xlabel(
    "Employment carbon footprint (metric tonnes CO₂e per employee)",
    fontsize=8, labelpad=4
)

# Social cost secondary x-axis label below histogram
fig.text(0.05, 0.035,
         f"Social cost per employee (USD per employee, at ${SCC}/tCO₂e)",
         fontsize=7, color="#555555")

# ── TITLE ─────────────────────────────────────────────────────────────────────
fig.text(
    0.41, 0.97,
    "Overall employment carbon footprints, by county",
    ha="center", va="top", fontsize=14, fontweight="bold"
)
fig.text(
    0.41, 0.935,
    "Distribution of overall ECFs across counties",
    ha="center", va="top", fontsize=9, style="italic", color="#444444"
)

# ── SAVE ──────────────────────────────────────────────────────────────────────
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight", facecolor="white")
print(f"\n Gráfica guardada en {OUTPUT_PATH}")
plt.close()