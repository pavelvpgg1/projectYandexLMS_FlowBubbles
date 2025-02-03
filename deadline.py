import pygame
import random
import math
import os
from settings import WIDTH, HEIGHT

ASSETS_PATH = os.path.join("assets", "deadline.png")

class Deadline:
    DEADLINE_IMAGE_ORIG = None

    def __init__(self, spawn_pos=None):
        if Deadline.DEADLINE_IMAGE_ORIG is None:
            Deadline.DEADLINE_IMAGE_ORIG = pygame.image.load(ASSETS_PATH).convert_alpha()
        self.radius = 15
        self.speed = 1.5
        self.image = Deadline.DEADLINE_IMAGE_ORIG
        self.update_image()
        if spawn_pos is not None:
            angle = random.uniform(0, 2 * math.pi)
            # Если обычный моб – используем, например, расстояние 250–400
            distance = random.uniform(250, 400)
            self.x = spawn_pos[0] + distance * math.cos(angle)
            self.y = spawn_pos[1] + distance * math.sin(angle)
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        else:
            self.x = random.choice([0, WIDTH])
            self.y = random.randint(0, HEIGHT)

    def update_image(self):
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(Deadline.DEADLINE_IMAGE_ORIG, (size, size))
        # Добавляем случайную вариацию оттенка
        tint_options = [(255, 0, 0), (255, 165, 0), (128, 0, 128)]
        tint = tint_options[random.randint(0, len(tint_options)-1)]
        tint_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        tint_surface.fill(tint + (50,))  # лёгкая прозрачность
        self.image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance != 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)

# Новый класс БОСС
class Boss(Deadline):
    def __init__(self, spawn_pos=None):
        super().__init__(spawn_pos)
        self.radius = 40    # больше размер
        self.speed = 4      # быстрее
        self.update_image()

    def update_image(self):
        size = int(self.radius * 2)
        base = pygame.transform.scale(Deadline.DEADLINE_IMAGE_ORIG, (size, size))
        dark_overlay = pygame.Surface((size, size), pygame.SRCALPHA)
        dark_overlay.fill((50, 0, 0, 100))  # затемнение
        base.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.image = base
