#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:35:08 2024

@author: MattBirnhak
"""

import math
import numpy as np
from beeman import Solar_system
from numpy.linalg import norm

class SolarEuler(Solar_system):
    """
    Class to simulate movement of the planets around the sun using the Direct Euler method
    """
    def __init__(self, bodies, num_timesteps, dt, G):
        "Initializes an array of Planet() objects with all the planets of the solar system"
        self.bodies = bodies
        self.num_timesteps = num_timesteps
        self.dt = dt
        self.G = G
        
        "intiialize velocities relative to the sun"
        m_sun = self.bodies[0].m
        for i in range(1, len(self.bodies)):
            r12 = self.bodies[i].orbit
            v = math.sqrt((self.G*m_sun)/r12)
            self.bodies[i].v = np.array([0.0, v])
            
        self.accel()
        self.bodies[0].a_curr = np.array([0.0, 0.0])
        
    def accel(self):
        "Calculate and set next timesteps acceleration for all planets"
        for i in range(0, len(self.bodies)):
            a_temp = np.array([0.0, 0.0])
            for j in range(0, len(self.bodies)):
                if i == j: continue
                mj = self.bodies[j].m
                rj = self.bodies[j].r
                ri = self.bodies[i].r
                rji_vect = ri - rj
                rji_mag = norm(rji_vect)
                a_temp += (mj/(rji_mag ** 3)) * rji_vect
            self.bodies[i].a_curr = -self.G * a_temp
            
    def position(self):
        "Calculate the next position for all planets"
        for i in range(0, len(self.bodies)):
            r_curr = self.bodies[i].r
            v = self.bodies[i].v
            dt = self.dt
            r_next = r_curr + v*dt
            self.bodies[i].r = r_next
            
    def velocity(self):
        "Calculate the next velocity for all planets"
        for i in range(0, len(self.bodies)):
            v_curr = self.bodies[i].v
            a = self.bodies[i].a_curr
            dt = self.dt
            v_next = v_curr + a*dt
            self.bodies[i].v = v_next
            
    def simulate_one_timestep(self):
        "Simulate a single time step of planetary motion using Euler"
        self.position()
        self.velocity()
        self.accel()
        
        "Return positions for animation update"
        positions = [body.r for body in self.bodies]
        return positions, self.total_energy()
        
    def simulation(self):
        "Simulate the entire movement of the planets for 'self.num_timesteps' iterations"
        energy_array = []
        for i in range(0, self.num_timesteps):
            _, energy = self.simulate_one_timestep()
            energy_array.append(energy)
        return energy_array