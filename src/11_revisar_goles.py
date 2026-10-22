
from pathlib import Path
import json
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

partidos = {
    3857276: "Canadá",
    3857292: "Costa Rica",
    3869151: "Australia",
}

for match_id, equipo in partidos.items():
    archivo = DATA_DIR / f"events_{match_id}.json"

    with archivo.open("r", encoding="utf-8") as f:
        eventos = json.load(f)

    df = pd.json_normalize(eventos, sep="_")

    goles = df[
        (df["type_name"] == "Shot")
        & (df["shot_outcome_name"] == "Goal")
    ].copy()

    columnas = [
        c for c in [
            "team_name",
            "player_name",
            "shot_type_name",
            "shot_technique_name",
            "shot_outcome_name",
            "period",
        ]
        if c in goles.columns
    ]

    print(f"\n{equipo} — partido {match_id}")
    print("=" * 55)
    print(goles[columnas].to_string(index=False))



print("\nEVENTOS RELACIONADOS CON AUTOGOLES")
print("=" * 55)

for match_id, equipo in partidos.items():
    archivo = DATA_DIR / f"events_{match_id}.json"

    with archivo.open("r", encoding="utf-8") as f:
        eventos = json.load(f)

    df = pd.json_normalize(eventos, sep="_")

    if "type_name" in df.columns:
        relacionados = df[
            df["type_name"].astype(str).str.contains(
                "own goal", case=False, na=False
            )
        ]

        print(f"\nPartido {match_id} — {equipo}")
        columnas = [
            c for c in [
                "type_name",
                "team_name",
                "player_name",
                "minute",
                "period",
            ]
            if c in relacionados.columns
        ]
        print(relacionados[columnas].to_string(index=False))
