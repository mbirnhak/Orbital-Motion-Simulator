#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:32:29 2024

@author: MattBirnhak
"""

import numpy as np

class Planet():
    """
    Planet class
    """
    def __init__(self, name, mass, orbit, colour):
        "Intiializes all values for each planet in the solar system"
        self.name = name.capitalize()
        self.m = mass
        self.orbit = orbit
        self.c = colour
        self.r = np.array([orbit, 0.0])
        self.r_prev = np.array([0.0, 0.0])
        self.v = np.array([0.0, 0.0])
        self.a_prev = np.array([0.0, 0.0])
        self.a_curr = np.array([0.0, 0.0])
        self.a_next = np.array([0.0, 0.0])
        self.years = 0