#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:32:29 2024

@author: MattBirnhak
"""

import math
import numpy as np
from numpy.linalg import norm

class Solar_system:
    """
    Class to simulate movement of the planets around the sun using the Beeman method
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
            
        "initialize accelerations"
        self.next_accel()
        for i in range(1, len(self.bodies)):
            self.bodies[i].a_curr = self.bodies[i].a_next
            self.bodies[i].a_prev = self.bodies[i].a_curr
            self.bodies[i].a_next = np.array([0.0, 0.0])    # reset next accel for time 0
        
      
    def update_accel(self):
        "Update previous and current accelerations"
        for i in range(0, len(self.bodies)):
            self.bodies[i].a_prev = self.bodies[i].a_curr
            self.bodies[i].a_curr = self.bodies[i].a_next
            
    def next_accel(self):
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
            self.bodies[i].a_next = -self.G * a_temp
            
    def position(self):
        "Calculate the next position for all planets"
        for i in range(0, len(self.bodies)):
            r_curr = self.bodies[i].r
            self.bodies[i].r_prev = r_curr    # Set previous position
            v_curr = self.bodies[i].v
            a_prev = self.bodies[i].a_prev
            a_curr = self.bodies[i].a_curr
            dt = self.dt
            r_next = r_curr + v_curr*dt + (1.0/6.0)*(4*a_curr - a_prev)*(dt ** 2)
            self.bodies[i].r = r_next
            
    def velocity(self):
        "Calculate the next velocity for all planets"
        for i in range(0, len(self.bodies)):
            v_curr = self.bodies[i].v
            a_prev = self.bodies[i].a_prev
            a_curr = self.bodies[i].a_curr
            a_next = self.bodies[i].a_next
            dt = self.dt
            v_next = v_curr + (1.0/6.0)*(2*a_next + 5*a_curr - a_prev)*dt
            self.bodies[i].v = v_next
    
    def ke(self):
        "Calculates the sum of kinectic energy for all planets"
        total_ke = 0
        for i in range(0, len(self.bodies)):
            m = self.bodies[i].m
            v = self.bodies[i].v
            total_ke += 0.5 * m * np.dot(v, v)
        return total_ke
    
    def pe(self):
        "Calculates the sum of potential energy for all planets"
        total_pe = 0
        for i in range(0, len(self.bodies) - 1):
            for j in range(i+1, len(self.bodies)):
                m1 = self.bodies[i].m
                r1 = self.bodies[i].r
                m2 = self.bodies[j].m
                r2 = self.bodies[j].r
                r12_vect = r2 - r1
                r12 = norm(r12_vect)
                total_pe -= (self.G * m1 * m2)/r12
        return total_pe
            
    def total_energy(self):
        "Adds the ke and pe to get total energy of the solar system"
        return self.ke() + self.pe()
        
    def simulate_one_timestep(self):
        "Simulate a single time step of planetary motion using Beeman"
        self.position()
        self.next_accel()
        self.velocity()
        self.update_accel()
        
        "Return positions for animation update"
        positions = []
        for i in range(0, len(self.bodies)):
            positions.append(self.bodies[i].r)
        return positions, self.total_energy()
    
    def simulation(self):
        "Simulate the entire movement of the planets for 'self.num_timesteps' iterations"
        energy_array = []
        for i in range(0, self.num_timesteps):
            _, energy = self.simulate_one_timestep()
            energy_array.append(energy)
            
            if i%1000 == 0: 
                print(f"Total Energy at time step {i}: {energy}") # print energy every 1000 iterations
            
            self.orbital_period(i)
            
            if self.alignment():
                print(f"{i*self.dt} years")
                
        return energy_array

    def new_year(self, planet):
        "Return true if the planet passes the +x axis"
        if (planet.r_prev[1] < 0.0) and (planet.r[1] >= 0.0): 
            planet.years += 1
            return True
        else: 
            return False
    
    def orbital_period(self, timestep):
        """
        Experiment 1: Orbital Periods
        
        Prints orbital period when a planet every new year
        """
        for i in range(0, len(self.bodies)):
            time = timestep*self.dt
            if self.new_year(self.bodies[i]):
                print(f"Orbital Period of {self.bodies[i].name}: {time/self.bodies[i].years: .2f} Earth Years")
                
    def alignment(self):
        """
        Experiment 4: Planetary Alignment
        
        Detects and prints out when all planets are within 5˚ of eachother
        """
        π = np.pi
        threshold = np.deg2rad(5) # Convert 5˚ threshold to radians
        aligned = True
        suns_y = self.bodies[0].r[1]  # get suns y component
        
        "Creates an array containing every planets angle from the +x-axis in range (0,2π)"
        angles = [(np.arctan2((body.r[1] - suns_y), body.r[0]) % (2*π)) for body in self.bodies]
            
        for i in range(1, len(self.bodies)-1):
            for j in range(i+1, len(self.bodies)):
                diff = abs(angles[i] - angles[j])
                if diff > threshold:
                    aligned = False   # if angle difference between 2 planets is >5˚ return false
                    break
            if not aligned:
                break
        if aligned: 
            print("Planets ARE aligned within 5˚")
            
        return aligned