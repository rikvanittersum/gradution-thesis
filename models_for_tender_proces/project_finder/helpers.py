# Bibliotheken voor Nederlandse stopwoordnen en tokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Functie voor het omzetten en bewerken van kolommen in een excel bestand.
def csv_naar_dataframe():

    # openen van excel bestand en laden tekens en stopwoorden voor bewerken van de eis teksten
    tekst = open("eisen_en_referenties.csv", "r")
    stop_words = stopwords.words('dutch')
    punctuations = ['(', ')', ':', '[', ']', ',', '.', '-', '&', '?']

    # Lijsten voor bewerken van data uit Excel bestand.
    lijsten = []
    toevoegen = []

    # Het excel bestand is een tekstbestand, de werkelijke data wordt gescheiden door een getla gevolgd door een ";".
    # Er moet geitereerd worden over de regels, maar soms is wordt naar de volegdne regel gegaan omdat de eis te lang
    # is. Het programma moet deze pas stoppen met tekst toevoegen aan de eis als de werkelijke volgende eis is begonnen.
    for line in tekst:

        # Itereren over regels en pas als een nieuwe eis met referentie begint ophouden met toevoegen tekst aan eis.
        if line[0].isdigit() and line[1] == ";" or line[0].isdigit() and line[1].isdigit() and line[2] == ";":
            lijsten.append(toevoegen)
            toevoegen = []
            toevoegen.append(line.rstrip())
        else:
            toevoegen.append(line.rstrip())

    # Lijsten voor bewerking
    nieuwe_lijst = []
    laatste = []

    # Itereren over lijsten, per lijst delen van zinnen samenvoegen en hoofdletters om te zetten naar lage letters.
    for item in lijsten:
        zin = ("".join(item))
        nieuwe_lijst.append(zin.lower())

    # Eerste lege lijst verwijderen
    nieuwe_lijst.pop(0)

    # laatste verschoning van de lijst
    for item in nieuwe_lijst:
        tokens = word_tokenize(item)
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
        joe =  (" ".join(keywords))
        laatste.append(joe)

    # Lijsten waarin de kolomen komen
    kolom1= []
    kolom2 = []

    # het nummer van de referentie en de bijbehorende eis worden nu gesplitst.
    for item in nieuwe_lijst:
        a,b, *rest = item.split(";")
        for item in rest:
            b += item
        kolom1.append(a)
        kolom2.append(b)

    return kolom1, kolom2


def referentie_bij_nr():
    lijst_met_referenties = ["Ombouw N261 Tilburg-Waalwijk",
    "Optimaliseren aansluiting 10 A6 Lelystad",
    "Trajectaanpak N201 fase 3 Hoofddorp"
    "Rioolvervanging Veldstraat-Provinciewijk Deurne",
    "Fase 1 Verde Vista Meerburg, Zoeterwoude",
    "Vervangen asfaltverharding Handelsveem Sardinieweg",
    "Corsicaweg, Amsterdam",
    "blauwe berg",
    "Herinrichting Lange Nieuwstraat Ijmuiden",
    "lander",
    "N509 Herinrichting / Groot onderhoud",
    "Vervangen riool Torensloot Wormer",
    "windpark netterden",
    "Haags startstation",
    "Onderdoorgang spoorzone ede",
    "Woonrijp maken De Romp Noordoost  Boekelermeer",
    "Bouwrijp maken Kloosterveste Oostzijde",
    "Bravo 6A en 6B",
    "Aanleg Zuidelijke Randweg Borne",
    "Reconstructie Laan 1940 – 1945, Maassluis",
    "Offshore Terminal Rotterdam",
    "Vernieuwing Leidsebrug Amsterdam",
    "Aanleg 4 ecoducten ",
    "Arnhem Centraal Midden",
    "Raamovereenkomst Stationsgebied Alkmaar",
    "woonrijp maken De Buitenhagen te Schijndel",
    "Ontwerp en realisatie vna herinrichting N208 Hillegom",
    "OV SAAL Zuidtak Oost, Amsterdam",
    "Verbreding A4 Burgerveen-Leiden",
    "Verdubbeling Zutphensestraat, Apeldoorn",
    "Herinrichting Ureterpvallaat, Drachten",
    "Bouwrijp maken Vervoersknooppunt Bleizo, Zoetermeer",
    "Sontbrug Groningen",
    "n33 Assen-zuidbroek",
    "Fietsparkeergarage Mahlerplein",
    "Verhogen trambrug Breda"]

    lijst = list()
    for x, y in enumerate(lijst_met_referenties):
        lijst.append((x, y))
    referentie_met_nr = dict(lijst)

    return referentie_met_nr


