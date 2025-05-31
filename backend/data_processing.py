from pathlib import Path
import pandas as pd  
from utils.constants import DATA_DIRECTORY
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter





# === 1. Load and transform data ===
DATA_DIRECTORY = Path(__file__).parents[1] / "files"
df = pd.read_csv(DATA_DIRECTORY / "beviljade_platser_full_2019_2024.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

df_2024 = pd.read_excel(
    DATA_DIRECTORY / "2024_tabell3.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)
df_kön = pd.read_excel(DATA_DIRECTORY / "long_format_Cleaned_Data.xlsx")
df_filter_kön = pd.read_excel(DATA_DIRECTORY / "kön.xlsx", decimal=",")


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


# Clean numbers
# Initial states



def filter_df_indicator(df_kön, indicator="Antal studerande"):
    return df_kön.query("Indicator == @indicator").reset_index()
df_antal_studerande = filter_df_indicator(df_kön) 
def create_indicator_bar_image(df_kön, **options):
    fig, ax = plt.subplots(figsize=(8, 5))




    bars = ax.barh(df_kön["Year"], df_kön["Value"], color="#A5B9E6", edgecolor="white")


    ax.set_title("Ökande efterfrågan på yrkesutbildning(En tydlig tillväxttrend i YH-studier 2007–2024)", fontsize=13,loc="left", fontweight="bold", fontstyle="italic")
    ax.set_xlabel(options.get("ylabel", "Antal studerande"), fontsize=11, fontstyle="italic", labelpad=10)
    ax.set_ylabel(options.get("xlabel", "År"), fontsize=11, fontstyle="italic")
    ax.spines[["top", "right"]].set_visible(False) 
    ax.spines[["left", "bottom"]].set_linewidth(1.5)
    ax.spines[["left", "bottom"]].set_color("lightgray") 


    ax.annotate("", xy=(df_kön["Value"].iloc[-1], df_kön["Year"].iloc[-1]),    
        xytext=(df_kön["Value"].iloc[0]+50, df_kön["Year"].iloc[0]),
        textcoords='data',   
        arrowprops=dict(
            arrowstyle="->",
            color="darkblue",
            lw=1.5,
            connectionstyle="arc3,rad=-0.15",
             linestyle="dashed"
        ),
        fontsize=9,
        color="gray",
        ha="left",
        va="center"
    )
      
    ax.text(
        x=(df_kön["Value"].iloc[0] + df_kön["Value"].iloc[-1]) / 2.2,  
        y=(df_kön["Year"].iloc[0] + df_kön["Year"].iloc[-1]) / 2 - 0.009,        
        s="Fler studerande",
        fontsize=10,
        color="gray",
        rotation=40 
    )


    plt.figtext(0.5, -0.05, "Källa: Statistiska centralbyrån (SCB)", ha="center", fontsize=10, color="gray")
    ax.set_yticks(df_kön["Year"])
    ax.set_yticklabels(df_kön["Year"].astype(int))
    ax.tick_params(left=False, bottom=False)
    ax.tick_params(axis='y', labelsize=9, labelcolor="gray")
    ax.tick_params(axis='x', labelsize=10, labelcolor="gray")
    formatter = FuncFormatter(lambda x, pos: f"{int(x/1000)}K")
    ax.xaxis.set_major_formatter(formatter)
    plt.tight_layout()

    pathpng = Path(__file__).parents[1] / "public" / "bar_chart.png"
    

    
    plt.savefig(pathpng, bbox_inches="tight")
    plt.close()
    return str(pathpng)


#filter women men


# Clean numbers
df_clean = df_filter_kön.copy()
cols_to_clean = df_clean.columns[1:]
for col in cols_to_clean:
    df_clean[col] = df_clean[col].astype(str).str.replace(u'\xa0', '', regex=False)
    df_clean[col] = df_clean[col].str.replace(',', '.', regex=False)
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Extract indicators & years
året = list(map(str, df_clean.columns[1:]))
mainindic = df_clean["Unnamed: 0"][::3].tolist()  # Only main indicators

# Initial states
selected_year = året[0]
selected_indicator = mainindic[0]
filtered_value = ""

# Logic function to extract women/men percentages
def show_gender_distribution(indicator: str, year: str):
    indicator_rows = df_clean[df_clean["Unnamed: 0"] == indicator].index.tolist()
    if not indicator_rows:
        return "⛔ Indikatorn hittades inte."

    idx = indicator_rows[0]

    try:
        year_col = int(year) if int(year) in df_clean.columns else str(year)
        women = df_clean.iloc[idx + 1][year_col]
        men = df_clean.iloc[idx + 2][year_col]
    except (IndexError, KeyError):
        return f"⛔ Data för år {year} saknas eller har fel format."

    if pd.isna(women) or pd.isna(men):
        return f"⚠️ Fullständig data saknas för år {year}."

    return f"{indicator} år {year}:\n- 👩 Kvinnor: {women}%\n- 👨 Män: {men}%"













# === 5. Initial chart
chart_fig = generate_chart(selected_field)
bar_chart_image = create_indicator_bar_image(df_antal_studerande)
