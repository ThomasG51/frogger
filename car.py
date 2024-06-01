import pygame
from os import walk
from random import randint
from custom_enum import SpriteType


class Car(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        super().__init__(groups)
        self.type = SpriteType.CAR
        self.image = self._random_car()
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(self.rect.center)
        self._car_direction()
        self.speed = 300
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)

    def update(self, delta_time):
        self._move(delta_time=delta_time)
        self._clear()

    def _random_car(self):
        for path, _, file_names in walk("graphics/cars"):
            random_file_name = file_names[randint(0, 2)]
            return pygame.image.load(f"{path}/{random_file_name}").convert_alpha()

    def _car_direction(self):
        position_x = self.position[0]
        if position_x < 0:
            self.direction = pygame.math.Vector2((1, 0))
        else:
            self.direction = pygame.math.Vector2((-1, 0))
            self.image = pygame.transform.flip(surface=self.image, flip_x=True, flip_y=False)

    def _move(self, delta_time):
        self.position += self.direction * self.speed * delta_time
        self.hitbox.center = (round(self.position.x), round(self.position.y))  # ne pas oublier le round()
        self.rect.center = self.hitbox.center

    def _clear(self):
        if not -200 < self.rect.x < 3400:
            self.kill()
