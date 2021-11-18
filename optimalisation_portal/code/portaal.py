# Import van noodzakelijke libraries voor constructie berekeningen en ene helpers functie voor bepalen absulte
# maximale moment.
from anastruct.material.profile import HEB, HEA
from anastruct.material.units import to_kN, to_kNm2
from anastruct.fem.system import SystemElements
from helpers import maximaal_moment

# Elasticiteits modules staal.
E = 210000

# Klasse portaal. hierin zitten de eiegnschappen van een portaal en functies om het te toetsen.
class portaal:

    # Functie om een object met klasse portaal aan te maken. Op basis van de eigenschappen en de profielen van de ligger
    # en kolommen worden voor berekening noodzakelijke eigenschappen gegenereerd. HEA balken geimporteerd uit Anastruct.
    def __init__(self, hoogte, overspanning, hoh, ligger_teller, kolommen_teller):
        self.hoogte = hoogte
        self.overspanning = overspanning
        self.hoh = hoh * 1.25

        self.liggerprofiel = list(HEA)[ligger_teller]
        self.kolomprofiel = list(HEA)[kolommen_teller]

        self.A_ligger = HEA[list(HEA)[ligger_teller]]["A"]
        self.I_ligger = HEA[list(HEA)[ligger_teller]]["Iy"]
        self.W_ligger = HEA[list(HEA)[ligger_teller]]["Wy"]
        self.It_ligger= HEA[list(HEA)[ligger_teller]]["It"] * 10
        self.Iw_ligger = HEA[list(HEA)[ligger_teller]]["Iw"]
        self.Iz_ligger = HEA[list(HEA)[ligger_teller]]["Iz"]

        self.I_kolommen = HEA[list(HEA)[kolommen_teller]]["Iy"]
        self.A_kolommen = HEA[list(HEA)[kolommen_teller]]["A"]
        self.W_kolommen = HEA[list(HEA)[kolommen_teller]]["Wy"]
        self.It_kolommen = HEA[list(HEA)[kolommen_teller]]["It"] * 10
        self.Iw_kolommen = HEA[list(HEA)[kolommen_teller]]["Iw"]
        self.Iz_kolommen = HEA[list(HEA)[kolommen_teller]]["Iz"]

        self.A_profiel_ligger = HEA[list(HEA)[ligger_teller]]["tw"] * \
                        (HEA[list(HEA)[ligger_teller]]["h"] - 2 *HEA[list(HEA)[ligger_teller]]["tf"])

        self.A_profiel_kolommen = HEA[list(HEA)[kolommen_teller]]["tw"] * \
                        (HEA[list(HEA)[kolommen_teller]]["h"] - 2 * HEA[list(HEA)[kolommen_teller]]["tf"])

        self.EG_profiel_ligger = HEA[list(HEA)[ligger_teller]]["G"] / 100
        self.EG_profiel_kolommen = HEA[list(HEA)[kolommen_teller]]["G"] / 100


    # Functie op de krachten en verplaatsingen op de constructie te bepalen. Neemt de eigenschappen van het portaal en
    # de van toepassing zijn de belastingcombinatie. Functie levert krachten van elementen ov verplaatsingen terug.
    def krachten_en_verplaatsingen_elementen(self, belastingcombi):

        # Belasting combi is een dict. Op deze wijze worden de van toepassing zijnde factoren bepaald.
        factor_wind = belastingcombi.get('factor veranderlijk wind')
        factor_permanent = belastingcombi.get('factor permanent')
        factor_dak_ver = belastingcombi.get('factor veranderlijk dak')

        # Opstarten van een constructie taak. Anastruct standaard opzet.
        ss = SystemElements()

        # Creeren elementen voor liggers en kolommen, met bijbehorende EA en EI.
        ss.add_element(location=[[0, 0], [0, self.hoogte]], EA=to_kN(E * self.A_kolommen),
                       EI=to_kNm2(E * self.I_kolommen))
        ss.add_element(location=[[0, self.hoogte], [self.overspanning, self.hoogte]], EA=to_kN(E * self.A_ligger),
                       EI=to_kNm2(E * self.I_ligger))
        ss.add_element(location=[[self.overspanning, self.hoogte], [self.overspanning, 0]],
                       EA=to_kN(E * self.A_kolommen), EI=to_kNm2(E * self.I_kolommen))

        # Toevoegen verbindingen.
        ss.add_support_hinged(node_id=1)
        ss.add_support_hinged(node_id=4)

        # Veranderlijke windbelasting kolom.
        ss.q_load(q=- factor_wind * self.hoh, element_id=1)

        # Veranderlijke en permanente lasten ligger.
        ss.q_load(q=-factor_permanent * 2 * self.hoh - factor_permanent * self.EG_profiel_ligger - factor_dak_ver * 1.5
                    * self.hoh, element_id=2)

        # Vaste belastingen kolommen
        ss.point_load(node_id=2, Fz=- factor_permanent * self.EG_profiel_kolommen * self.hoogte)
        ss.point_load(node_id=3, Fz=- factor_permanent * self.EG_profiel_kolommen * self.hoogte)

        # Oplossen constructie. Onder elements worden resultaten opgeslagen, heeft de structuur van een dict.
        ss.solve()
        elements = ss.get_element_results()

        # Als de functie wordt aangeroepen voor de krachten op de elementen. Is te zien aan de factoren.
        if factor_wind is not 1 and factor_dak_ver is not 1:

            # Maatgevende krachten per element bepalen, die geranschikt worden opgeslagen in een lijst. De eerste kracht
            # in de lijst correspondeert met het eerste element van het portaal.
            moment = maximaal_moment(elements)
            dwarskracht = ss.get_element_result_range("shear")
            normaalkracht = ss.get_element_result_range("axial")

            # De krachten per element wordne nu in een dict opgeslagen. Dit ziet er als volgt uit:
            # {"dwarskracht": [25.0, 53.9, 7.8] etc.
            krachten_elementen = {"dwarskracht": dwarskracht, "normaalkracht": normaalkracht, "moment": moment}
            return krachten_elementen

        # Anders wordt de functie aangeroepen voor verplaatsingen.
        else:
            # Verkrijgen relatieve doorbuiging.
            element_doorbuiging = ss.get_element_results()
            element_doorbuiging = element_doorbuiging[1].get('wmin') / self.overspanning

            # Verkrijgen relatieve verplaatsing.
            knoop_verplaatsingen = ss.get_node_displacements()
            knoop_verplaatsingen = knoop_verplaatsingen[1][3] / self.hoogte

            return element_doorbuiging, knoop_verplaatsingen

    # Fucntie ter controle van verplaatsingen.
    def verplaatsingen_controle(self, belastingcombi):
        element_doorbuiging, knoop_verplaatsing = self.krachten_en_verplaatsingen_elementen(belastingcombi)

        # Als zowel doorbuiging als knoopverplaatisngen niet voldoen, bepalen welke realtief het meest belast
        # overbelast wordt.
        if element_doorbuiging > 1 / 250 and knoop_verplaatsing > 1 / 150:
            if element_doorbuiging / (1 / 250) > knoop_verplaatsing / (1 / 150):
                return 0
            else:
                return 1

        # Doorbuiging voldoet niet.
        if element_doorbuiging > 1 / 250:
            return 0

        # Knoop verplaatsingen voldoen niet.
        if knoop_verplaatsing > 1 / 150:
            return 1

        # Beide voldoen, return true.
        return True