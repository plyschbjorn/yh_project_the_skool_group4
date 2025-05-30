from taipy.gui import Gui
import taipy.gui.builder as tgb


with tgb.Page() as home_page:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Välkommen till The SkoolBoard", mode="md")
            tgb.text(
                """
            The Skool’s egna dashboard för att utforska och förstå YH-data. Snabba insikter, smarta beslut – allt på ett ställe.
            """
            )
            

Gui(home_page).run(dark_mode=False, use_reloader=True, port=8080)