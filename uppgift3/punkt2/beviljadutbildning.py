
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from pathlib import Path
import pandas as pd  
#from utils.constants import DATA_DIRECTORY





# === 1. Load and transform data ===
DATA_DIRECTORY = Path(__file__).parents[2] / "files"
df = pd.read_csv(DATA_DIRECTORY / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df_2024 = pd.read_excel(
    DATA_DIRECTORY / "2024_tabell3.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)


long_df = df.melt(id_vars="Utbildningsområde", var_name="År", value_name="Beviljade")
long_df["År"] = long_df["År"].astype(int)

# === 2. Define state variables ===
utb_list = sorted(long_df["Utbildningsområde"].unique().tolist())
selected_field = utb_list[0]

# === 3. Create table for each utbildningsområde
all_tables = {
    utb: long_df[long_df["Utbildningsområde"] == utb] for utb in utb_list
}

# === 4. Chart generator function ===
def generate_chart(utb):
    filtered = long_df[long_df["Utbildningsområde"] == utb]
    fig = px.line(
        filtered,
        x="År",
        y="Beviljade",
        title=f"Beviljade platser för <b>{utb}</b>",
        line_shape="spline",
    )
    fig.update_traces(
        line=dict(width=3, dash='dash'),
        marker=dict(size=10, symbol='circle'),
        mode='lines+markers'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="År",
        yaxis_title="Antal studerande",
        font=dict(size=12),
        title_x=0.5,
        width=700,
        height=400,
        margin=dict(l=80, r=30, t=60, b=60),
        yaxis=dict(
            ticklabelstandoff=15,
            showline=True,
            linecolor='lightgray',
            linewidth=2
        ),
        xaxis=dict(
            showline=True,
            linecolor='lightgray',
            linewidth=2
        )
    )
    return fig

# === 5. Initial chart
chart_fig = generate_chart(selected_field)






# === 6. Update function for dropdown
def update_chart(state):
    state.chart_fig = generate_chart(state.selected_field)

# === 7. GUI layout
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("## Vad väljer studenterna? En titt på trender inom yrkeshögskolan (2019–2024)", mode="md")

        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card") as column_chart:
                tgb.chart(figure="{chart_fig}", mode="plotly")

            with tgb.part(class_name="card") as column_filters:
                tgb.text("#### Välj utbildningsområde", mode="md")
                tgb.selector(
                    value="{selected_field}",
                    lov=utb_list,
                    dropdown=True,
                    on_change=update_chart,
                    width="90%"
                )

        #with tgb.part(class_name="card"):
         #   tgb.text("## Rådata för alla utbildningsområden", mode="md")
          #  for utb in utb_list:
           #     tgb.text(f"### {utb}", mode="md")
               # tgb.table(f"{{all_tables['{utb}']}}")

        with tgb.part(class_name="card"):

            tgb.text("## Rådata", mode="md")
            tgb.table("{df_2024}")

# === 8. Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8050)
