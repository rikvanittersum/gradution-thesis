# Libraries importeren voor constructieve berekeningen, creeren Dataframe, willekeurig kiezen en HEA balk eigenschappen.
from anastruct.fem.system import SystemElements
from anastruct.material.profile import HEA
import random
from pandas import DataFrame

# Constanten voor uitrekenen oplegreactie en spanningen met Anastruct.
E = 210000
EA = 15000
EI = 5000

# Lijst voor het opslaan van eigenschappen ligger en het optimale profiel.
data = []

# 10 miljoen een ligger met verschillende eigenschappen optimaliseren
for i in range(1000000):
    print(i)
    # De eigenschappen van de balk worden willekeurig gekozen. De eigenschappne zijn de overspanning,
    # de afstand waarop de puntlast aangrijpt en de groote van de puntlast en de q-last. De willekeurig gekozen
    # eigenschappen liggen wel tussen bepaalde waardes en worden afgerong op 1 decimaal
    overspanning = round(random.uniform(0.1, 25), 1)
    afstand_puntlast = overspanning * round(random.uniform(0.1, 0.9), 1)
    puntlast = round(random.uniform(-2, -100), 1)
    qlast = round(random.uniform(-10, -40), 1)

    # De constructie bestaat uit 1 element, dus het traagheidsmoment en het oppervlakte van het profiel hebben geen
    # invloed op de oplegreacties ed. Vandaar dat de stijfehedn ed voor het gemak zo worden verklaard.
    ss = SystemElements(EA=EA, EI=EI)

    # Construeren van het element. het element wordt in twee delen opgedeeld omdat Anastruct geen puntlast op afstanden
    # tot knopen toe laat, maar alleen op knopen zelf.
    ss.add_element(location=[[0, 0], [afstand_puntlast, 0]])
    ss.add_element(location=[[afstand_puntlast, 0], [overspanning, 0]])

    # Toevoegen van opleggingen. Een vast scharnier en een rolscharnier. het systeem is statisch bepaald.
    ss.add_support_hinged(node_id=1)
    ss.add_support_roll(node_id=3)

    # Toevoegen van de lasten. De puntlast grijpt aan op de middelste knoop, een willekeurige afstand dus.
    ss.point_load(node_id=2, Fz=puntlast)
    ss.q_load(q=qlast, element_id=1)

    # Uitrekenen van de constructie. De resultaten worden opgeslagen onder resultaten.
    ss.solve()
    resultaat = ss.get_element_results()

    # Lijst om de maximale momenten in op te slaan. Daarna itereren over de elementen en de maximale momenten opslaan.
    momenten = []
    for element in resultaat:
        momenten.append(element['Mmin'])

    # Ittereren over alle HEA balken.
    for balk in HEA:

        # Weerstandsmoment van de balk verkrijgen.
        Wy = HEA[balk]["Wy"]

        # De uniti check wordt uitgevoerd. Med/Mcr.
        UC = (momenten[0] * 1000000) / (- Wy * 235)

        # Als de Unity Check lager is dan 1, voldoet de balk. Dit is de optimale balk voor deze ligger, en de
        # eigenschappen en het optimum worden opgeslagen in de lijst data. De iteratie wordt afgebroken door break,
        # omdat het optimum al is gevonden. Een nieuwe ligger kan worden geoptimaliseerd.
        if UC < 1:
            data.append([overspanning, qlast * - 1, puntlast * -1, afstand_puntlast, list(HEA).index(balk)])
            break

# Van de opgeslagen data wordt nu een dataframe gemaakt zodat het geschikt is voor een ML model. het wordt opgeslagen
# als een pickle.
df = DataFrame.from_records(data, columns=['Overspanning', 'q-last', 'puntlast', 'afstand puntlast', 'HEA profiel nr.'])
df.to_pickle("data_verschuivende_10_mil")
