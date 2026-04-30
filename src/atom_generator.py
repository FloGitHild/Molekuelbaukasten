#!/usr/bin/env python3
"""Minimal generator for a single 'super-atom' with all possible socket positions.

This is a lightweight scaffold that collects 3D positions for potential socket locations
around an atom. The actual 3D printing output (STL) will combine these positions with
the atom sphere, using the same unit scale as the rest of the project.
"""
from math import pi
from typing import List, Tuple

try:
    from .geometries import generate_positions
except Exception:
    # Fallback in case of import issues during initial runs
    def generate_positions(geom, dist=1.0):
        return [(0,0,dist)]

def build_super_atom(symbol: str, diameter_mm: float) -> dict:
    """Return a simple dictionary describing the super-atom with socket positions.
    The positions are relative to the atom center; these are not camera-ready STL output yet.
    """
    # Collect all representative socket directions (a union of several common geometries)
    dist_unit = diameter_mm * 0.4  # arbitrary scaling for socket distance
    geoms = ["linear","tetrahedral","trigonal planar","tbp","oktaedrisch","square planar"]
    positions: List[Tuple[float, float, float]] = []
    for g in geoms:
        for p in generate_positions(g, dist=dist_unit):
            positions.append(p)
    # Deduplicate approximately (by string)
    uniq = []
    seen = set()
    for p in positions:
        key = (round(p[0],4), round(p[1],4), round(p[2],4))
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return {
        "symbol": symbol,
        "diameter_mm": diameter_mm,
        "radius_mm": diameter_mm/2.0,
        "socket_positions": uniq,
    }
