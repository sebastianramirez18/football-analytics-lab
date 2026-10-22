
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

df = pd.read_csv(DATA_DIR / "resumen_ofensivo_mundial_2022.csv")
FIGURES_DIR.mkdir(exist_ok=True)

# Diferencia entre goles reales y goles esperados.
df["diferencia_goles_xg"] = (
    df["goles_oficiales"] - df["xG"]
).round(2)

# Selecciones con mayor diferencia positiva y negativa.
df = df.sort_values("diferencia_goles_xg")

bottom = df.head(5)
top = df.tail(5).sort_values("diferencia_goles_xg", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].barh(bottom["equipo"], bottom["diferencia_goles_xg"])
axes[0].set_title("Goles por debajo del xG")
axes[0].set_xlabel("Goles oficiales − xG")
axes[0].axvline(0, linewidth=1)

axes[1].barh(top["equipo"], top["diferencia_goles_xg"])
axes[1].set_title("Goles por encima del xG")
axes[1].set_xlabel("Goles oficiales − xG")
axes[1].axvline(0, linewidth=1)

for ax in axes:
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)

fig.suptitle("Mundial Qatar 2022: goles frente a xG")
fig.tight_layout(rect=[0, 0.06, 1, 0.95])

# Añadir atribución visual a StatsBomb.
logo_file = PROJECT_ROOT / "assets" / "statsbomb-logo.png"

if logo_file.exists():
    logo = plt.imread(logo_file)
    image_box = OffsetImage(logo, zoom=0.07)
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

output_file = FIGURES_DIR / "goles_vs_xg_mundial_2022.png"


fig.savefig(output_file, dpi=150, bbox_inches="tight")
plt.show()

print("Mayor diferencia negativa:")
print(bottom[["equipo", "goles_oficiales", "xG", "diferencia_goles_xg"]].to_string(index=False))

print("\nMayor diferencia positiva:")
print(top[["equipo", "goles_oficiales", "xG", "diferencia_goles_xg"]].to_string(index=False))

print(f"\nGráfico guardado en: {output_file}")
