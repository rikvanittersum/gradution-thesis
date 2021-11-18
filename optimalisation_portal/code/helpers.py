# Libraries voor constructies.
from anastruct.material.profile import HEA
from stabiliteit import stabiliteit_elementen

# Dicts met veiligheidsfactoren voor ULS en SLS.
combinaties_sterkte = [{'factor veranderlijk wind': 0, 'factor veranderlijk dak' : 1.35, 'factor permanent': 1.1},
               {'factor veranderlijk wind': 1.35, 'factor veranderlijk dak': 0, 'factor permanent': 0.9},
               {'factor veranderlijk wind': 0, 'factor veranderlijk dak': 0, 'factor permanent': 1.2}]

combinaties_bruikbaarheid = [{'factor veranderlijk wind': 1, 'factor veranderlijk dak': 0, 'factor permanent': .9},
                             {'factor veranderlijk wind': 0, 'factor veranderlijk dak': 1, 'factor permanent': .9}]


# Functie voor checken stabiliteit.
def stabiliteit_check(portaal, belasting_combi):

    elementen_constructie_krachten = portaal.krachten_en_verplaatsingen_elementen(belasting_combi)
    stabiliteit_krachten = stabiliteit_elementen(elementen_constructie_krachten, portaal)

    return stabiliteit_krachten

# Functie ter aanvulling op anastruct om maximaal absoluut moment te achterhalen.
def maximaal_moment(element_resultaat):
    momenten_waarden = ['Mmax', 'Mmin']
    maximale_momenten_elementen = []
    for element in element_resultaat:
        min_en_max_momenten = []
        for moment in momenten_waarden:
            min_en_max_momenten.append(abs(element.get(moment)))
        maximale_momenten_elementen.append(max(min_en_max_momenten))

    return maximale_momenten_elementen


# Functie om de combinaties van liggers en kolommen van portalen op basis van materiaalgebruik te rangschikken.
def combinaties_portaal():
    combinaties_zonder_rangschikking = {}
    combinaties = {}

    i = 0

    for balk in HEA:
        for kolom in HEA:
            combinaties_zonder_rangschikking[balk, kolom] = 2 * HEA.get(kolom)["G"] + HEA.get(balk)["G"]

    while bool(combinaties_zonder_rangschikking):

        joe = min(combinaties_zonder_rangschikking, key=combinaties_zonder_rangschikking.get)
        combinaties_zonder_rangschikking.pop(joe)
        combinaties[joe] = i
        i += 1

    return combinaties
joe = combinaties_portaal()
