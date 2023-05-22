import pandas as pd
from animals import Animal, WEBSITE
import os, webbrowser

def watch_online(animal: Animal) -> None:
    """
    Opens the relative iucnredlist web page, when existing
    """
    if animal.is_listed:
        webbrowser.open(animal.url) # opens the website onto the default browser
    else:
        print(f"No page found on {WEBSITE}")


def watch_offline(animal: Animal) -> None:
    """
    Makes, saves and opens in a browser app a html page
    """
    page = os.path.join("pages", f"{animal.name.replace(' ', '-').lower()}.html")
    # On Windows -> "...\\pages\anguilla-anguilla.jpg"
    # On MacOS or Linux -> ".../pages/anguiilla-anguilla.jpg"
    bar = Animal.assessments.loc[animal.assessmentId]
    html_content = (
    f"<main style=\"background-color: #444444;"
    f"color: white; font-family: verdana;"
    f"text-align: justify;"
    f"margin: 25px; padding: 25px\">"

    f"<h1>{animal.vernacular}</h1>"
    f"<h2><i>{animal.name}</i></h2>"

    f"<h2>Taxonomy</h2>"
    f"<p><ul>"
    f"<li> Kingdom:  <b>{animal.kingdom}</b></li>"
    f"<li> Phylum:   <b>{animal.phylum}</b></li>"
    f"<li> Class:    <b>{animal.classis}</b></li>"
    f"<li> Order:    <b>{animal.order}</b></li>"
    f"<li> Family:   <b>{animal.family}</b></li>"
    f"<li> Genus:    <b>{animal.genus}</b></li></p></ul>"

    f"<h2>Assessment</h2>"
    f"<p><b>{animal.status}</b> ({animal.trend})</p>"
    f"{bar['rationale']}</p>"

    f"<h2>Geographic Range</h2>"
     f"<p>Realm: <b>{bar['realm']}</b></p>"
    f"<p>{bar['range']}</p>"

    f"<h2>Population</h2>"
    f"<p>{bar['population']}</p>"

    f"<h2>Habitat and Ecology</h2>"
    f"<p>System: <b>{bar['systems']}</b></p>"
    f"<p>{bar['habitat']}</p>"

    f"<h2>Threats</h2>"
    f"<p>{bar['threats']}</p>"

    f"<h2>Use and Trade</h2>"
    f"<p>{bar['useTrade']}</p>"

    f"<h2>Conservation Actions</h2>"
    f"<p>{bar['conservationActions']}</p>"

    f"</main>"
    )

    if not os.path.exists("pages"):
        os.makedirs("pages") # makes a folder named "pages" when not already existent

    with open(page, 'w', encoding = "utf-8") as output:
        # utf-8 encoding allows to encode special characters such as '≈'      
        output.write(html_content) # writes a html page

    webbrowser.open(page) #opens a local html page onto the default browser

# test library
if __name__ == "__main__":
    Animal.species = pd.read_csv("simple_summary.csv")
    Animal. names = pd.read_csv("common_names.csv")
    Animal.assessments = pd.read_csv("assessments.csv", index_col = 'assessmentId')
    animal = Animal('European eel')
    watch_online(animal)
    watch_offline(animal)