import pygame
from custom_enum import SpriteType


class LongSprite(pygame.sprite.Sprite):
    def __init__(self, groups, surface_path, position):
        super().__init__(groups)
        self.type = SpriteType.OBJECT
        self.image = pygame.image.load(surface_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-self.rect.width*0.8, -self.rect.height/2)
        # on descend la hitbox vers le bas pour les longs objets pour garder un bonne perspective
        self.hitbox.bottom = self.rect.bottom - (self.rect.height * 0.10)

