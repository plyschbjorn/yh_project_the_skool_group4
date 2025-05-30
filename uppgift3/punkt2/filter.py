import pandas as pd
from taipy.gui import Gui, State
import taipy.gui.builder as tgb
import plotly.express as px
from pathlib import Path



DATA_DIRECTORY = Path(__file__).parents[2] / "files"
df = pd.read_excel(DATA_DIRECTORY / "long_format_cleaned_data.xlsx")



# Define dropdown options
years = sorted(df["Year"].dropna().unique().tolist())
indicators = [
    "Antal antagna som påbörjat studier",
    "Antal studerande",
    "Antal examinerade",
    "Examensgrad"
]

# Initial state
data = {
    "selected_year": years[0],
    "selected_indicator": indicators[0],
    "years": years,
    "indicators": indicators,
    "main_value": "",
    "percent_women": "",
    "percent_men": ""
}

# Update function
def update_result(state: State):
    filtered = df[df["Year"] == state.selected_year]
    main = filtered[filtered["Indicator"] == state.selected_indicator]
    women = filtered[filtered["Indicator"] == "därav andel kvinnor i procent"]
    men = filtered[filtered["Indicator"] == "därav andel män i procent"]

    state.main_value = main["Value"].values[0] if not main.empty else "N/A"
    state.percent_women = women["Value"].values[0] if not women.empty else ""
    state.percent_men = men["Value"].values[0] if not men.empty else ""

# GUI layout
with tgb.Page() as page:
    tgb.text("Select Year:")
    tgb.selector(label="Year", value="{selected_year}", choices="{years}", on_change=update_result)

    tgb.text("Select Indicator:")
    tgb.selector(label="Indicator", value="{selected_indicator}", choices="{indicators}", on_change=update_result)

    tgb.text("Total: {main_value}")
    tgb.text("Women %: {percent_women}")
    tgb.text("Men %: {percent_men}")

# Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8060)
