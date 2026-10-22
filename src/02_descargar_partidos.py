
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Objetivo:
Descargar la lista oficial de partidos del Mundial
masculino de 2022 desde StatsBomb Open Data.
"""

import json
from pathlib import Path

import requests

# Identificadores que verificamos en el paso anterior.
COMPETITION_ID = 43
SEASON_ID = 106

# Dirección oficial del archivo de partidos.
URL = (
    "https://raw.githubusercontent.com/"
    "hudl/open-data/master/data/matches/"
    f"{COMPETITION_ID}/{SEASON_ID}.json"
)

# Encontrar la carpeta principal del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Definir dónde guardaremos los partidos.
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "matches_world_cup_2022.json"


def main():
    print("Football Analytics Lab")
    print("-" * 40)
    print("Descargando partidos del Mundial 2022...")

    # Descargar el archivo de partidos.
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    matches = response.json()

    # Comprobar que los datos tengan el formato esperado.
    if not isinstance(matches, list):
        raise ValueError("La respuesta no contiene una lista de partidos.")

    if not matches:
        raise ValueError("La lista de partidos está vacía.")

    # Guardar una copia local de los datos originales.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            matches,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Partidos descargados: {len(matches)}")
    print(f"Archivo guardado en: {OUTPUT_FILE}")
    print()

    # Mostrar algunos encuentros como ejemplo.
    print("Primeros cinco partidos:")

    for match in matches[:5]:
        home_team = match.get("home_team", {}).get("home_team_name")
        away_team = match.get("away_team", {}).get("away_team_name")
        match_date = match.get("match_date")

        print(f"{match_date}: {home_team} vs. {away_team}")

    print()
    print("Descarga y verificación completadas.")


if __name__ == "__main__":
    main()
