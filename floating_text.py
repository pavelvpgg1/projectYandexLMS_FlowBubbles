import pygame


class DamageText:
    def __init__(self, text, pos, duration=1000):
        self.text = text
        self.pos = list(pos)
        self.duration = duration  # время жизни в мс
        self.start_time = pygame.time.get_ticks()
        self.alpha = 255
        self.font = pygame.font.SysFont(None, 24)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > self.duration:
            return False
        self.pos[1] -= 0.5  # плавное перемещение вверх
        self.alpha = max(0, 255 - int(255 * (elapsed / self.duration)))
        return True

    def draw(self, screen):
        surf = self.font.render(self.text, True, (255, 0, 0))
        surf.set_alpha(self.alpha)
        screen.blit(surf, self.pos)
