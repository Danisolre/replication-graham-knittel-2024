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
"""
plot_fig1A.py  v3
─────────────────────────────────────────────────────────────────────────────
Fixes:
  1. State outlines (not country outline) – per-state segment deduplication
  2. Vertical colorbar completely removed
  3. Alaska & Hawaii bigger and above the bottom bars
  4. Social cost bar matches paper (own log-spaced ticks, correct values)
"""

import json, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict


GEOJSON_PATH = "data/processed/counties_ecf_merged.geojson"
OUTPUT_PATH  = "output/fig1A_ecf_county.png"
ECF_COL_RAW  = "tonneCO2e_eff_peremp_avg"
LOG_COL      = "tonneCO2e_eff_peremp_avg_log10"
SCC          = 190   # $/tonne CO2e (EPA social cost of carbon used in paper)
DPI          = 200

# ── LOAD ──────────────────────────────────────────────────────────────────────
print("Loading GeoJSON …")
with open(GEOJSON_PATH) as f:
    features = json.load(f)["features"]

log_vals = np.array([
    feat["properties"][LOG_COL] for feat in features
    if feat["properties"].get(LOG_COL) is not None
    and int(str(feat["properties"].get("STATE","99")).zfill(2)) <= 56
])
log_min, log_max, log_mean = log_vals.min(), log_vals.max(), log_vals.mean()
print(f"ECF log10: min={log_min:.3f} mean={log_mean:.3f} max={log_max:.3f}")

# ── COLORMAP ──────────────────────────────────────────────────────────────────
cmap = LinearSegmentedColormap.from_list("ecf", [
    "#2166AC","#74ADD1","#ABD9E9","#E0F3F8","#FFFFBF",
    "#FEE090","#FDAE61","#F46D43","#D73027","#A50026"
], N=512)
norm = mcolors.TwoSlopeNorm(vmin=log_min, vcenter=log_mean, vmax=log_max)

# ── extract coordinates 
def get_rings(geo):
    if geo["type"] == "Polygon":
        return [np.array(geo["coordinates"][0])]
    return [np.array(p[0]) for p in geo["coordinates"]]

def county_collection(feats):
    patches, colors = [], []
    for f in feats:
        geo = f.get("geometry")
        if not geo: continue
        v = f["properties"].get(LOG_COL)
        c = cmap(norm(v)) if v is not None else (0.85, 0.85, 0.85, 1)
        for ring in get_rings(geo):
            patches.append(MplPolygon(ring, closed=True))
            colors.append(c)
    return PatchCollection(patches, facecolors=colors, edgecolors="#AAAAAA",
                           linewidths=0.2, zorder=2)

def state_outlines(feats, prec=3):
    """
    Per-state: segments appearing exactly once within a state = state exterior.
    Collect all states' exterior segments together → draws state borders only.
    """
    # Group by state
    by_state = defaultdict(list)
    for f in feats:
        si = str(f["properties"].get("STATE","99")).zfill(2)
        by_state[si].append(f)

    all_exterior = []
    for si, sfeats in by_state.items():
        seg_cnt = defaultdict(int)
        for f in sfeats:
            geo = f.get("geometry")
            if not geo: continue
            rings = (geo["coordinates"] if geo["type"] == "Polygon"
                     else [p for poly in geo["coordinates"] for p in poly])
            for ring in rings:
                pts = [(round(x, prec), round(y, prec)) for x, y in ring]
                for i in range(len(pts) - 1):
                    seg = tuple(sorted([pts[i], pts[i+1]]))
                    seg_cnt[seg] += 1
        all_exterior.extend(seg for seg, cnt in seg_cnt.items() if cnt == 1)

    return LineCollection(all_exterior, colors="black", linewidths=0.7, zorder=3)

# ── SPLIT FEATURES ────────────────────────────────────────────────────────────
cont, ak, hi = [], [], []
for f in features:
    si = int(str(f["properties"].get("STATE","99")).zfill(2))
    if si > 56: continue
    (ak if si == 2 else hi if si == 15 else cont).append(f)

# ── BUILD COLLECTIONS ─────────────────────────────────────────────────────────
print("Building state outlines …")
col_cont = county_collection(cont)
col_ak   = county_collection(ak)
col_hi   = county_collection(hi)
lc_cont = state_outlines(cont)
lc_ak   = state_outlines(ak)
lc_hi   = state_outlines(hi)

# ── FIGURE LAYOUT ─────────────────────────────────────────────────────────────
# Heights from bottom:
#   0.00–0.04  social cost bar
#   0.04–0.05  gap
#   0.05–0.12  ECF histogram
#   0.12–0.14  gap
#   0.14–0.32  AK / HI insets
#   0.32–1.00  main map
fig = plt.figure(figsize=(16, 10), facecolor="white", dpi=DPI)

# ── MAIN MAP ──────────────────────────────────────────────────────────────────
ax = fig.add_axes([0.00, 0.33, 0.88, 0.63])
ax.set_facecolor("white"); ax.set_aspect("equal"); ax.axis("off")
print("Drawing contiguous US …")
ax.add_collection(county_collection(cont))
ax.add_collection(lc_cont)
ax.autoscale_view()

# ── ALASKA  (large, above bottom bars) ────────────────────────────────────────
ax_ak = fig.add_axes([0.00, 0.15, 1.5, 0.18])  # [left, bottom, width, height]
ax_ak.set_facecolor("white"); ax_ak.set_aspect("equal"); ax_ak.axis("off")
print("Drawing Alaska …")
ax_ak.add_collection(county_collection(ak))
ax_ak.add_collection(lc_ak)
ax_ak.autoscale_view()


# ── HAWAII  (large, right of AK, above bottom bars) ───────────────────────────

# bounding box en coords de datos (incluye colecciones)
xmin, xmax = ax_ak.dataLim.xmin, ax_ak.dataLim.xmax
ymin, ymax = ax_ak.dataLim.ymin, ax_ak.dataLim.ymax

ax_hi = fig.add_axes([0.30, 0.15, 0.22, 0.16])
ax_hi.set_facecolor("white"); ax_hi.set_aspect("equal"); ax_hi.axis("off")
print("Drawing Hawaii …")
ax_hi.add_collection(county_collection(hi))
ax_hi.add_collection(lc_hi)
ax_hi.autoscale_view()

# ── ECF HISTOGRAM ─────────────────────────────────────────────────────────────
# Tick positions: paper uses 1.5, 5.5, 19(mean), 66, 230, 780, 2000
ecf_ticks_raw = [1.5, 5.5, 19, 66, 230, 780, 2000]
ecf_ticks_log = [np.log10(v) for v in ecf_ticks_raw
                 if log_min <= np.log10(v) <= log_max]

ax_hist = fig.add_axes([0.05, 0.07, 0.80, 0.055])
ax_hist.set_facecolor("white")
counts, edges = np.histogram(log_vals, bins=80)
mids = (edges[:-1] + edges[1:]) / 2
for l, r, cnt, col in zip(edges[:-1], edges[1:], counts,
                           [cmap(norm(m)) for m in mids]):
    ax_hist.bar(l, cnt, width=r - l, color=col, edgecolor="none", align="edge")

ax_hist.axvline(log_mean, color="black", linewidth=1.2, linestyle="--")
ax_hist.set_xlim(log_min - 0.05, log_max + 0.05)
ax_hist.set_ylim(bottom=0)
ax_hist.set_yticks([])
ax_hist.spines[["top", "right", "left"]].set_visible(False)
ax_hist.set_xticks(ecf_ticks_log)
ax_hist.set_xticklabels([f"{v:,}" for v in ecf_ticks_raw
                          if log_min <= np.log10(v) <= log_max], fontsize=8.5)
ax_hist.set_xlabel("Employment carbon footprint (metric tonnes CO₂e per employee)",
                   fontsize=9.5, labelpad=5)
ax_hist.tick_params(axis="x", length=4)

# ── SOCIAL COST BAR  (matches paper exactly) ──────────────────────────────────
# Paper ticks (from image): 367, 1270, 4400(mean), 15200, 52500, 182000, 463000
# Their log10(SC/190) positions map onto the same log_min–log_max x-axis
sc_ticks_raw  = [367, 1270, 4400, 15200, 52500, 182000, 463000]
sc_ticks_log  = [np.log10(v / SCC) for v in sc_ticks_raw]  # position on log-ECF axis

ax_sc = fig.add_axes([0.05, 0.015, 0.80, 0.027])

# Gradient image (same colormap, same norm)
gradient = np.linspace(log_min, log_max, 512).reshape(1, -1)
ax_sc.imshow(gradient, aspect="auto", cmap=cmap, norm=norm,
             extent=[log_min, log_max, 0, 1], origin="lower")
ax_sc.set_xlim(log_min - 0.05, log_max + 0.05)
ax_sc.set_ylim(0, 1)
ax_sc.set_yticks([])
ax_sc.spines[["top", "left", "right"]].set_visible(False)

# Only show ticks that fall within our data range
valid = [(lv, sv) for lv, sv in zip(sc_ticks_log, sc_ticks_raw)
         if log_min <= lv <= log_max]
ax_sc.set_xticks([lv for lv, _ in valid])

def fmt_sc(v):
    if v >= 1_000_000:
        return f"${v/1e6:,.2f}M"
    elif v >= 1_000:
        return f"${v/1e3:,.0f}k"
    return f"${v:,.0f}"

ax_sc.set_xticklabels([fmt_sc(sv) for _, sv in valid], fontsize=8.5)
ax_sc.set_xlabel("Social cost per employee (USD per employee)", fontsize=9.5, labelpad=5)
ax_sc.tick_params(axis="x", length=4)

# Mean dashed line on social cost bar
ax_sc.axvline(log_mean, color="black", linewidth=1.2, linestyle="--")

# ── TITLE ─────────────────────────────────────────────────────────────────────
fig.text(0.44, 0.985, "Overall employment carbon footprints, by county",
         ha="center", va="top", fontsize=14, fontweight="bold")
fig.text(0.44, 0.960, "Distribution of overall ECFs across counties",
         ha="center", va="top", fontsize=9, style="italic", color="#444444")

# ── SAVE ──────────────────────────────────────────────────────────────────────
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight", facecolor="white")
print(f"\n Saved → {OUTPUT_PATH}")
plt.close()