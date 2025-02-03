import random
import sys

import pygame

from assets import generate_assets
from deadline import Deadline, Boss
from floating_text import DamageText
from player import Player
from settings import FPS, BLUE, BLACK
from task import Task

# Глобальные настройки игры
game_settings = {
    "resolution": (1920, 1080),  # варианты до 1920x1080
    "brightness": 100,  # от 0 до 100 (яркость)
    "fullscreen": False  # полноэкранный режим (False - окно)
}


def draw_button(screen, text, center, font, bg_color=(200, 200, 200)):
    """
    Отрисовывает кнопку с заданным текстом на экране.

    :param screen: Объект экрана Pygame для отрисовки.
    :param text: Текст, который будет отображаться на кнопке.
    :param center: Кортеж (x, y) с координатами центра кнопки.
    :param font: Шрифт, используемый для отрисовки текста.
    :param bg_color: Цвет фона кнопки (по умолчанию (200,200,200)).
    :return: Прямоугольник (pygame. Rect), описывающий область кнопки.
    """
    button_text = font.render(text, True, BLACK)
    button_rect = button_text.get_rect(center=center)
    pygame.draw.rect(screen, bg_color, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    return button_rect


def settings_menu(screen, clock, font):
    """
    Отображает меню настроек, где можно выбрать разрешение экрана,
    изменить яркость и переключить полноэкранный режим.

    :param screen: Текущий экран для отрисовки меню.
    :param clock: Объект clock для контроля FPS.
    :param font: Шрифт для отрисовки текста.
    """
    resolutions = [(800, 600), (1024, 768), (1280, 720), (1600, 900), (1920, 1080)]
    current_res = game_settings["resolution"]
    brightness = game_settings["brightness"]
    fullscreen = game_settings["fullscreen"]

    running = True
    while running:
        screen.fill(BLUE)
        width, height = current_res
        title = font.render("Настройки", True, BLACK)
        screen.blit(title, ((width - title.get_width()) // 2, 50))

        res_text = font.render(f"Разрешение: {current_res[0]}x{current_res[1]}", True, BLACK)
        screen.blit(res_text, (width // 4, 150))
        bright_text = font.render(f"Яркость: {brightness}", True, BLACK)
        screen.blit(bright_text, (width // 4, 200))
        fs_text = font.render(f"Полноэкранный режим: {'ВКЛ' if fullscreen else 'ВЫКЛ'}", True, BLACK)
        screen.blit(fs_text, (width // 4, 250))

        res_up = draw_button(screen, "Разрешение +", (width * 3 // 4, 150), font)
        res_down = draw_button(screen, "Разрешение -", (width * 3 // 4 + 150, 150), font)
        bright_up = draw_button(screen, "Яркость +", (width * 3 // 4, 200), font)
        bright_down = draw_button(screen, "Яркость -", (width * 3 // 4 + 150, 200), font)
        fs_toggle = draw_button(screen, "Toggle Fullscreen", (width * 3 // 4, 250), font)
        back_button = draw_button(screen, "Назад", (width // 2, 350), font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if res_up.collidepoint(pos):
                    idx = resolutions.index(current_res)
                    current_res = resolutions[(idx + 1) % len(resolutions)]
                if res_down.collidepoint(pos):
                    idx = resolutions.index(current_res)
                    current_res = resolutions[(idx - 1) % len(resolutions)]
                if bright_up.collidepoint(pos):
                    brightness = min(100, brightness + 10)
                if bright_down.collidepoint(pos):
                    brightness = max(0, brightness - 10)
                if fs_toggle.collidepoint(pos):
                    fullscreen = not fullscreen
                if back_button.collidepoint(pos):
                    game_settings["resolution"] = current_res
                    game_settings["brightness"] = brightness
                    game_settings["fullscreen"] = fullscreen
                    return
        pygame.display.flip()
        clock.tick(FPS)


def pause_menu(screen, clock, font):
    """
    Отображает меню паузы во время игры. Здесь можно продолжить игру,
    зайти в настройки, вернуться в главное меню или выйти из игры.

    :param screen: Экран для отрисовки меню.
    :param clock: Объект clock для контроля FPS.
    :param font: Шрифт для отрисовки текста.
    """
    paused = True
    while paused:
        screen.fill(BLUE)
        res = game_settings["resolution"]
        title = font.render("Пауза", True, BLACK)
        screen.blit(title, (res[0] // 2 - title.get_width() // 2, 100))
        resume_btn = draw_button(screen, "Продолжить", (res[0] // 2, 200), font)
        settings_btn = draw_button(screen, "Настройки", (res[0] // 2, 300), font)
        mainmenu_btn = draw_button(screen, "Главное меню", (res[0] // 2, 400), font)
        exit_btn = draw_button(screen, "Выход", (res[0] // 2, 500), font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_btn.collidepoint(pos):
                    paused = False
                if settings_btn.collidepoint(pos):
                    settings_menu(screen, clock, font)
                    if game_settings["fullscreen"]:
                        screen = pygame.display.set_mode(game_settings["resolution"], pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(game_settings["resolution"])
                if mainmenu_btn.collidepoint(pos):
                    main_menu(screen, clock, font)
                    paused = False
                if exit_btn.collidepoint(pos):
                    pygame.quit();
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def main_menu(screen, clock, font):
    """
    Отображает главное меню игры с вариантами «Начать игру» и «Настройки».

    :param screen: Экран для отрисовки меню.
    :param clock: Объект clock для контроля FPS.
    :param font: Шрифт для отрисовки текста.
    """
    running = True
    while running:
        screen.fill(BLUE)
        res = game_settings["resolution"]
        title = font.render("Flow Bubbles", True, BLACK)
        screen.blit(title, (res[0] // 2 - title.get_width() // 2, 50))
        start_button = draw_button(screen, "Начать игру", (res[0] // 2, 200), font)
        settings_button = draw_button(screen, "Настройки", (res[0] // 2, 300), font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    return  # старт игры
                if settings_button.collidepoint(pos):
                    settings_menu(screen, clock, font)
                    if game_settings["fullscreen"]:
                        screen = pygame.display.set_mode(game_settings["resolution"], pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(game_settings["resolution"])
        pygame.display.flip()
        clock.tick(FPS)


def game_loop(screen, clock, font):
    """
    Основной игровой цикл. Здесь происходит обновление игрового состояния,
    обработка столкновений, спавн мобов и боссов, регенерация HP, а также отрисовка.

    :param screen: Экран, на котором происходит игра.
    :param clock: Объект clock для контроля FPS.
    :param font: Шрифт для отрисовки текста.
    """
    player = Player()
    task = Task()
    deadlines = [Deadline() for _ in range(3)]
    bullets = []
    damage_texts = []

    game_over = False
    restart_button_rect = None

    last_regen_time = pygame.time.get_ticks()
    mob_spawn_interval = 5000  # каждые 5 секунд спавн нового моба
    last_mob_spawn_time = pygame.time.get_ticks()

    # Основной цикл игры
    while True:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            # Обработка нажатия кнопки паузы (в правом верхнем углу)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pause_button_rect.collidepoint(pos):
                    pause_menu(screen, clock, font)
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button_rect and restart_button_rect.collidepoint(pos):
                    game_loop(screen, clock, font)
                    return

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update_hit()

            # Регенерация HP: каждые 1000 мс +1 hp (максимум 100)
            if current_time - last_regen_time >= 1000:
                player.hp = min(100, player.hp + 1)
                last_regen_time = current_time

            # Спавн мобов по таймеру
            if current_time - last_mob_spawn_time >= mob_spawn_interval:
                # 10% шанс спавна босса
                if random.random() < 0.1:
                    deadlines.append(Boss())
                else:
                    deadlines.append(Deadline())
                last_mob_spawn_time = current_time

            # Проверка столкновения с едой
            dx = player.x - task.x
            dy = player.y - task.y
            if (dx ** 2 + dy ** 2) ** 0.5 < player.radius + task.radius:
                player.grow()
                # При подборе еды восстанавливаем HP на 10 единиц
                player.hp = min(100, player.hp + 10)
                task.reposition()
                new_enemies_count = player.weapon_level * 3
                for i in range(new_enemies_count):
                    if random.random() < 0.1:
                        deadlines.append(Boss(spawn_pos=(player.x, player.y)))
                    else:
                        deadlines.append(Deadline(spawn_pos=(player.x, player.y)))

            new_bullets = player.auto_shoot(deadlines)
            bullets.extend(new_bullets)

            for deadline in deadlines[:]:
                deadline.update(player)
                dx = player.x - deadline.x
                dy = player.y - deadline.y
                if (dx ** 2 + dy ** 2) ** 0.5 < player.radius + deadline.radius:
                    player.hp -= 10
                    player.is_hit = True
                    player.hit_timer = current_time
                    damage_texts.append(DamageText("-10hp", (player.x, player.y - player.radius)))
                    deadlines.remove(deadline)
                    if player.hp <= 0:
                        game_over = True

            for bullet in bullets:
                bullet.update()
                for deadline in deadlines[:]:
                    dist = ((bullet.x - deadline.x) ** 2 + (bullet.y - deadline.y) ** 2) ** 0.5
                    if dist < bullet.radius + deadline.radius:
                        if not bullet.penetration:
                            bullet.alive = False
                            deadlines.remove(deadline)
                            break
                        else:
                            deadlines.remove(deadline)
            bullets = [b for b in bullets if b.alive]
            damage_texts = [dt for dt in damage_texts if dt.update()]

        # Отрисовка объектов
        screen.fill(BLUE)
        task.draw(screen)
        player.draw(screen)
        for deadline in deadlines:
            deadline.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for dt in damage_texts:
            dt.draw(screen)

        score_text = font.render(f"Score: {player.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        weapon_text = font.render(f"Уровень оружия: {player.weapon_level}", True, BLACK)
        screen.blit(weapon_text, (10, 40))
        hp_text = font.render(f"HP: {player.hp}", True, BLACK)
        screen.blit(hp_text, (10, 70))

        # Рисуем кнопку паузы в правом верхнем углу
        pause_button_rect = draw_button(screen, "Пауза", (game_settings["resolution"][0] - 70, 30), font,
                                        bg_color=(180, 180, 180))

        if game_over:
            res = game_settings["resolution"]
            over_text = font.render("GAME OVER", True, BLACK)
            screen.blit(over_text, (res[0] // 2 - over_text.get_width() // 2,
                                    res[1] // 2 - over_text.get_height() // 2))
            restart_button_rect = draw_button(screen, "Начать заново", (res[0] // 2, res[1] // 2 + 50), font)

        overlay = pygame.Surface(game_settings["resolution"])
        overlay.set_alpha(255 - int(255 * (game_settings["brightness"] / 100)))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.display.flip()


def main():
    """
    Главная функция, которая инициализирует игру, запускает главное меню и игровой цикл.
    """
    pygame.init()
    generate_assets()
    if game_settings["fullscreen"]:
        screen = pygame.display.set_mode(game_settings["resolution"], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(game_settings["resolution"])
    pygame.display.set_caption("Flow Bubbles: Мы едим задачи, а дедлайны нас гонят!")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    main_menu(screen, clock, font)
    # Обновляем глобальные размеры (если они используются в логике)
    import settings
    settings.WIDTH, settings.HEIGHT = game_settings["resolution"]
    game_loop(screen, clock, font)


if __name__ == "__main__":
    main()
