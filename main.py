import random
import sys
from typing import List

import matplotlib.pyplot as plot
import matplotlib.pyplot as plt

# Constants
GRAVITY_FORCE = -1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128


class Particle:
    def __init__(self, x_pos: float, y_pos: float):
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
    plot.xlim(0, WORLD_WIDTH_PIXELS)
    plot.ylim(0, WORLD_HEIGHT_PIXELS)
    # Refresh with the new particles
    plot.pause(0.001)


def make_particles() -> List[Particle]:
    # Spawn particles at random positions
    NUM_PARTICLES = 100
    particles_list: List[Particle] = []

    for i in range(NUM_PARTICLES):
        new_particle = Particle(random.random() * WORLD_WIDTH_PIXELS,
                                random.random() * WORLD_HEIGHT_PIXELS)
        particles_list.append(new_particle)

    return particles_list

def update_particles(particles_list: List[Particle]):
    for particle in particles_list:

        # Calculate the Force pushing on this particle
        force_x = 0
        force_y = GRAVITY_FORCE

        # Calculate velocity from force
        particle.x_vel += force_x
        particle.y_vel += force_y

        # Move particle by the value of its velocity
        particle.x_pos += particle.x_vel
        particle.y_pos += particle.y_vel


def main():
    particles_list = make_particles()

    # Update loop
    while True:
        draw(particles_list)
        update_particles(particles_list)

main()
