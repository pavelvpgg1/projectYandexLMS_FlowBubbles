import pygame
import math
from settings import WIDTH, HEIGHT

class Bullet:
    def __init__(self, start_pos, angle, speed, color, radius=4):
        self.x, self.y = start_pos
        self.angle = angle
        self.speed = speed
        self.vel_x = speed * math.cos(angle)
        self.vel_y = speed * math.sin(angle)
        self.color = color
        self.radius = radius
        self.alive = True
        self.penetration = False  # по умолчанию пуля не пробивает

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
