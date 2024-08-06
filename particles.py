import random
import math
import pygame

class Particle:
    def __init__(self, x, y, radius, window_width, window_height):
        self.x = x
        self.y = y
        self.window_width = window_width
        self.window_height = window_height
        self.radius = radius
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.angle += 0.02
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        if self.x < 0:
            self.x = self.window_width
        elif self.x > self.window_width:
            self.x = 0

        if self.y < 0:
            self.y = self.window_height
        elif self.y > self.window_height:
            self.y = 0

    def draw(self, window):
        color = (255, 255, 255)
        pos = (int(self.x), int(self.y))
        radius = int(self.radius)
        pygame.draw.circle(window, color, pos, radius)

# Particle system class
class ParticleSystem:
    def __init__(self, window_width, window_height):
        self.particles = []
        self.window_width = window_width
        self.window_height = window_width

    def add_particle(self, x, y, radius):
        self.particles.append(Particle(x, y, radius, self.window_width, self.window_height))

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, window):
        for particle in self.particles:
            particle.draw(window)