import taipy.gui.builder as tgb
from backend.map_processing import kurs_2022, kurs_2023, kurs_2024
from backend.anordnare_processing import load_anordnarstatistik
import pandas as pd

# Initiera variabler
selected_year_org = 2022
selected_anordnare = ""
anordnar_df, approved, total, approved_ratio = load_anordnarstatistik("", selected_year_org)

# Lista unika anordnare för selector
all_anordnare_df = pd.concat([kurs_2022, kurs_2023, kurs_2024])
all_anordnare_list = sorted(all_anordnare_df["Anordnare namn"].dropna().unique().tolist())

def on_filter_anordnare(state):
    year = state.selected_year_org
    anordnare = state.selected_anordnare
    state.anordnar_df, state.approved, state.total, state.approved_ratio = load_anordnarstatistik(anordnare, year)

with tgb.Page() as anordnare_page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        tgb.text("# Statistik för Anordnare", mode="md")

        with tgb.layout(columns="1 1"):
            with tgb.part(class_name="card"):
                tgb.selector("{selected_anordnare}",label="Välj anordnare", lov=all_anordnare_list, dropdown=True)
                tgb.selector("{selected_year_org}", lov=[2022, 2023, 2024], dropdown=True)
                tgb.button("Filtrera", on_action=on_filter_anordnare)

            with tgb.part(class_name="card"):
                tgb.text("## Statistik", mode="md")
                tgb.text("Totalt antal kurser: **{total}**", mode="md")
                tgb.text("Antal beviljade kurser: **{approved}**", mode="md")
                tgb.text("Andel beviljade: **{approved_ratio:.1%}**", mode="md")

        tgb.text("## Detaljerad data", mode="md")
        tgb.table("{anordnar_df}")

    __all__ = ["anordnare_page"]