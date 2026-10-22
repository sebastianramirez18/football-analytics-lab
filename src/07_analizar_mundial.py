
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Analiza los remates, goles de remate y xG
de las 32 selecciones durante el Mundial.
"""

import json
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

MATCHES_FILE = DATA_DIR / "matches_world_cup_2022.json"
BASE_URL = (
    "https://raw.githubusercontent.com/hudl/open-data/"
    "master/data/events"
)

# 1. Cargar los 64 partidos.
with MATCHES_FILE.open("r", encoding="utf-8") as file:
    matches = json.load(file)

session = requests.Session()
resumen_partidos = []
errores = []

print("FOOTBALL ANALYTICS LAB")
print("=" * 50)
print(f"Partidos encontrados: {len(matches)}")
print("Procesando eventos...\n")

remates_sin_xg = 0

# 2. Procesar los eventos de cada partido.
for i, match in enumerate(matches, start=1):
    match_id = match["match_id"]
    events_file = DATA_DIR / f"events_{match_id}.json"

    try:
        # Reutilizar eventos descargados previamente.
        if events_file.exists():
            with events_file.open("r", encoding="utf-8") as file:
                events = json.load(file)
        else:
            url = f"{BASE_URL}/{match_id}.json"
            response = session.get(url, timeout=30)
            response.raise_for_status()
            events = response.json()

            with events_file.open("w", encoding="utf-8") as file:
                json.dump(events, file, ensure_ascii=False)

        # Convertir los eventos en una tabla.
        df = pd.json_normalize(events, sep="_")

        # Filtrar los remates.
        shots = df[df["type_name"] == "Shot"].copy()
        if "period" in shots.columns:
            shots = shots[shots["period"] != 5].copy()

        # Preparar columnas necesarias.
        if "shot_outcome_name" not in shots.columns:
            shots["shot_outcome_name"] = None

        if "shot_statsbomb_xg" not in shots.columns:
             remates_sin_xg += len(shots)
             shots["shot_statsbomb_xg"] = float("nan")

        shots["shot_statsbomb_xg"] = pd.to_numeric(
            shots["shot_statsbomb_xg"],
            errors="coerce"
        )

        remates_sin_xg += shots["shot_statsbomb_xg"].isna().sum()

        # Solo para poder continuar el procesamiento.
        # Los valores faltantes ya quedaron contabilizados.
        shots["shot_statsbomb_xg"] = shots["shot_statsbomb_xg"].fillna(0)

        shots["gol_de_remate"] = (
            shots["shot_outcome_name"] == "Goal"
        ).astype(int)

        # 3. Crear un registro para cada equipo del partido.
        equipos = [
            (
                match["home_team"]["home_team_name"],
                match["home_score"],
            ),
            (
                match["away_team"]["away_team_name"],
                match["away_score"],
            ),
        ]

        for team_name, goles_oficiales in equipos:
            team_shots = shots[
                shots["team_name"] == team_name
            ]

            resumen_partidos.append({
                "partido_id": match_id,
                "fecha": match["match_date"],
                "equipo": team_name,
                "goles_oficiales": goles_oficiales,
                "remates": len(team_shots),
                "goles_de_remate": int(
                    team_shots["gol_de_remate"].sum()
                ),
                "xG": team_shots["shot_statsbomb_xg"].sum(),
            })

        if i % 8 == 0 or i == len(matches):
            print(f"Partidos procesados: {i}/{len(matches)}")

    except (requests.RequestException, ValueError, KeyError, OSError) as error:
        errores.append((match_id, str(error)))
        print(f"Error en el partido {match_id}: {error}")

# 4. No presentar un resumen parcial como si estuviera completo.
if errores:
    print(f"\nHubo {len(errores)} errores.")
    print("No se generará el resumen final para evitar resultados incompletos.")
    raise SystemExit(1)

partidos_df = pd.DataFrame(resumen_partidos)

# 5. Consolidar los datos por selección.
resumen = (
    partidos_df.groupby("equipo", as_index=False)
    .agg(
        partidos=("partido_id", "nunique"),
        goles_oficiales=("goles_oficiales", "sum"),
        remates=("remates", "sum"),
        goles_de_remate=("goles_de_remate", "sum"),
        xG=("xG", "sum"),
    )
)

resumen["xG"] = resumen["xG"].round(2)
resumen = resumen.sort_values("xG", ascending=False)

# 6. Guardar resultados.
partidos_file = DATA_DIR / "resumen_por_partido.csv"
equipos_file = DATA_DIR / "resumen_ofensivo_mundial_2022.csv"

partidos_df.to_csv(
    partidos_file, index=False, encoding="utf-8-sig"
)
resumen.to_csv(
    equipos_file, index=False, encoding="utf-8-sig"
)

print("\nTOP 10 SELECCIONES POR xG")
print("=" * 65)
print(resumen.head(10).to_string(index=False))

print(f"\nSelecciones analizadas: {resumen['equipo'].nunique()}")
print(f"Partidos analizados: {partidos_df['partido_id'].nunique()}")
print(f"Resumen por partido: {partidos_file}")
print(f"Resumen por selección: {equipos_file}")

print("\nVALIDACIÓN GENERAL")
print("=" * 50)

print("Partidos únicos:", partidos_df["partido_id"].nunique())
print("Selecciones:", resumen["equipo"].nunique())
print("Goles oficiales totales:", resumen["goles_oficiales"].sum())
print("Goles de remate:", resumen["goles_de_remate"].sum())
print("Remates totales:", resumen["remates"].sum())
print("xG total:", round(resumen["xG"].sum(), 2))

print("\nSelecciones sin remates:")
print(
    resumen.loc[resumen["remates"] == 0, ["equipo", "partidos"]]
    .to_string(index=False)
)

print("\nDiferencias entre goles oficiales y goles de remate:")
print(
    resumen.loc[
        resumen["goles_oficiales"] != resumen["goles_de_remate"],
        [
            "equipo",
            "goles_oficiales",
            "goles_de_remate",
            "remates",
            "xG",
        ],
    ].to_string(index=False)
)
print("Remates sin xG válido:", remates_sin_xg)
print("\nPromedio de xG por remate:")
if resumen["remates"].sum() > 0:
    print(round(resumen["xG"].sum() / resumen["remates"].sum(), 3))