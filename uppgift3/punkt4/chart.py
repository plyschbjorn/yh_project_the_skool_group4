import pandas as pd
from pathlib import Path
import taipy.gui.builder as tgb
from taipy.gui import Gui

PROJECT_ROOT = Path(r"C:\Users\azizm\Documents\github\yh_project_the_skool_group4")

FILES_DIR = PROJECT_ROOT / "files"
DATA_DIR = PROJECT_ROOT / "EDA_filer" / "Data"

df = pd.read_csv(FILES_DIR / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df_schablon = pd.read_excel(FILES_DIR / "2024_tabell3.xlsx", sheet_name="Tabell 3", skiprows=5)

df_statsbidrag = pd.read_csv(DATA_DIR / "statsbidrag_schablonnivåer.csv", sep=",", encoding="utf-8-sig")

df["Totalt antal platser"] = df.iloc[:, 1:].sum(axis=1)

df_kpi = pd.merge(
    df,
    df_statsbidrag[["Utbildningsområde", "Med momskompensation"]],
    on="Utbildningsområde",
    how="inner"
)

df_kpi["Beräknad kostnad"] = df_kpi["Totalt antal platser"] * df_kpi["Med momskompensation"]

selected_educational_area = "Data/IT"
educational_areas = df_kpi["Utbildningsområde"].unique().tolist()
total_places = cost_per_place = total_cost = "Välj område"

filtered_df_kpi = pd.DataFrame(columns=["Utbildningsområde", "Totalt antal platser", "Beräknad kostnad"])

def filter_kpi(state):
    data = df_kpi[df_kpi["Utbildningsområde"] == state.selected_educational_area]
    if not data.empty:
        state.total_places = f"{int(data['Totalt antal platser'].values[0]):,} st"
        state.cost_per_place = f"{int(data['Med momskompensation'].values[0]):,} kr"
        state.total_cost = f"{int(data['Beräknad kostnad'].values[0]):,} kr"

        state.filtered_df_kpi = pd.DataFrame({
            "Utbildningsområde": [state.selected_educational_area],
            "Totalt antal platser": [int(data['Totalt antal platser'].values[0])],
            "Beräknad kostnad": [int(data['Beräknad kostnad'].values[0])]
        })
    else:
        state.total_places = state.cost_per_place = state.total_cost = "0"
        state.filtered_df_kpi = pd.DataFrame(columns=["Utbildningsområde", "Totalt antal platser", "Beräknad kostnad"])

with tgb.Page() as page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="card"):
            tgb.text("# KPI för utbildningsområden", mode="md")
            tgb.selector("Välj område", value="{selected_educational_area}", lov=educational_areas, dropdown=True)
            tgb.button("Visa KPI", on_action=filter_kpi)
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card"):
                tgb.text("Totalt antal platser")
                tgb.text("{total_places}")
            with tgb.part(class_name="card"):
                tgb.text("Statsbidrag per plats")
                tgb.text("{cost_per_place}")
            with tgb.part(class_name="card"):
                tgb.text("Beräknad total kostnad")
                tgb.text("{total_cost}")
        with tgb.part(class_name="card"):
            tgb.text("### Diagram för valt område")
            tgb.chart(
                data="{filtered_df_kpi}",
                x="Utbildningsområde",
                y=["Totalt antal platser", "Beräknad kostnad"],
                type="bar"
            )

Gui(page).run()
