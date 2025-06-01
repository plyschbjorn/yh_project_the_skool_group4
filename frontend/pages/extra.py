import taipy.gui.builder as tgb
from utils.constants import DATA_DIRECTORY

with tgb.Page() as extra_page:
    with tgb.part(class_name="container card stack-large"):
        with tgb.part(class_name= "container card"):
            tgb.navbar()
        with tgb.layout(columns="1 1"):
            
            with tgb.part():
                tgb.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGhoZjl5bXpuc2VocnRrdXdpOW5sNDE1MzJha3NlZmZuOHFsZDdrNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jpEWg27oVLZ0xgvEgz/giphy.gif")
            with tgb.part():
                tgb.html("h2", "Summer Jazz Podcast Cocktail Music")
                tgb.html(
                    "audio",
                    src="../files/summer-jazz-podcast-cocktail-music-333890.mp3",  # 🔗 sökvägen relativ till .py-filen
                    controls="true",  # visar uppspelningsknappar
                    style="width:50%;"
                )

            tgb.text("## TACK FÖR OSS - Ha en fin sommar allihop ☀️ 😎", mode="md")
        
        with tgb.part():
            with tgb.html("marquee", behavior="scroll", direction="left", scrollamount="10", style="color:black; font-size:24px;"):
                tgb.html(None, "Detta projekt skapades av Abdulazeez Stef, Eyoub Beraki Tesfamicael, Maryam Moghadasi och Thorbjörn P Steive")

        