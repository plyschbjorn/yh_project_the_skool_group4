# processing.py
import pandas as pd
import duckdb as db
import json
from difflib import get_close_matches
from utils.constants import DATA_DIRECTORY, ASSETS_DIRECTORY

with open(ASSETS_DIRECTORY / "swedish_regions.geojson", "r") as file:
    geojson_data = json.load(file)

def load_beviljade_per_lan(year: int):
    path = DATA_DIRECTORY / f"resultat-{year}-for-kurser-inom-yh.xlsx"
    df = pd.read_excel(path)
    df["Årtal"] = df["Diarienummer"].str.extract(r'(\d{4})')

    valda = db.query(f"""
        SELECT 
            "Årtal",
            "Beslut",
            "Anordnare namn" AS "Anordnare",
            "Utbildningsnamn" AS "Kurs",
            "Utbildningsområde",
            "Län"
        FROM df
    """).df()

    # Summera antal beviljade per län
    beviljade_df = db.query(f"""
        SELECT 
            Län, 
            CAST(COUNT_IF(Beslut = 'Beviljad') AS INT) AS Beviljade
        FROM valda
        WHERE Län != 'Se "Lista flera kommuner"'
        GROUP BY Län
        ORDER BY Beviljade DESC
    """).df()

    total = valda.shape[0]
    approved = valda[valda["Beslut"] == "Beviljad"].shape[0]

    # Karta: matcha län -> länskod
    properties = [feature["properties"] for feature in geojson_data["features"]]
    region_codes = {
        prop["name"]: prop["ref:se:länskod"] for prop in properties
    }

    region_codes_map = [
        region_codes[get_close_matches(region, region_codes.keys(), n=1)[0]]
        for region in beviljade_df["Län"]
    ]

    return beviljade_df, region_codes_map, approved, total, geojson_data