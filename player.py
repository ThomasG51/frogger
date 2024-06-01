import pygame
import sys
from os import walk
from custom_enum import SpriteType, CollisionDirection


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, position, collision_group):
        super().__init__(groups)
        self.type = SpriteType.PLAYER
        self._import_assets()
        self.frame_index = 0
        self.animation_direction = 'down'
        self.image = self.animations[self.animation_direction][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200
        self.collision_group = collision_group
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)

    def update(self, delta_time):
        self._animate(delta_time=delta_time)
        self._input()
        self._move(delta_time=delta_time)
        self._add_map_walls()

    def _import_assets(self):
        path = "graphics/player/"
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:  # récupération des noms des dossiers
                child_folder_names = folder[1]
                for name in child_folder_names:
                    self.animations[name] = []
            else:  # récupération des noms de fichier contenu dans les dossiers
                folder_path = folder[0]
                file_names = folder[2]
                animations_key = folder[0].split("/")[2]
                for file_name in file_names:
                    surface = pygame.image.load(f"{folder_path}/{file_name}").convert_alpha()
                    self.animations[animations_key].append(surface)

    def _animate(self, delta_time):
        self.frame_index += 10 * delta_time
        current_animation = self.animations[self.animation_direction]

        if self.direction.magnitude() != 0:  # si un déplacement des en cours on anime les frames (player marche)
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:  # sinon on prend la premiere frame (player immobile)
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def _input(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.animation_direction = "up"
            self.direction.y = -1
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.animation_direction = "down"
            self.direction.y = 1
        else:
            self.direction.y = 0

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.animation_direction = "right"
            self.direction.x = 1
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.animation_direction = "left"
            self.direction.x = -1
        else:
            self.direction.x = 0

    def _move(self, delta_time):
        # pour que le player se déplace a la meme vitesse en ligne droite ou diagonale
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.position.x += self.direction.x * self.speed * delta_time
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self._collision(CollisionDirection.HORIZONTAL)

        self.position.y += self.direction.y * self.speed * delta_time
        self.hitbox.centery = round(self.position.y)
        self.rect.centery =  self.hitbox.centery
        self._collision(CollisionDirection.VERTICAL)

    def _collision(self, direction: CollisionDirection):
        for sprite in self.collision_group.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if hasattr(sprite, 'type') and sprite.type == SpriteType.CAR:
                    pygame.quit()
                    sys.exit()
                if direction == CollisionDirection.HORIZONTAL:
                    if self.direction.x > 0: #  le player se déplace vers la droite
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # le player se déplace vers la gauche
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx
                elif direction == CollisionDirection.VERTICAL:
                    if self.direction.y > 0:  # le player se déplace vers la bas
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # le player se déplace vers la haut
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery

    def _add_map_walls(self):
        if self.rect.left < 640:
            self.position.x = 640 + (self.rect.width / 2)
            self.hitbox.left = 640
            self.rect.left = self.hitbox.left
        if self.rect.right > 2560:
            self.position.x = 2560 - (self.rect.width / 2)
            self.hitbox.right = 2560
            self.rect.right = self.hitbox.right
        if self.rect.bottom > 3500:
            self.position.y = 3500 - (self.rect.height / 2)
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

