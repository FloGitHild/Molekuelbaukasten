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
            # Placeholder: detailed binding data to be populated later
            writer.writerow([sym, diameter, "to be filled", "data not yet populated"])

def write_per_element_csv(symbol: str, index: int):
    # A minimal per-element CSV with placeholder bindings. More rows can be added later.
    path = os.path.join(PER_ELEMENT_DIR, f"{symbol}.csv")
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["binding_type","description","geometry","hybridization","example"])
        # Placeholder row - to be expanded with actual bonding geometries
        writer.writerow(["to_be_defined","placeholder for element data","-","-","-"])

def main():
    ensure_dirs()
    master_path = os.path.join(BASE_DIR, "all_elements.csv")
    write_master_csv(master_path)
    for i, sym in enumerate(ELEMENTS):
        write_per_element_csv(sym, i)
    print(f"CSVs generated under {BASE_DIR} and {PER_ELEMENT_DIR}")

if __name__ == "__main__":
    main()
