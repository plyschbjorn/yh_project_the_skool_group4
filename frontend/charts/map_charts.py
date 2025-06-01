import numpy as np
import plotly.graph_objects as go

def create_choropleth_map(beviljade_df, region_codes_map, geojson, approved, total, year):
    log_approved = np.log1p(beviljade_df["Beviljade"])

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=region_codes_map,
            z=log_approved,
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            marker_opacity=0.9,
            marker_line_width=0.4,
            text=beviljade_df["Län"],
            customdata=beviljade_df["Beviljade"],
            hovertemplate="<b>%{text}</b><br>Beviljade utbildningar: %{customdata}<extra></extra>",
            showscale=False,
        )
    )

    fig.update_layout(
        title=dict(
            text=f"""
                <br>Antal beviljade kurser per län
                <br>inom YH i Sverige för omgång <b>{year}</b>
                <br>Ju mörkare färg, desto fler beviljade kurser
                <br><b>{approved}</b> av <b>{total}</b> ansökningar har godkänts
                <br>Beviljandegrad: <b>{approved/total*100:.0f}%</b>
            """,
            x=0.05, y=0.8, font=dict(size=13),
        ),
        mapbox=dict(style="white-bg", zoom=4.0, center=dict(lat=62.7, lon=14)),
        margin=dict(r=0, t=0, l=0, b=0),
        width=600,
        height=800,
        autosize=False,
        dragmode=False,
    )
    return fig