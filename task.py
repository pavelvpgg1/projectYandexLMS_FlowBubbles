import pygame
import random
import os
from settings import WIDTH, HEIGHT

ASSETS_PATH = os.path.join("assets", "task.png")

class Task:
    TASK_IMAGE_ORIG = None

    def __init__(self):
        if Task.TASK_IMAGE_ORIG is None:
            Task.TASK_IMAGE_ORIG = pygame.image.load(ASSETS_PATH).convert_alpha()
        self.radius = 8
        self.image = Task.TASK_IMAGE_ORIG
        self.update_image()
        self.reposition()

    def update_image(self):
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(Task.TASK_IMAGE_ORIG, (size, size))

    def draw(self, screen):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)

    def reposition(self):
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
