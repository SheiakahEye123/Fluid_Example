import math
import random
import sys
from typing import List
import numpy as np

import matplotlib.pyplot as plot

# Constants
GRAVITY_FORCE = -1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128
WALL_DAMP = 0.5
TD = 1
XOFFSET = 0
YOFFSET = 0
NUM_PARTICLES = 200
MAX_DISTANCE = 3
MIN_DISTANCE = 0.5
# PRESSURE_COEFFICIENT = 0.25
PRESSURE_COEFFICIENT = 1
maxCap = 10
VISCOSITY = 0.2


class ParticleList:
    def __init__(self):
        self.x_pos = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.y_pos = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.x_vel = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.y_vel = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.force_y = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.force_x = np.zeros(NUM_PARTICLES, dtype=np.float32)

    def update_particles(self):
        """
        Calculates density of particles
            Density is calculated by summing the relative distance of neighboring particles
        """
        #     # Density is calculated by summing the relative distance of neighboring particles
        #     for particle_2 in particles_list:

        for i in range(NUM_PARTICLES):
            distance = np.hypot((self.x_pos - self.x_pos[i]), (self.y_pos - self.y_pos[i]))

            close_enough = MIN_DISTANCE < distance[i] & distance[i] < MAX_DISTANCE

            normal_distance = 1 - distance / MAX_DISTANCE

            pressure = normal_distance ** 2

            pressurex = PRESSURE_COEFFICIENT * (pressure * (self.x_pos[i] - self.x_pos))
            pressurey = PRESSURE_COEFFICIENT * (pressure * (self.y_pos[i] - self.y_pos))

            viscosityx = VISCOSITY * math.pow(self.x_vel[i] - self.x_vel, 1) / distance
            viscosityy = VISCOSITY * math.pow(self.y_vel[i] - self.y_vel, 1) / distance

            self.force_y[i] += np.sum(pressurey[close_enough])
            self.force_x[i] += np.sum(pressurex[close_enough])

            self.force_y[i] += np.sum(viscosityy[close_enough])
            self.force_x[i] += np.sum(viscosityx[close_enough])

            # Calculate the Force pushing on this particle
            force_x = 0
            force_y = 0
            force_y += GRAVITY_FORCE

            # Calculate velocity from force

            # Move particle by the value of its velocity

            particle.x_vel += force_x * TD
            particle.y_vel += force_y * TD
            particle.x_vel *= 0.95
            particle.y_vel *= 0.95
            particle.x_pos += particle.x_vel * TD
            particle.y_pos += particle.y_vel * TD
            if particle.x_pos < 0:
                # force_x -= (particle.x_pos - 0) * WALL_DAMP
                particle.x_vel = 0.2
                particle.x_pos = XOFFSET
                # force_x = force_x * -1

            # Same thing for the right wall
            if particle.x_pos > WORLD_WIDTH_PIXELS:
                # force_x -= (particle.x_pos - WORLD_WIDTH_PIXELS) * WALL_DAMP
                particle.x_vel = -0.2
                particle.x_pos = WORLD_WIDTH_PIXELS - XOFFSET
                # force_x = force_x * -1

            # Same thing but for the floor
            if particle.y_pos <= 0:
                # We use SIM_W instead of BOTTOM here because otherwise particles are too low
                particle.y_vel = random.random() * 5
                particle.y_pos = YOFFSET
                # force_y = force_y * -1

            if particle.y_pos > WORLD_HEIGHT_PIXELS:
                # force_x -= (particle.x_pos - WORLD_WIDTH_PIXELS) * WALL_DAMP
                particle.y_vel = -0.2
                particle.y_pos = WORLD_HEIGHT_PIXELS - YOFFSET

    def draw(particles: List[Particle]):
        x_positions = [particle.x_pos for particle in particles]
        y_positions = [particle.y_pos for particle in particles]

        # Clear the plot
        plot.cla()
        # Draw each particle according to x_position and y_positions
        plot.scatter(x_positions, y_positions,
                     s=4,  # Each particle is 4px
                     c='b'  # Color them blue
                     )
        # Fix the x and y range of the plot (or else they'll change based on the data)
        plot.xlim(-XOFFSET, WORLD_WIDTH_PIXELS + XOFFSET)
        plot.ylim(-YOFFSET, WORLD_HEIGHT_PIXELS + YOFFSET)
        # Refresh with the new particles
        plot.pause(0.001)

    def make_particles() -> List[Particle]:
        # Spawn particles at random positions
        particles_list: List[Particle] = []

        for i in range(NUM_PARTICLES):
            new_particle = Particle(random.random() * WORLD_WIDTH_PIXELS,
                                    random.random() * WORLD_HEIGHT_PIXELS)
            particles_list.append(new_particle)

        return particles_list


class QuadTree:
    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float, particlesList: []):
        self.particlesList = particlesList
        self.ymax = ymax
        self.xmax = xmax
        self.ymin = ymin
        self.xmin = xmin
        self.northwest = None
        self.southwest = None
        self.southeast = None
        self.northeast = None

    def split(self):
        if self.northwest == None and self.particlesList.size() > maxCap:
            for _ in self.particlesList:
                if self.xmin < _.x_pos < self.xmax / 2:
                    _.add

    def insert(self, quadtree):
        for _ in self.particlesList:
            if quadtree.xmin <= _.x_pos < quadtree.xmax / 2 and quadtree.ymin <= _.y_pos < quadtree.ymax / 2:
                self.particlesList.add(_)


# Interactive Mode (Allow plots to be updated)
plot.ion()
# Allows the X button to work. Don't worry about how this works exactly unless you are interested
plot.gcf().canvas.mpl_connect('close_event', lambda event: sys.exit())


def main():
    particles_list = make_particles()

    # Update loop
    while True:
        draw(particles_list)
        update_particles(particles_list)


main()
