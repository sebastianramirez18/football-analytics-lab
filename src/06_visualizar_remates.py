
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

input_file = DATA_DIR / "calidad_remates_primer_partido.csv"
FIGURES_DIR.mkdir(exist_ok=True)

df = pd.read_csv(input_file)

# Crear dos gráficos: goles y xG.
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(df["team_name"], df["goles"])
axes[0].set_title("Goles por equipo")
axes[0].set_ylabel("Goles")

axes[1].bar(df["team_name"], df["xG"])
axes[1].set_title("Goles esperados (xG)")
axes[1].set_ylabel("xG total")

for ax in axes:
    ax.set_xlabel("Equipo")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

fig.suptitle("Mundial Qatar 2022 — Calidad ofensiva")
fig.tight_layout()

output_file = FIGURES_DIR / "calidad_remates_primer_partido.png"
fig.savefig(output_file, dpi=150, bbox_inches="tight")
plt.show()

print(f"Gráfico guardado en: {output_file}")
