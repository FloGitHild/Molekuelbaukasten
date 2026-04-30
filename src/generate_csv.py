#!/usr/bin/env python3
"""
Comprehensive CSV generator for 34 main-group elements H..Xe.
Note: This initial version creates a master CSV and per-element placeholder CSVs.
Further detailed bonding-geometry data can be filled later, as data gathering progresses.
"""
import csv
import os

ELEMENTS = [
    "H","He","Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar",
    "K","Ca","Ga","Ge","As","Se","Br","Kr",
    "Rb","Sr","In","Sn","Sb","Te","I","Xe"
]

# Structured, non-exotic binding data per element (typical valence patterns in neutral compounds).
# Each entry is a list of tuples: (binding_type, description, geometry, hybridization, example)
BINDINGS_MAP = {
    "H": [("covalent","1 covalent bond (H-H in H2)","linear","s","H2")],
    "He": [],
    "Li": [("ionic","1 ionic bond (Li+ salts)","-","-","LiCl")],
    "Be": [
        ("covalent","2 covalent bonds (BeCl2)","linear","sp","BeCl2"),
        ("coordinative","2–4 coordination in complexes (Be(H2O)4)2+ typical","tetrahedral","sp3","Be(H2O)4]2+")
    ],
    "B": [("covalent","3 covalent bonds (BF3) Electro deficiency in B compounds","trigonal planar","sp2","BF3")],
    "C": [
        ("covalent","4 covalent (sp3) tetrahedral like CH4","tetrahedral","sp3","CH4"),
        ("covalent","2 covalent with double bonds (sp2) like CO2 or H2C=O","linear or trig planar","sp2","CO2"),
        ("covalent","2 double bonds (sp) like C2H2 or CO2 in cumulatives","linear","sp","C2H2")
    ],
    "N": [
        ("covalent","3 covalent + 1 lone pair (NH3)","pyramidal","sp3","NH3"),
        ("covalent","1 triple + 0 lone pairs (N2)","linear","sp","N2"),
        ("covalent","2 covalent + 1 double (NO2⁻)","trigonal planar oder bent","sp2","NO2-"),
        ("coordinative","donor in complexes (NH3→AlCl3)","tetrahedral","sp3","NH3 to AlCl3")
    ],
    "O": [
        ("covalent","2 covalent + 2 lone pairs (H2O)","bent","sp3","H2O"),
        ("covalent","1 double (C=O) in carbonyl", "trigonal planar","sp2","H2C=O"),
        ("covalent","2 double (O=O in CO2 per O)","linear","sp","O=O"),
        ("koordinativ","donor in H3O+ or metal-ligand","trigonal pyramidal","sp3","H3O+ or metal complex")
    ],
    "F": [("covalent","1 covalent (HF, CF4)","linear","s","HF"),("koord_koordinativ","1 donor in complexes","-","-","F-bridges in HF…")],
    "Ne": [],
    "Na": [("ionic","1 ionic bond (Na+ salts)","-","-","NaCl")],
    "Mg": [
        ("ionic","2 ionic bonds (Mg2+ in salts)","-","-","MgCl2"),
        ("koordinativ","6-coordination in hydrated complexes (Mg(H2O)6)2+","octahedral","-","Mg(H2O)6]2+")
    ],
    "Al": [
        ("covalent","3 covalent bonds (AlCl3)","trigonal planar","sp2","AlCl3"),
        ("koordinativ","4 covalent/coordinate (AlH4−, AlCl4−)","tetrahedral","sp3","AlH4-"),
        ("koordinativ","6-coordinate (Al(H2O)6)3+ typical","octahedral","sp3d2","[Al(H2O)6]3+")
    ],
    "Si": [
        ("covalent","4 covalent (SiR4) tetrahedral","tetrahedral","sp3","SiH4"),
        ("koordinativ","6-coordinate (SiF6)2-","octahedral","sp3d2","SiF6^2-"),
    ],
    "P": [
        ("covalent","3 covalent (PH3)","pyramidal","sp3","PH3"),
        ("covalent","5 covalent (PF5) TBP","TBP","sp3d","PF5"),
        ("koordinativ","6-coordinate (PF6−) octahedral","octahedral","sp3d2","PF6-"),
    ],
    "S": [
        ("covalent","2 covalent + 2 lone pairs (H2S)","bent","sp3","H2S"),
        ("covalent","4 covalent (SF4) seesaw","see-saw","sp3d","SF4"),
        ("covalent","6-coordinate (SF6) octahedral","octahedral","sp3d2","SF6"),
    ],
    "Cl": [
        ("covalent","1 covalent (HCl) or many covalent in organochlorines","linear or bent","sp3","HCl"),
        ("covalent","3 bonds (ClO3+) trigonal planar","trigonal planar","sp2","ClO3+"),
        ("covalent","4 bonds (ClO4−) tetrahedral","tetrahedral","sp3","ClO4-"),
        ("covalent","5 bonds (ClF5) square pyramidal","square pyramidal","sp3d","ClF5"),
        ("koordinativ","6-coordinate (ClF6−) octahedral","octahedral","sp3d2","ClF6-"),
    ],
    "Ar": [],
    "K": [("ionic","1 ionic bond (K+ salts)","-","-","KF"),("koordinativ","complexes reaching CN 4–6","tetrahedral to octahedral","-","K+ in complexes")],
    "Ca": [("ionic","2 ionic bonds (Ca2+)","-","-","CaCl2"),("koordinativ","CN 6–8 typical in hydrated complexes","octahedral","-","[Ca(H2O)6]2+" )],
    "Ga": [
        ("covalent","3 covalent (GaCl3)","trigonal planar","sp2","GaCl3"),
        ("covalent","4 covalent (GaCl4−)","tetrahedral","sp3","GaCl4-"),
        ("TBP","5 coordination (GaF5 TBP)","trigonal Bipyramidal","sp3d","GaF5"),
        ("oktaedrisch","6-coordinate (Ga(H2O)6)3+","octahedral","sp3d2","[Ga(H2O)6]3+"),
    ],
    "Ge": [
        ("covalent","4 covalent (GeCl4)","tetrahedral","sp3","GeCl4"),
        ("koordinativ","6-coordinate (GeF6)2−","octahedral","sp3d2","GeF6^2-"),
    ],
    "As": [
        ("covalent","3 covalent (AsCl3)","pyramidal","sp3","AsCl3"),
        ("covalent","5 covalent (AsF5) TBP","TBP","sp3d","AsF5"),
        ("koordinativ","4–6 coordination in oxoanions","tetra-/octahedral","sp3d2","AsO4^3- / AsO6^3-"),
    ],
    "Se": [
        ("covalent","2 covalent (SeCl2) bent","bent","sp3","SeCl2"),
        ("covalent","4 covalent (SeF4) seesaw","see-saw","sp3d","SeF4"),
        ("koordinativ","6-coordinate (SeF6) octahedral","octahedral","sp3d2","SeF6"),
    ],
    "Br": [
        ("covalent","1 covalent (HBr) or organobromines","linear or bend","sp3","HBr"),
        ("covalent","3 bonds (BrF3) T‑shaped","T‑shaped","sp3","BrF3"),
        ("covalent","5 bonds (BrF5) square pyramidal","square pyramidal","sp3d","BrF5"),
        ("koordinativ","6-coordinate (BrF6−) octahedral","octahedral","sp3d2","BrF6-"),
    ],
    "Kr": [],
    "Rb": [("ionic","1 ionic bond (Rb+ salts)","-","-","RbI")],
    "Sr": [("ionic","2 ionic bonds (Sr2+)","-","-","SrSO4")],
    "In": [
        ("covalent","3 covalent (InCl3)","trigonal planar","sp2","InCl3"),
        ("covalent","4 covalent (InCl4−)","tetrahedral","sp3","InCl4-"),
        ("koordinativ","5–6 coordination in complexes","pyramidal to octahedral","-","In(H2O)6+ etc"),
    ],
    "Sn": [
        ("covalent","4 covalent (SnCl4)","tetrahedral","sp3","SnCl4"),
        ("covalent","2 covalent (SnCl2) bent","bent","sp2?","SnCl2"),
    ],
    "Sb": [
        ("covalent","3 covalent (SbCl3)","pyramidal","sp3","SbCl3"),
        ("covalent","5 covalent (SbF5) TBP","TBP","sp3d","SbF5"),
        ("koordinativ","6-coordinate (SbF6−) octahedral","octahedral","sp3d2","SbF6-"),
    ],
    "Te": [
        ("covalent","2 covalent (TeCl2) bent","bent","sp3","TeCl2"),
        ("covalent","4 covalent (TeF4) seesaw","see-saw","sp3d","TeF4"),
        ("koordinativ","6-coordinate (TeF6) octahedral","octahedral","sp3d2","TeF6"),
    ],
    "I": [
        ("covalent","1 covalent (HI) or organoiodines","linear","p","HI"),
        ("covalent","3 bonds (IF3) T‑shaped","T‑shaped","sp3","IF3"),
        ("covalent","5 bonds (IF5) square pyramidal","square pyramidal","sp3d","IF5"),
        ("covalent","7 coordination (IF7) pentagonal bipyramidal","pentagonal bipyramidal","sp3d2","IF7"),
    ],
    "Xe": [
        ("covalent","2 covalent (XeF2) linear","linear","sp","XeF2"),
        ("covalent","4 covalent (XeF4) square planar","square planar","sp3d2","XeF4"),
        ("covalent","6 covalent (XeF6) octahedral","octahedral","sp3d2","XeF6"),
        ("koordinativ","4 coordinate (XeO4) tetrahedral","tetrahedral","sp3","XeO4"),
    ],
}

BASE_DIR = os.path.join("data")
PER_ELEMENT_DIR = os.path.join(BASE_DIR, "per_element")

def ensure_dirs():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(PER_ELEMENT_DIR, exist_ok=True)

def write_master_csv(path: str):
    # Master CSV with a high-level view for all 34 elements
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["element","diameter_mm","typical_bindings","notes"])
        for idx, sym in enumerate(ELEMENTS):
            diameter = 15 + idx  # grow by 1 mm per step, as requested
            # Build a compact summary of bindings for the master CSV
            bindings = BINDINGS_MAP.get(sym, [])
            if not bindings:
                summary = "none"
            else:
                parts = []
                for b in bindings:
                    parts.append(f"{b[0]}:{b[4]}")
                summary = "; ".join(parts)
            writer.writerow([sym, diameter, summary, "data not yet populated"])

def write_per_element_csv(symbol: str, index: int):
    # A minimal per-element CSV with placeholder bindings. More rows can be added later.
    path = os.path.join(PER_ELEMENT_DIR, f"{symbol}.csv")
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["binding_type","description","geometry","hybridization","example"])
        # Populate with the bindings map if available
        bindings = BINDINGS_MAP.get(symbol, [])
        if bindings:
            for b in bindings:
                writer.writerow([b[0], b[1], b[2], b[3], b[4]])
        else:
            writer.writerow(["none","no standard neutral covalent/ionic binding","-","-","-"]) 

def main():
    ensure_dirs()
    master_path = os.path.join(BASE_DIR, "all_elements.csv")
    write_master_csv(master_path)
    for i, sym in enumerate(ELEMENTS):
        write_per_element_csv(sym, i)
    print(f"CSVs generated under {BASE_DIR} and {PER_ELEMENT_DIR}")

if __name__ == "__main__":
    main()
