import math
import random
import sys
from typing import List

import matplotlib.pyplot as plot
import matplotlib.pyplot as plt

# Constants
GRAVITY_FORCE = -1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128
WALL_DAMP = 1.1
TD = 0.1
XOFFSET = 10;
YOFFSET = 10;
NUM_PARTICLES = 1000
MAX_DISTANCE = 1.5;


class Particle:
    def __init__(self, x_pos: float, y_pos: float):
        self.pressure = 0;
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_vel = 0.0
        self.y_vel = 0.0


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

        density = 0.0
        # Density is calculated by summing the relative distance of neighboring particles
        for particle_2 in particles_list:
            distance = math.hypot(
                (particle.x_pos - particle_2.x_pos)
                + (particle.y_pos - particle_2.y_pos)
            )
            if particle != particle_2 and distance < MAX_DISTANCE:
                # normal distance is between 0 and 1
                normal_distance = 1 - distance / MAX_DISTANCE
                density += normal_distance ** 2
                particle_2.pressure += normal_distance ** 2

        # Calculate the Force pushing on this particle
        force_x = 1;
        force_y = 0;
        force_y += GRAVITY_FORCE

        # Calculate velocity from force

        # Move particle by the value of its velocity
        if particle.x_pos < 0:
            force_x -= (particle.x_pos - 0) * WALL_DAMP

        # Same thing for the right wall
        if particle.x_pos > WORLD_WIDTH_PIXELS:
            force_x -= (particle.x_pos - WORLD_WIDTH_PIXELS) * WALL_DAMP

        # Same thing but for the floor
        if particle.y_pos < 0:
            # We use SIM_W instead of BOTTOM here because otherwise particles are too low
            force_y -= particle.y_pos * WALL_DAMP

        particle.x_vel += force_x * TD
        particle.y_vel += force_y * TD
        particle.x_pos += particle.x_vel * TD
        particle.y_pos += particle.y_vel * TD


def main():
    particles_list = make_particles()

    # Update loop
    while True:
        draw(particles_list)
        update_particles(particles_list)

main()
