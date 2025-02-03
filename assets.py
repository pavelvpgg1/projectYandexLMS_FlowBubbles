import pygame
import os


def generate_assets():
    pygame.init()  # инициализируем для работы шрифтов
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Изображение для главного персонажа (смешное личико)
    player_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(player_img, (255, 200, 200), (20, 20), 20)
    pygame.draw.circle(player_img, (0, 0, 0), (13, 15), 3)
    pygame.draw.circle(player_img, (0, 0, 0), (27, 15), 3)
    pygame.draw.arc(player_img, (0, 0, 0), (10, 10, 20, 20), 3.14, 6.28, 2)
    pygame.image.save(player_img, os.path.join("assets", "player.png"))

    # Изображение для задачи (жёлтый кружок с буквой «З»)
    task_img = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(task_img, (255, 223, 0), (8, 8), 8)
    font = pygame.font.SysFont(None, 12)
    text_surf = font.render("З", True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(8, 8))
    task_img.blit(text_surf, text_rect)
    pygame.image.save(task_img, os.path.join("assets", "task.png"))

    # Изображение для дедлайна (красный монстр с буквой «Д»)
    deadline_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(deadline_img, (255, 0, 0), (15, 15), 15)
    font = pygame.font.SysFont(None, 18)
    text_surf = font.render("Д", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(15, 15))
    deadline_img.blit(text_surf, text_rect)
    pygame.image.save(deadline_img, os.path.join("assets", "deadline.png"))

    # Изображения оружия для уровней 1-4

    # Уровень 1: простой пистолет (как раньше)
    weapon1 = pygame.Surface((30, 10), pygame.SRCALPHA)
    pygame.draw.rect(weapon1, (0, 0, 0), (0, 0, 30, 10))
    pygame.draw.circle(weapon1, (150, 150, 150), (5, 5), 5)
    pygame.image.save(weapon1, os.path.join("assets", "weapon1.png"))

    # Уровень 2: дробовик (более массивный, с несколькими "стволами")
    weapon2 = pygame.Surface((40, 12), pygame.SRCALPHA)
    pygame.draw.rect(weapon2, (30, 30, 30), (0, 0, 40, 12))
    # Рисуем пару "стволов"
    pygame.draw.rect(weapon2, (80, 80, 80), (5, 2, 10, 8))
    pygame.draw.rect(weapon2, (80, 80, 80), (25, 2, 10, 8))
    pygame.image.save(weapon2, os.path.join("assets", "weapon2.png"))

    # Уровень 3: винтовка (длиннее, с прицелом)
    weapon3 = pygame.Surface((50, 14), pygame.SRCALPHA)
    pygame.draw.rect(weapon3, (0, 0, 0), (0, 0, 50, 14))
    pygame.draw.circle(weapon3, (200, 200, 200), (10, 7), 4)
    pygame.image.save(weapon3, os.path.join("assets", "weapon3.png"))

    # Уровень 4: снайперка (длинная и элегантная)
    weapon4 = pygame.Surface((70, 16), pygame.SRCALPHA)
    pygame.draw.rect(weapon4, (0, 0, 0), (0, 0, 70, 16))
    pygame.draw.circle(weapon4, (220, 220, 220), (15, 8), 5)
    pygame.image.save(weapon4, os.path.join("assets", "weapon4.png"))
