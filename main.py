
from frontend.pages.dashboard import page
from taipy.gui import Gui
from frontend.pages.data import data_page
from frontend.pages.home import home_page
from frontend.pages.dashboard import dashboard_page
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from frontend.pages.ansök_kurs_omgång import ansökningar, gui_data



pages = {
    "home": home_page, "kurs": ansökningar, "dashboard": dashboard_page , "data": data_page
}       



if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/style.css").run(
        port=8080,
        dark_mode=False,
        use_reloader=False
    )