from pathlib import Path
import pandas as pd  
from utils.constants import DATA_DIRECTORY
import plotly.express as px




# === 1. Load and transform data ===
DATA_DIRECTORY = Path(__file__).parents[1] / "files"
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
