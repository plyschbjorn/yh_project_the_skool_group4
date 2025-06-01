from taipy.gui import Gui
from frontend.pages.data import data_page
from frontend.pages.home import home_page
from frontend.pages.dashboard import dashboard_page
from frontend.pages.ansök_kurs_omgång import ansökningar
from frontend.pages.map import map_page, beviljade_df, choropleth_chart, selected_year
from frontend.pages.kpi import kpi_page
from frontend.pages.extra import extra_page

pages = {
    "home": home_page, "studerande": dashboard_page, "kurser": ansökningar, "karta": map_page, "kpi": kpi_page, "data": data_page, "_": extra_page
}       

if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/main.css").run(
        dark_mode=False,
        beviljade_df=beviljade_df, 
        choropleth_chart=choropleth_chart, 
        selected_year=selected_year, 
        use_reloader=True,
        port=8080
    )