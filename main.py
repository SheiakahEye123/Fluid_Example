import math
import random
import sys
from typing import List

import numpy as np
import time

import matplotlib.pyplot as plot

# Constants
GRAVITY_FORCE = -0.1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128
WALL_DAMP = 0.5
TD = 1
XOFFSET = 0
YOFFSET = 3
NUM_PARTICLES = 500
MAX_DISTANCE = 6
MIN_DISTANCE = 0.5
PRESSURE_COEFFICIENT = 0.25
maxCap = 10
VISCOSITY = 0.005
BOUNCEBACK = 0.2
BOUNCEBACKX = 0.2
BELOWX = -5
BELOWY = -5
COLOR = 5
EMPTYONES = np.ones(NUM_PARTICLES,dtype=np.float32)

plot.ion()
# Allows the X button to work. Don't worry about how this works exactly unless you are interested
plot.gcf().canvas.mpl_connect('close_event', lambda event: sys.exit())


class ParticleList:
    def __init__(self):
        self.x_pos = np.random.random(NUM_PARTICLES) * WORLD_WIDTH_PIXELS
        self.y_pos = np.random.random(NUM_PARTICLES) * WORLD_HEIGHT_PIXELS
        self.x_vel = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.y_vel = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.force_y = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.force_x = np.zeros(NUM_PARTICLES, dtype=np.float32)

    def update_particles(self, sec, sleep):

        self.force_x = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.force_y = np.zeros(NUM_PARTICLES, dtype=np.float32)

        """
        Calculates density of particles
            Density is calculated by summing the relative distance of neighboring particles
        """
        #     # Density is calculated by summing the relative distance of neighboring particles

        for i in range(NUM_PARTICLES):
            distance = np.hypot((self.x_pos - self.x_pos[i]), (self.y_pos - self.y_pos[i]))

            close_enough = np.logical_and((MIN_DISTANCE < distance), (distance < MAX_DISTANCE))

            normal_distance = 1 - distance / MAX_DISTANCE

            pressure = normal_distance ** 2

            pressurex = PRESSURE_COEFFICIENT * (pressure * (self.x_pos[i] - self.x_pos))
            pressurey = PRESSURE_COEFFICIENT * (pressure * (self.y_pos[i] - self.y_pos))

            viscosityx = VISCOSITY * np.power(self.x_vel[i] - self.x_vel[close_enough], 2) / distance[close_enough]
            viscosityy = VISCOSITY * np.power(self.y_vel[i] - self.y_vel[close_enough], 2) / distance[close_enough]

            self.force_y[i] += np.sum(pressurey[close_enough])
            self.force_x[i] += np.sum(pressurex[close_enough])

            self.force_y[i] += np.sum(viscosityy)
            self.force_x[i] += np.sum(viscosityx)

            # Calculate the Force pushing on this particle

        below0X = self.x_pos < BELOWX
        aboveMaxX = self.x_pos > WORLD_WIDTH_PIXELS

        below0Y = self.y_pos <= BELOWY
        aboveMaxY = self.y_pos > WORLD_HEIGHT_PIXELS

        self.x_vel[aboveMaxX] = -BOUNCEBACKX
        self.x_pos[aboveMaxX] = WORLD_WIDTH_PIXELS - BELOWX
        self.x_vel[below0X] = BOUNCEBACKX
        self.x_pos[below0X] = -1

        self.y_vel[aboveMaxY] = -BOUNCEBACK
        self.y_pos[aboveMaxY] = WORLD_HEIGHT_PIXELS - BELOWY
        self.y_vel[below0Y] = BOUNCEBACK
        self.y_pos[below0Y] = -1

        self.force_y += GRAVITY_FORCE

        # Calculate velocity from force

        # Move particle by the value of its velocity

        self.x_vel += self.force_x * TD
        self.y_vel += self.force_y * TD

        self.x_vel *= 0.95
        self.y_vel *= 0.95

        self.x_pos += self.x_vel * TD
        self.y_pos += self.y_vel * TD


        if sleep:
            time.sleep(sec)

    def draw(self):
        # Clear the plot
        plot.cla()
        # Draw each particle according to x_position and y_positions
        plot.scatter(self.x_pos, self.y_pos,
                     s=30,  # Each particle is 4px
                     c=np.clip(np.stack([np.abs(self.force_x) * COLOR, np.abs(self.force_y) * COLOR, EMPTYONES * COLOR]).T,0,1)
                     )
        # Fix the x and y range of the plot (or else they'll change based on the data)
        plot.xlim(-XOFFSET, WORLD_WIDTH_PIXELS + XOFFSET)
        plot.ylim(-YOFFSET, WORLD_HEIGHT_PIXELS + YOFFSET)
        # Refresh with the new particles
        plot.pause(0.001)


# class QuadTree:
#     def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float, particlesList: []):
#         self.particlesList = particlesList
#         self.ymax = ymax
#         self.xmax = xmax
#         self.ymin = ymin
#         self.xmin = xmin
#         self.northwest = None
#         self.southwest = None
#         self.southeast = None
#         self.northeast = None
#
#     # def split(self):
#     #     if self.northwest is None and self.particlesList.size() > maxCap:
#     #         for i in range(self.particlesList):
#     #             if self.xmin < _.x_pos < self.xmax / 2:
#     #
#     #
#     # def insert(self, quadtree):
#     #     for _ in self.particlesList:
#     #         if quadtree.xmin <= _.x_pos < quadtree.xmax / 2 and quadtree.ymin <= _.y_pos < quadtree.ymax / 2:
#     #             self.particlesList.add(_)


# Interactive Mode (Allow plots to be updated


def main():
    particles = ParticleList()

    # Update loop
    while True:
        particles.draw()
        particles.update_particles(0.1, False)


main()
