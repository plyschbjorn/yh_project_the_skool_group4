import pandas as pd 
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from pathlib import Path

# === 1. Load and transform data ===
DATA_DIRECTORY = Path(__file__).parents[2] / "files"
df = pd.read_csv(DATA_DIRECTORY / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

long_df = df.melt(id_vars="Utbildningsområde", var_name="År", value_name="Beviljade")
long_df["År"] = long_df["År"].astype(int)

# === 2. Create list of utbildningsområden
utb_list = sorted(long_df["Utbildningsområde"].unique().tolist())
selected_field = utb_list[0]  # default value

# === 3. Chart generator function
def generate_chart(utb):
    filtered = long_df[long_df["Utbildningsområde"] == utb]
    fig = px.line(
        filtered,
        x="År",
        y="Beviljade",
        title=f"Beviljade platser för <b>{utb}</b>",
        line_shape="spline"
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

# === 4. Initial chart
chart_fig = generate_chart(selected_field)

# === 5. Update callback
def update_chart(state):
    state.chart_fig = generate_chart(state.selected_field)

# === 6. Build GUI
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("## Vad väljer studenterna? En titt på trender inom yrkeshögskolan (2019–2024)", mode="md")

        tgb.text("Välj utbildningsområde", mode="md")
        tgb.selector(
            value="{selected_field}",
            lov=utb_list,
            dropdown=True,
            on_change=update_chart,
            width="60%"
        )

        tgb.chart(figure="{chart_fig}", mode="plotly", width=800, height=400)

# === 7. Run GUI
Gui(page).run(dark_mode=False, use_reloader=True, port=8050)
