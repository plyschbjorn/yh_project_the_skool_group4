from taipy.gui import Gui
import taipy.gui.builder as tgb
from backend.map_processing import load_beviljade_per_lan
from frontend.charts.map_charts import create_choropleth_map

# Funktion för att hämta data
def get_data(year):
    beviljade_df, region_codes_map, approved, total, geojson = load_beviljade_per_lan(year)
    choropleth_chart = create_choropleth_map(beviljade_df, region_codes_map, geojson, approved, total, year)
    return beviljade_df, choropleth_chart

# Initierade variabler
year_options = [2022, 2023, 2024]
selected_year = 2022
beviljade_df, choropleth_chart = get_data(selected_year)

# Knappens funktion
def on_filter_button_click(state):
    year = state.selected_year
    state.beviljade_df, state.choropleth_chart = get_data(year)

# GUI-layout
with tgb.Page() as map_page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        tgb.text("# Karta över MYH beviljade kurser", mode="md")

        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card"):
                tgb.text("## Beviljade kurser per län", mode="md")
                tgb.chart(figure="{choropleth_chart}")

            with tgb.part(class_name="card left-margin-md"):
                tgb.text("### Välj år", mode="md")
                tgb.selector("{selected_year}", lov=year_options, dropdown=True)
                tgb.button("Uppdatera karta", on_action=on_filter_button_click)

        with tgb.part(class_name="card"):
            tgb.text("## Datatabell", mode="md")
            tgb.table("{beviljade_df}")