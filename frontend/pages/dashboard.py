import taipy.gui.builder as tgb
from backend.data_processing import  long_df, utb_list, df_2024 , chart_fig, selected_field
from backend.updates import update_chart
from taipy.gui.builder import page



with tgb.Page() as dashboard_page:
    
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
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

    __all__ = ["dashboard_page"]


