
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Objetivo:
1. Leer los eventos de un partido.
2. Convertirlos en una tabla con pandas.
3. Identificar los remates.
4. Resumir cuántos remates realizó cada equipo.
"""

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Encontrar el archivo de eventos que descargamos.
event_files = sorted(DATA_DIR.glob("events_*.json"))

if not event_files:
    raise FileNotFoundError(
        "No encontramos archivos events_*.json en la carpeta data."
    )

# Por ahora analizaremos un solo partido.
events_file = event_files[0]

with events_file.open("r", encoding="utf-8") as file:
    events = json.load(file)

# Convertir la lista de eventos en una tabla.
df = pd.json_normalize(events, sep="_")

print("Football Analytics Lab")
print("-" * 40)
print(f"Archivo analizado: {events_file.name}")
print(f"Total de eventos: {len(df)}")
print(f"Columnas disponibles: {len(df.columns)}")
print()

# Revisar qué tipos de eventos existen.
print("Tipos de eventos más frecuentes:")
print(df["type_name"].value_counts().head(10))
print()

# Seleccionar exclusivamente los remates.
shots = df[df["type_name"] == "Shot"].copy()

print(f"Total de remates: {len(shots)}")
print()

# Resumir los remates por equipo.
if not shots.empty:
    shots_by_team = (
        shots.groupby("team_name")
        .size()
        .reset_index(name="remates")
        .sort_values("remates", ascending=False)
    )

    print("Remates por equipo:")
    print(shots_by_team.to_string(index=False))

    # Guardar la tabla de remates para futuros análisis.
    output_file = DATA_DIR / "remates_primer_partido.csv"
    shots.to_csv(output_file, index=False, encoding="utf-8-sig")

    print()
    print(f"Tabla de remates guardada en: {output_file}")
else:
    print("No se encontraron remates en este archivo.")

print()
print("Análisis inicial completado.")
