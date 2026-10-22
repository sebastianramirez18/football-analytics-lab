
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Objetivo:
Comparar remates, goles y goles esperados (xG)
por equipo en el partido analizado.
"""

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

event_files = sorted(DATA_DIR.glob("events_*.json"))

if not event_files:
    raise FileNotFoundError(
        "No encontramos archivos events_*.json en la carpeta data."
    )

events_file = event_files[0]

with events_file.open("r", encoding="utf-8") as file:
    events = json.load(file)

df = pd.json_normalize(events, sep="_")

# Seleccionar los eventos de tipo remate.
shots = df[df["type_name"] == "Shot"].copy()

if shots.empty:
    print("No se encontraron remates.")
    raise SystemExit

# Algunas columnas podrían faltar si no aparecen en los datos.
if "shot_outcome_name" not in shots.columns:
    shots["shot_outcome_name"] = None

if "shot_statsbomb_xg" not in shots.columns:
    shots["shot_statsbomb_xg"] = 0.0

shots["shot_statsbomb_xg"] = pd.to_numeric(
    shots["shot_statsbomb_xg"], errors="coerce"
).fillna(0)

# Un gol es un remate cuyo resultado es Goal.
shots["gol"] = (
    shots["shot_outcome_name"] == "Goal"
).astype(int)

# Resumen por equipo.
resumen = (
    shots.groupby("team_name")
    .agg(
        remates=("type_name", "size"),
        goles=("gol", "sum"),
        xG=("shot_statsbomb_xg", "sum"),
    )
    .reset_index()
)

resumen["precision_gol_pct"] = (
    resumen["goles"] / resumen["remates"] * 100
).round(1)

resumen["xG"] = resumen["xG"].round(2)

resumen = resumen.sort_values("xG", ascending=False)

print("FOOTBALL ANALYTICS LAB")
print("=" * 45)
print(f"Archivo analizado: {events_file.name}")
print()
print("Calidad ofensiva por equipo:")
print(resumen.to_string(index=False))
print()

output_file = DATA_DIR / "calidad_remates_primer_partido.csv"
resumen.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Resumen guardado en: {output_file}")
