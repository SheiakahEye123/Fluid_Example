import math
import random
import sys
from typing import List
from xmlrpc.client import boolean

import matplotlib.lines
import matplotlib.pyplot as plot
import matplotlib.pyplot as plt
import null as null

# Constants
GRAVITY_FORCE = -1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128
WALL_DAMP = 0.5
TD = 1
XOFFSET = 0
YOFFSET = 0
NUM_PARTICLES = 10
MAX_DISTANCE = 3
MIN_DISTANCE = 0.5
PRESSURE_COEFFICIENT = 0.25
maxCap = 1000


class Particle:
    def __init__(self, x_pos: float, y_pos: float):
        self.pressure = 0;
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_vel = 0.0
        self.y_vel = 0.0


class QuadTree:

    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float, particlesList: [], level: int):

        self.particlesList = particlesList
        self.ymax = ymax
        self.xmax = xmax
        self.ymin = ymin
        self.xmin = xmin

        self.level = level

    def split(self):
        if self.particlesList.size() > maxCap:
            northeast = QuadTree(self.xmin, self.xmax / 2, self.ymin, self.ymax / 2, [], self.level + 1)
            southeast = QuadTree(self.xmin, self.xmax / 2, self.ymin / 2, self.ymax, [], self.level + 1)
            northwest = QuadTree(self.xmin / 2, self.xmax, self.ymin, self.ymax / 2, [], self.level + 1)
            southwest = QuadTree(self.xmin / 2, self.xmax / 2, self.ymin / 2, self.ymax, [], self.level + 1)
            self.insertParticles(northeast, southeast, northwest, southwest)

    def insertParticles(self, ne, se, nw, sw):
        for _ in self.particlesList:
            if ne.xmin <= _.x_pos < ne.xmax and ne.ymin <= _.y_pos < ne.ymax:
                # noreast
                ne.particlesList.add(_)
            if se.xmin <= _.x_pos < se.xmax and se.ymin <= _.y_pos < se.ymax:
                # souteast
                se.particlesList.add(_)
            if nw.xmin <= _.x_pos < nw.xmax and nw.ymin <= _.y_pos < nw.ymax:
                # norwest
                nw.particlesList.add(_)
            if sw.xmin <= _.x_pos < sw.xmax and sw.ymin <= _.y_pos < sw.ymax:
                # southest
                se.particlesList.add(_)

        self.particlesList.clear()

        ne.split()
        se.split()
        nw.split()
        sw.split()




# Interactive Mode (Allow plots to be updated)
plot.ion()
# Allows the X button to work. Don't worry about how this works exactly unless you are interested
plot.gcf().canvas.mpl_connect('close_event', lambda event: sys.exit())


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


def update_particles(particles_list: List[Particle]):
    """
    Calculates density of particles
        Density is calculated by summing the relative distance of neighboring particles
    """

    for particle in particles_list:

        # Density is calculated by summing the relative distance of neighboring particles
        for particle_2 in particles_list:
            distance = math.hypot(
                (particle.x_pos - particle_2.x_pos), (particle.y_pos - particle_2.y_pos)
            )
            if particle != particle_2 and MIN_DISTANCE < distance < MAX_DISTANCE:
                # normal distance is between 0 and 1
                normal_distance = 1 - distance / MAX_DISTANCE
                pressure = normal_distance ** 2
                particle_2.y_vel += PRESSURE_COEFFICIENT * (pressure * (particle_2.y_pos - particle.y_pos));
                particle_2.x_vel += PRESSURE_COEFFICIENT * (pressure * (particle_2.x_pos - particle.x_pos));

        # Calculate the Force pushing on this particle
        force_x = 0;
        force_y = 0;
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

        baseQuad = QuadTree(0, 0, WORLD_WIDTH_PIXELS, WORLD_HEIGHT_PIXELS, particles_list, 0)
        baseQuad.insertParticles()


def main():
    particles_list = make_particles()

    # Update loop
    while True:
        draw(particles_list)
        update_particles(particles_list)


main()
