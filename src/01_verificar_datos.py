
"""
Football Analytics Lab
Proyecto 01: Mundial de Qatar 2022

Primera prueba:
1. Descargar el catálogo de StatsBomb.
2. Guardarlo en nuestra carpeta data.
3. Identificar el Mundial masculino de 2022.
"""

import json
from pathlib import Path

import requests

# Catálogo oficial de competiciones de StatsBomb.
URL = (
    "https://raw.githubusercontent.com/"
    "hudl/open-data/master/data/competitions.json"
)

# Ubicamos la carpeta principal del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Creamos data si todavía no existe.
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "competitions.json"


def main():
    print("Football Analytics Lab")
    print("-" * 35)
    print("Descargando catálogo de StatsBomb...")

    # Descargamos los datos desde Internet.
    response = requests.get(URL, timeout=30)

    # Si hay un error HTTP, lo reportamos.
    response.raise_for_status()

    # Convertimos el JSON a una lista de Python.
    competitions = response.json()

    if not isinstance(competitions, list):
        raise ValueError("El catálogo no tiene el formato esperado.")

    # Guardamos una copia local de los datos originales.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            competitions,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Competiciones encontradas: {len(competitions)}")
    print(f"Catálogo guardado en: {OUTPUT_FILE}")
    print()

    # Buscamos el Mundial masculino de 2022.
    world_cup = [
        item
        for item in competitions
        if item.get("competition_name") == "FIFA World Cup"
        and str(item.get("season_name")) == "2022"
        and item.get("competition_gender") == "male"
    ]

    if not world_cup:
        print("No encontramos el Mundial de 2022.")
        print("Revisaremos la estructura del catálogo.")
        return

    for competition in world_cup:
        print("¡Mundial de 2022 encontrado!")
        print("Competición:", competition.get("competition_name"))
        print("Temporada:", competition.get("season_name"))
        print("Competition ID:", competition.get("competition_id"))
        print("Season ID:", competition.get("season_id"))

    print()
    print("Verificación inicial completada.")


if __name__ == "__main__":
    main()
