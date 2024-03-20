import sys
import pygame
import random
from pygame import mixer

import database.sqlite
import formulario.form
import serial
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/spaceship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.speed = 6
        self.last_shot = pygame.time.get_ticks()
        self.score = 0

    def update(self):
        # Velocidad
        speed = 6
        cooldown = 100

        # Entradas por teclado
        keys = pygame.key.get_pressed()

        # Tiempo para espera del disparo
        time_now = pygame.time.get_ticks()

        # Movimiento del personaje
        self.keys_update(keys)  # Pasar keys como parámetro

        # Disparo
        self.shoot(keys, time_now, cooldown)  # Pasar keys, time_now y cooldown como parámetros

        # Dibujar barra de vida
        self.draw_health_bar()

        # Actualizar la máscara para que la colisión sea con los pixeles de color y no los transparentes del png
        self.mask = pygame.mask.from_surface(self.image)

    def keys_update(self, keys):
        """print(rawString.decode('UTF-8'))

        if rawString.decode('UTF-8') == 'd' and self.rect.right < screen_width:
            self.rect.x += self.speed
        if rawString.decode('UTF-8') == 'a' and self.rect.left > 0:
            self.rect.x -= self.speed"""


        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
    def shoot(self, keys, time_now, cooldown):
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            laser_fx.play()

    def draw_health_bar(self):
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (
                self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)),
                15))

        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
            return game_over

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update_score(self, points):
        self.score += points


aliens_eliminados = 0

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

        self.bullets_collisions()

    def bullets_collisions(self):
        global aliens_eliminados  # Declarar la variable global dentro de la función
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            explosion_fx.play()
            aliens_eliminados += 1  # Incrementar el contador global
            spaceship.update_score(20)

class Aliens(pygame.sprite.Sprite):
    speed = 0
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/alien" + str(random.randint(1, 5)) + ".png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.move_direction = 1
        self.speed = Aliens.speed

    def update(self):
        self.rect.x += self.move_direction * self.speed
        self.counter += self.speed
        if (abs(self.counter) > screen_width - 200 - 100 * cols):
            self.move_direction *= -1
            self.counter *= self.move_direction / self.counter
            self.rect.y += 20

    @classmethod
    def set_global_speed(cls, new_speed):
        cls.speed = new_speed

class Alien_Bullets(pygame.sprite.Sprite):
    speed = 2  # Atributo de clase para la velocidad inicial

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/alien_bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = Alien_Bullets.speed  # Usar el atributo de clase como valor inicial

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height: self.kill()
        self.bullet_collision()

    def bullet_collision(self):
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            spaceship.health_remaining -= 1
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            explosion_2_fx.play()

    @classmethod
    def set_global_speed(cls, new_speed):
        cls.speed = new_speed



class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"graphics/exp{num}.png").convert_alpha()
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))

            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(200 + (item * 100), 100 + (row * 70))
            alien_group.add(alien)

def alien_shoot(last_alien_shoot=pygame.time.get_ticks()):
    time_now = pygame.time.get_ticks()
    if time_now - last_alien_shoot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shoot = time_now

def menu():
    global level_1_rect, level_2_rect, level_3_rect
    level_1_rect = draw_text("LEVEL 1", font30, white, (screen_width / 2) - 200, screen_height / 2)
    level_2_rect = draw_text("LEVEL 2", font30, white, (screen_width / 2), screen_height / 2)
    level_3_rect = draw_text("LEVEL 3", font30, white, (screen_width / 2) + 200, screen_height / 2)

    if not can_access_level[1]:
        candado_1 = pygame.image.load("graphics/candado.png").convert_alpha()
        candado_1 = pygame.transform.scale_by(candado_1, 0.05)
        candado_1_rect = candado_1.get_rect(center=((screen_width / 2) + 50, (screen_height / 2) - 25))
        screen.blit(candado_1, (candado_1_rect))

    if not can_access_level[2]:
        candado_2 = pygame.image.load("graphics/candado.png")
        candado_2 = pygame.transform.scale_by(candado_2, 0.05)
        candado_2_rect = candado_2.get_rect(center=((screen_width / 2) + 250, (screen_height / 2) - 25))
        screen.blit(candado_2, (candado_2_rect))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect


def key_updates():
    global level, game_active, game_start, aliens_eliminados, game_over, game_inserted
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if level_1_rect.collidepoint(event.pos) and can_access_level[0]:
                level = 1
                game_active = True
            if level_2_rect.collidepoint(event.pos) and can_access_level[1]:
                level = 2
                game_active = True
                game_inserted = False
            if level_3_rect.collidepoint(event.pos) and can_access_level[2]:
                level = 3
                game_active = True
                game_inserted = False
            if not game_active:
                if volver_al_menu_rect.collidepoint(event.pos):
                    level = 0
                    game_start = 0
                    aliens_eliminados = 0

def display_score():
    draw_text(f"SCORE: {spaceship.score}", font30, white, (screen_width / 2), 20)


def alien_shoot(number_bullets=10):
    time_now = pygame.time.get_ticks()
    if (time_now - last_alien_shoot > alien_cooldown) and (len(alien_bullet_group) < number_bullets) and (len(alien_group) > 0):
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)

def game_end(game_finish, game_start):
    global volver_al_menu_rect, game_inserted

    for alien in alien_group.sprites():
        alien.kill()

    for bullet in bullet_group.sprites():
        bullet.kill()

    for bullet in alien_bullet_group.sprites():
        bullet.kill()

    total_time = game_finish - game_start

    username = formulario.form.logged_in_user

    if game_lose:
        draw_text(f"YOU LOSE {username}", font40, white, screen_width / 2, screen_height / 2)
    else: draw_text(f"YOU WIN {username}", font40, white, screen_width / 2, screen_height / 2)
    draw_text(f"SCORE: {int(spaceship.score + (game_finish - game_start) / 100 * 2.50)}", font40, white, screen_width / 2, (screen_height / 2) - 50)
    draw_text(f"TOTAL TIME: {int(total_time / 1000)} seconds", font40, white, screen_width / 2, (screen_height / 2) - 100)
    counter = 0
    if not game_inserted:
        database.sqlite.introduce_game_level(username, spaceship.score, level, game_start, game_finish)
        game_inserted = True

    spaceship.score = 0

    volver_al_menu_rect = draw_text("VOLVER AL MENÚ", font40, white, screen_width / 2, (screen_height / 2) - 300)


"""arduino = serial.Serial("COM8", 9600)
"""# Inicialización de pygame, mixer y font
pygame.init()
mixer.init()
pygame.font.init()

game_inserted = False

# Pre configuración de mixer
pygame.mixer.pre_init(44100, -16, 2, 512)

# FPS
clock = pygame.time.Clock()
fps = 60

# Variables de colores globales
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Dimensiones de pantalla
screen_width = 1920
screen_height = 1080

# 0- El juego no a terminado, 1- El jugador a ganado, -1- El jugador a perdido.
game_over = 0

# Variables de generación de aliens
rows = 0
cols = 0

# Cooldown disparos aliens
alien_cooldown = 1000
last_alien_shoot = pygame.time.get_ticks()

countdown = 3
last_count = pygame.time.get_ticks()

# Creación de ventana.
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Cargar imágenes
bg = pygame.image.load("graphics/back_ground.webp").convert_alpha()

# Cargar sonidos
explosion_fx = pygame.mixer.Sound("graphics/explosion.wav")
explosion_fx.set_volume(0.2)

explosion_2_fx = pygame.mixer.Sound("graphics/explosion2.wav")
explosion_2_fx.set_volume(0.2)

laser_fx = pygame.mixer.Sound("graphics/laser.wav")
laser_fx.set_volume(0.2)

# Cargar fuentes
font30 = pygame.font.Font(None, 30)
font40 = pygame.font.Font(None, 40)

# Titulo dentro del juego
title_surface = font40.render("Space Invaders", False, white)
title_rect = title_surface.get_rect(midtop=(screen_width / 2, 0))

# Creamos los grupos para nuestra nave
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Creamos el jugador
spaceship = Spaceship(int(screen_width / 2), int(screen_height - 100), 3)
spaceship_group.add(spaceship)

can_access_level = [True, False, False]

run = True
game_active = False
level = 0
game_start = 0

while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    key_updates()


    if game_active:
        # Lógica de juegoº

        if game_start == 0:
            game_start = pygame.time.get_ticks()


            if level == 1:
                spaceship.speed = 5
                spaceship.health_remaining = 5
                Alien_Bullets.set_global_speed(3)
                Aliens.set_global_speed(3)
                rows = 3
                cols = 5
                number_alien_shoots = 8


                # Creamos los aliens
                create_aliens()

            if level == 2:
                spaceship.speed = 5
                spaceship.health_remaining = 4
                Alien_Bullets.set_global_speed(5)
                Aliens.set_global_speed(5)
                rows = 4
                cols = 6
                number_alien_shoots = 12

                create_aliens()

            if level == 3:
                spaceship.speed = 5
                spaceship.health_remaining = 2
                Alien_Bullets.set_global_speed(5)
                Aliens.set_global_speed(6)
                rows = 5
                cols = 8
                number_alien_shoots = 15

                create_aliens()

        #rawString = arduino.readline().strip()

        # Alien shoots
        alien_shoot(number_alien_shoots)

        # Actualizaciones de las sprites
        spaceship_group.update()
        bullet_group.update()
        alien_group.update()
        alien_bullet_group.update()
        explosion_group.update()

        # Dibujar las sprites
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        display_score()
        #Falta hacerlo


        if spaceship.health_remaining == 0:
            game_active = False
            game_finish = pygame.time.get_ticks()
            game_lose = True

        for alien in alien_group:
            if alien.rect.bottom >= spaceship.rect.top - 100:
                game_active = False
                game_finish = pygame.time.get_ticks()
                game_lose = True

        if aliens_eliminados == rows * cols :
            game_active = False
            game_finish = pygame.time.get_ticks()
            game_lose = False

            if level == 1:
                can_access_level[1] = True
            elif level == 2:
                can_access_level[2] = True

    else:
        if level == 0:
            formulario.form.root.mainloop()
            menu()
        else:
            game_end(game_finish, game_start)

    pygame.display.flip()

pygame.quit()
#arduino.close()aaaaaaa
exit()

