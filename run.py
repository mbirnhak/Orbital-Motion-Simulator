#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 23:09:14 2024

@author: MattBirnhak
"""
import time
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from planet import Planet
from beeman import Solar_system
from euler import SolarEuler
        
class Animation:
    """"
    A class to animate the movement of the planets around the sun
    """
    def __init__(self, method, bodies, num_timesteps, dt, G):
        "Initialize either Euler or Beeman to animate"
        if method == 'B':
            self.S = Solar_system(bodies, num_timesteps, dt, G)
        elif method == 'E':
            self.S = SolarEuler(bodies, num_timesteps, dt, G)
        self.dt = dt
        
    def update(self, frame):
        "Update current animation positions and check for new year passed"
        positions = []
        positions,energy = self.S.simulate_one_timestep()
        
        if frame%1000 == 0: 
            print(f"Total Energy at time step {frame}: {energy}") # print energy every 1000 iterations
        
        self.S.orbital_period(frame)
        
        if self.S.alignment():
            print(f"{frame*self.dt} years")
            time.sleep(1)  # freeze for 1 seconds when aligned
        
        for i in range(0, len(positions)):
            self.patches[i].center = positions[i]
        return self.patches
        
    def animate(self):
        "Set up the figure and execute the animation"
        fig = plt.figure()
        ax = plt.axes()
        
        self.patches = []
        for i in range(0, len(self.S.bodies)):
            patch = plt.Circle((self.S.bodies[i].r[0], self.S.bodies[i].r[1]), 0.2, color=self.S.bodies[i].c, animated=True)
            ax.add_patch(patch)
            self.patches.append(patch)

        # Set plot limits
        ax.axis('scaled')
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 7)
        
        self.ani = FuncAnimation(fig, self.update, self.S.num_timesteps, repeat=True, interval=1, blit=True)
        plt.show()

def energy_comparison(bodies, num_timesteps, dt, G):
    "Runs both the Beeman and Direct Euler simulations and graphs total energy over time"
    Euler_bodies = deepcopy(bodies)
    Beeman_bodies = deepcopy(bodies)
    
    print("Running...") # show that method is running
    
    E = SolarEuler(Euler_bodies, num_timesteps, dt, G)
    y_euler = E.simulation()
    
    B = Solar_system(Beeman_bodies, num_timesteps, dt, G)
    y_beeman = B.simulation()
    
    time = np.arange(0, num_timesteps*dt, dt)
    
    
    plt.plot(time, y_beeman, label='Beeman', zorder=2)
    plt.plot(time, y_euler, label='Euler', zorder=1)
    plt.xlabel('Time (years)')
    plt.ylabel('Energy (J)')
    plt.title('Energy vs Time')
    plt.legend()
    plt.show()

def main():
    "Read in values from file, run simulation"
    filename = 'parameters-solar.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    values = []
    for line in lines:
        "only include lines that are not empty, and exclude comments in the input file after a space"
        if not line.startswith("#"):
            values.append(line.strip())
              
    num_timesteps = int(values[0])
    dt = float(values[1])
    G = float(values[2])
    
    bodies = []
    for i in range(3, len(values)-3, 4):
        name = values[i]
        mass = float(values[i+1])
        orbit = float(values[i+2])
        colour = values[i+3]
        bodies.append(Planet(name, mass, orbit, colour))
    
    "Determine what experiments to run based on command line input"
    experiment = input("Enter 'S' for simulation', 'A' for Animation, or 'C' for Energy Comparison: ")
    if experiment == 'C':
        energy_comparison(bodies, num_timesteps, dt, G)
    
    else:
        method = input("Enter 'B' for Beeman or 'E' for Euler: ")
        if experiment == 'A':
            if method == 'B':
                A = Animation('B', bodies, num_timesteps, dt, G)
            elif method == 'E':
                A = Animation('E', bodies, num_timesteps, dt, G)
            A.animate()
                
        elif experiment == 'S':
            if method == 'B':
                S = Solar_system(bodies, num_timesteps, dt, G)
            elif method == 'E':
                S = SolarEuler(bodies, num_timesteps, dt, G)
            S.simulation()
    
    
if __name__ == "__main__":
    main()