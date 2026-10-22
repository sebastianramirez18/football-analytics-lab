
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

input_file = DATA_DIR / "resumen_ofensivo_mundial_2022.csv"
FIGURES_DIR.mkdir(exist_ok=True)

df = pd.read_csv(input_file)

# Seleccionar las 10 selecciones con mayor xG.
top10 = df.nlargest(10, "xG").sort_values("xG")

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(top10["equipo"], top10["xG"])

ax.bar_label(bars, fmt="%.2f", padding=4)
ax.set_title("Mundial Qatar 2022: Top 10 selecciones por xG")
ax.set_xlabel("Goles esperados (xG)")
ax.set_ylabel("Selección")
ax.grid(axis="x", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()

output_file = FIGURES_DIR / "top10_xg_mundial_2022.png"

# Añadir atribución visual a StatsBomb.
logo_file = PROJECT_ROOT / "assets" / "statsbomb-logo.png"

if logo_file.exists():
    logo = plt.imread(logo_file)
    image_box = OffsetImage(logo, zoom=0.12)
    annotation = AnnotationBbox(
        image_box,
        (0.99, 0.01),
        xycoords="figure fraction",
        box_alignment=(1, 0),
        frameon=False,
    )
    fig.add_artist(annotation)

fig.text(
    0.01,
    0.01,
    "Data: StatsBomb Open Data",
    fontsize=8,
    alpha=0.8,
)

fig.savefig(output_file, dpi=150, bbox_inches="tight")
plt.show()

print(f"Gráfico guardado en: {output_file}")
