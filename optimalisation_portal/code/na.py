from anastruct.material.profile import HEB, HEA
from anastruct.material.units import to_kN, to_kNm2
from anastruct.fem.system import SystemElements

I_ligger = HEA[list(HEA)[11]]["Iy"]
I_kolommen = HEA[list(HEA)[0]]["Iy"]
print(I_ligger/I_kolommen)
A_ligger = HEA[list(HEA)[11]]["A"]
A_kolommen = HEA[list(HEA)[0]]["A"]

EG_profiel_ligger = HEA[list(HEA)[11]]["G"] / 100
EG_profiel_kolommen = HEA[list(HEA)[0]]["G"] / 100

E = 210000
hoogte = 4.7
overspanning = 8.0
ss = SystemElements()

ss.add_element(location=[[0, 0], [0, 4.7]], EA=to_kN(E * A_kolommen),
               EI=to_kNm2(E * I_kolommen))
ss.add_element(location=[[0, hoogte], [overspanning, hoogte]], EA=to_kN(E * A_ligger),
               EI=to_kNm2(E * I_ligger))
ss.add_element(location=[[overspanning, hoogte], [overspanning, 0]],
               EA=to_kN(E * A_kolommen), EI=to_kNm2(E * I_kolommen))

ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=4)
print(-1.1 * 2 * 5.6 * 1.25 - 1.1 * EG_profiel_ligger - 1.35 * 1.5 * 5.6 * 1.25)
ss.q_load(q=-1.1 * 2 * 5.6 * 1.25 - 1.1 * EG_profiel_ligger - 1.35 * 1.5 * 5.6 * 1.25, element_id=2)
ss.point_load(node_id=2, Fz=- 1.1 * EG_profiel_kolommen * 4.7)
ss.point_load(node_id=3, Fz=- 1.1 * EG_profiel_kolommen * 4.7)

ss.solve()
ss.show_axial_force()