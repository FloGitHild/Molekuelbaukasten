#!/usr/bin/env python3
"""Minimal bond connector generator for magnet-based bindings.

Provides simple descriptors for single, double and triple bonds with two-ended magnets.
The actual STL generation will convert these descriptors to physical rods.
"""
from typing import List, Tuple

def bonds_lengths(single_mm=20.0, double_mm=12.0, triple_mm=8.0) -> List[Tuple[str, float]]:
    return [
        ("single", float(single_mm)),
        ("double", float(double_mm)),
        ("triple", float(triple_mm)),
    ]
