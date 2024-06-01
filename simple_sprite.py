import pygame
from custom_enum import SpriteType


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, groups, surface_path, position):
        super().__init__(groups)
        self.type = SpriteType.OBJECT
        self.image = pygame.image.load(surface_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        # on réduit la hauteur de la hitbox de 50%
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)
