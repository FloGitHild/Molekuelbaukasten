#!/usr/bin/env python3
"""Lightweight geometry helpers for simple PV geometries around a central atom.

- Distances are in arbitrary units; real radii will be scaled in later steps.
- Returns list of 3D vectors (x,y,z) pointing to binding directions.
"""
import math

def deg2rad(d):
    return d * math.pi / 180.0

def linear_distance(n):
    # return n vectors for linear geometries along +/- z axis
    if n == 1:
        return [(0,0,1)]
    elif n == 2:
        return [(0,0,1),(0,0,-1)]
    else:
        # generic: distribute on z axis
        return [(0,0,1) for _ in range(n)]

def positions_linear(n, dist=1.0):
    base = linear_distance(n)
    return [(x*dist,y*dist,z*dist) for x,y,z in base]

def positions_tetrahedral(dist=1.0):
    s = (1/math.sqrt(3))
    dirs = [ ( 1,  1, 1), ( 1, -1,-1), (-1, 1,-1), (-1,-1, 1) ]
    return [(x*s*dist, y*s*dist, z*s*dist) for x,y,z in dirs]

def positions_trigonal_planar(dist=1.0):
    angles = [0, 120, 240]
    return [(math.cos(deg2rad(a))*dist, math.sin(deg2rad(a))*dist, 0.0) for a in angles]

def positions_tbp(dist=1.0):
    # trigonal bipyramidal: 3 equatorial + 2 axial
    equator = positions_trigonal_planar(dist)
    axial = [(0,0, dist), (0,0,-dist)]
    return equator + axial

def positions_okta(dist=1.0):
    # octahedral: 6 directions along +/- x/y/z
    return [ (1,0,0),( -1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1) ]

def positions_square_planar(dist=1.0):
    pts = [ (1,0,0),(0,1,0),(-1,0,0),(0,-1,0) ]
    return [(x*dist,y*dist,0) for x,y,z in pts for _ in [0] for z in [0]]

def positions_pyramidal(dist=1.0):
    # pyramid with 4 base points around a square and a apex; use tetrahedral directions as simple proxy
    return positions_tetrahedral(dist)

def generate_positions(geom, dist=1.0):
    geom = geom.lower()
    if geom == "linear":
        return positions_linear(2, dist)
    if geom in ("tetrahedral","tetraedrisch"):  # sp3 around central atom
        return positions_tetrahedral(dist)
    if geom == "trigonal planar":
        return positions_trigonal_planar(dist)
    if geom == "trigonal pyramid" or geom == "pyramidal":
        return positions_pyramidal(dist)
    if geom == "tbp" or geom == "trigonal bipyramidal":
        return positions_tbp(dist)
    if geom == "oktaedrisch" or geom == "octahedral":
        return positions_okta(dist)
    if geom == "square planar":
        return positions_square_planar(dist)
    if geom == "see-saw" or geom == "see saw":
        # approximate as TBP with one axial replaced; here reuse TBP as a placeholder
        return positions_tbp(dist)
    # default fallback
    return [(0,0,dist)]
