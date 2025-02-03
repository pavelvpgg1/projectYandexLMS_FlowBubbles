import pygame
import os, math
from settings import WIDTH, HEIGHT, BLACK
from bullet import Bullet

ASSETS_PATH = os.path.join("assets", "player.png")


class Player:
    PLAYER_IMAGE_ORIG = None

    WEAPON_DATA = {
        1: {"fire_rate": 1000, "bullet_speed": 5, "bullet_count": 1, "spread": 0, "asset": "weapon1.png"},
        2: {"fire_rate": 1200, "bullet_speed": 5, "bullet_count": 5, "spread": 30, "asset": "weapon2.png"},
        3: {"fire_rate": 800, "bullet_speed": 7, "bullet_count": 1, "spread": 0, "asset": "weapon3.png"},
        4: {"fire_rate": 1500, "bullet_speed": 10, "bullet_count": 1, "spread": 0, "asset": "weapon4.png"}
    }

    def __init__(self):
        if Player.PLAYER_IMAGE_ORIG is None:
            Player.PLAYER_IMAGE_ORIG = pygame.image.load(ASSETS_PATH).convert_alpha()
        # Начинаем позицию по центру окна
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 20
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 1.5  # уменьшенная скорость
        self.score = 0
        self.hp = 100  # начальное здоровье
        self.image = Player.PLAYER_IMAGE_ORIG

        weapon_asset = os.path.join("assets", Player.WEAPON_DATA[1]["asset"])
        self.weapon_image_orig = pygame.image.load(weapon_asset).convert_alpha()
        self.weapon_image = self.weapon_image_orig

        self.update_image()

        self.weapon_level = 1
        self.last_shot_time = 0
        data = Player.WEAPON_DATA[self.weapon_level]
        self.weapon_fire_rate = data["fire_rate"]
        self.bullet_speed = data["bullet_speed"]
        self.bullet_count = data["bullet_count"]
        self.bullet_spread = data["spread"]
        self.bullet_color = BLACK
        self.bullet_radius = 4

        self.is_hit = False
        self.hit_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.vel_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x += self.speed
        if keys[pygame.K_UP]:
            self.vel_y -= self.speed
        if keys[pygame.K_DOWN]:
            self.vel_y += self.speed

        self.x += self.vel_x
        self.y += self.vel_y

        # Ограничиваем движение по стенам (в зависимости от текущего разрешения)
        from settings import WIDTH, HEIGHT  # обновлённые размеры
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

        self.vel_x *= 0.8
        self.vel_y *= 0.8

    def update_image(self):
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(Player.PLAYER_IMAGE_ORIG, (size, size))
        self.update_weapon_image()

    def update_weapon_image(self):
        width = int(self.radius * 1.5)
        height = int(self.radius * 0.7)
        self.weapon_image = pygame.transform.scale(self.weapon_image_orig, (width, height))

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        # Если игрок недавно получил удар, используем эффект мерцания
        if self.is_hit:
            tinted = self.image.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            base_sprite = tinted
        else:
            base_sprite = self.image

        # Наложение эффекта повреждения: чем ниже HP, тем сильнее красный оттенок
        damage_factor = 1 - (self.hp / 100)
        if damage_factor > 0:
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, int(150 * damage_factor)))
            base_sprite.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        screen.blit(base_sprite, rect)
        weapon_offset = (self.radius, self.radius // 2)
        weapon_rect = self.weapon_image.get_rect(
            center=(int(self.x + weapon_offset[0]), int(self.y + weapon_offset[1])))
        screen.blit(self.weapon_image, weapon_rect)
        self.draw_hp_bar(screen, rect)

    def draw_hp_bar(self, screen, player_rect):
        bar_width = player_rect.width
        bar_height = 5
        hp_percent = max(0, self.hp) / 100
        fill_width = int(bar_width * hp_percent)
        bar_x = player_rect.left
        bar_y = player_rect.top - bar_height - 2
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

    def update_hit(self):
        if self.is_hit and pygame.time.get_ticks() - self.hit_timer > 200:
            self.is_hit = False

    def grow(self, amount=2):
        self.radius += 1
        self.score += amount
        self.update_image()
        self.check_weapon_upgrade()

    def check_weapon_upgrade(self):
        new_level = self.weapon_level
        if self.score >= 500:
            new_level = 4
        elif self.score >= 100:
            new_level = 3
        elif self.score >= 10:
            new_level = 2
        if new_level != self.weapon_level:
            self.weapon_level = new_level
            data = Player.WEAPON_DATA[self.weapon_level]
            self.weapon_fire_rate = data["fire_rate"]
            self.bullet_speed = data["bullet_speed"]
            self.bullet_count = data["bullet_count"]
            self.bullet_spread = data["spread"]
            weapon_asset = os.path.join("assets", data["asset"])
            self.weapon_image_orig = pygame.image.load(weapon_asset).convert_alpha()
            self.update_weapon_image()
            print(f"Оружие улучшено до уровня {self.weapon_level}!")

    def auto_shoot(self, targets):
        current_time = pygame.time.get_ticks()
        bullets = []
        if current_time - self.last_shot_time >= self.weapon_fire_rate and targets:
            target = min(targets, key=lambda d: math.hypot(self.x - d.x, self.y - d.y))
            dx = target.x - self.x
            dy = target.y - self.y
            base_angle = math.atan2(dy, dx)
            count = self.bullet_count
            spread = math.radians(self.bullet_spread)
            if count == 1:
                angles = [base_angle]
            else:
                angles = []
                for i in range(count):
                    offset = spread * (i - (count - 1) / 2)
                    angles.append(base_angle + offset)
            for angle in angles:
                bullet = Bullet((self.x, self.y), angle, self.bullet_speed, self.bullet_color, self.bullet_radius)
                if self.weapon_level == 4:
                    bullet.penetration = True
                bullets.append(bullet)
            self.last_shot_time = current_time
        return bullets
