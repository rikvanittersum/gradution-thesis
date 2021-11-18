# Librarie voor worteltrekken en een aantal constanten.
import math
E = 2.1E5
G = 81000
fy = 235

# Klasse stabiliteit. Maakt controle lokale stabiliteit mogelijk.
class stabiliteit_elementen:

    # Initiatie object met klasse stabiliteit. Alle relevante eigenschappen van de elementen opslaan.
    def __init__(self, elementen_constructie_krachten, portaal):

        # Krachten en momenten opelementen.
        normaal_krachten = elementen_constructie_krachten.get('normaalkracht')
        momenten = elementen_constructie_krachten.get('moment')
        self.kolom1_normaalkracht = abs(normaal_krachten [0])* 1E3
        self.ligger_normaalkracht = abs(normaal_krachten [1])* 1E3
        self.kolom2_normaalkracht = abs(normaal_krachten [2])* 1E3

        self.kolom1_moment = momenten [0]
        self.ligger_moment = momenten [1]
        self.kolom2_moment = momenten [2]

        # Mrd en Nrd worden in aparte functie bepaald en in het object opgeslagen.
        self.Mrd_kolommen = Mcr_bepalen(portaal)[0]
        self.Mrd_ligger = Mcr_bepalen(portaal)[1]

        self.Ncr_kolommen = Nrd_bepalen(portaal)[0]
        self.Ncr_ligger = Nrd_bepalen(portaal)[1]

    # Functie voor controle stabiliteit.
    def controle_stabiliteit(self):

        # med/mrd + ned/nrd controle uitvoeren voor elk element.
        kolom_1_stabiliteit = self.kolom1_normaalkracht  /self.Ncr_kolommen + self.kolom1_moment  /self.Mrd_kolommen
        ligger_stabiliteit = self.ligger_normaalkracht / self.Ncr_ligger + self.ligger_moment / self.Mrd_ligger
        kolom_2_stabiliteit = self.kolom2_normaalkracht / self.Ncr_kolommen + self.kolom2_moment / self.Mrd_kolommen

        # Resultata opslaan in  een lijst
        spanningen_combinatie = [kolom_1_stabiliteit, ligger_stabiliteit, kolom_2_stabiliteit]

        # Stabiliteit van alle elementen voldoet als het maximum van de controlles onder de 1 is.
        if max(spanningen_combinatie) < 1:
            return True
        # Anders voldoet de stabiliteit niet, element dat niet voeldoet teruggeven.
        else:
            return spanningen_combinatie.index(max(spanningen_combinatie))


# Functie voor bepalen Mcr. Volgt NEN-EN 1993-1-1 NB:Nb:2016.
def Mcr_bepalen(portaal):

    # Dict voor C1 en c2 ligger en kolommen. Volgt uit verschillende belastingwijzen uit NEN normen
    C1_en_C2 = {'ligger': [2.3, - 1.55], 'kolom verdeeld': [1.68, - 0.78], 'kolompuntlast': [1.45, - 0.56]}

    S_Ligger = math.sqrt(E * portaal.Iw_ligger / (G * portaal.It_ligger))
    S_Kolommen = math.sqrt(E * portaal.Iw_kolommen/ (G * portaal.It_kolommen))

    # C1 en C2 bepalen voor ligger uit dict C1_en_C2
    C1, C2 = C1_en_C2.get('ligger')

    eerste = math.pi * C1
    tweede = math.sqrt(1 + (math.pi**2 * S_Ligger**2 / (portaal.overspanning *1000)**2) * (C2**2 + 1))
    derde = math.pi * C2 * S_Ligger / (portaal.overspanning * 1000)

    C_ligger = eerste * (tweede + derde)

    C1, C2 = C1_en_C2.get('kolompuntlast')

    eerste = math.pi * C1
    tweede = math.sqrt(1 + (math.pi**2 * S_Kolommen**2 / (portaal.hoogte *1000)**2) * (C2**2 + 1))
    derde = math.pi * C2 * S_Kolommen/ (portaal.hoogte * 1000)

    C_kolommen = eerste * (tweede + derde)

    k_red = 1

    Mcr_kolommen = k_red * (C_kolommen / (portaal.hoogte*1000)) * math.sqrt(E * portaal.Iz_kolommen * G * portaal.It_kolommen)
    Mcr_ligger = k_red * (C_ligger / (portaal.overspanning*1000)) * math.sqrt(E * portaal.Iz_ligger * G * portaal.It_ligger)

    lamda_lt_kolommen  = math.sqrt(portaal.W_kolommen * fy / Mcr_kolommen)
    lamda_lt_ligger = math.sqrt(portaal.W_ligger * fy / Mcr_ligger)

    oi_kolommen = 0.5 *(1 + 0.34 * (lamda_lt_kolommen - 0.2) + lamda_lt_kolommen**2)
    oi_ligger = 0.5 * (1 + 0.34 * (lamda_lt_ligger - 0.2) + lamda_lt_ligger**2)

    Xlt_kolommen = 1 / (oi_kolommen + math.sqrt(oi_kolommen**2 - lamda_lt_kolommen**2))
    Xlt_ligger = 1 / (oi_ligger + math.sqrt(oi_ligger ** 2 - lamda_lt_ligger ** 2))

    if Xlt_ligger > 1:
        Xlt_ligger = 1
    if Xlt_kolommen > 1:
        Xlt_kolommen = 1

    MbRd_kolommen = Xlt_kolommen * portaal.W_kolommen * fy / 1E6
    MbRd_ligger = Xlt_ligger * portaal.W_ligger * fy / 1E6

    return MbRd_kolommen, MbRd_ligger


# Functie voor bepalen Nrd. Volgt NEN-EN 1993-1-1 6.3.1.1.
def Nrd_bepalen(portaal):

    slankheid_1 = math.pi * math.sqrt(210000/fy)

    slankheid_kolommen = portaal.hoogte / math.sqrt(portaal.I_kolommen/portaal.A_kolommen)
    slankheid_ligger = portaal.overspanning / math.sqrt(portaal.I_ligger / portaal.A_ligger)

    slankheid_kolommen = slankheid_kolommen/ slankheid_1
    slankheid_ligger = slankheid_ligger/ slankheid_1

    griekse_I_kolommen = .5 * (1 + .34 * (slankheid_kolommen - .2) + slankheid_kolommen**2)
    griekse_I_ligger = .5 * (1 + .34 * (slankheid_ligger - .2) + slankheid_ligger**2)

    reductiefactor_kolommen = 1 / (griekse_I_kolommen + math.sqrt(griekse_I_kolommen ** 2 - slankheid_kolommen ** 2))
    reductiefactor_ligger = 1 / (griekse_I_ligger + math.sqrt(griekse_I_ligger ** 2 - slankheid_ligger ** 2))

    Ncr_kolommen =  reductiefactor_kolommen * fy * portaal.A_kolommen
    Ncr_ligger = reductiefactor_ligger * fy * portaal.A_ligger

    return Ncr_kolommen, Ncr_ligger
