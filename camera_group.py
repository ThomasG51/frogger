import pygame
import settings

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.background = pygame.image.load("graphics/main/map.png").convert()
        self.overlay = pygame.image.load("graphics/main/overlay.png").convert_alpha()

    def draw_with_offset(self, display_surface, player):
        self.offset.x = player.rect.centerx - (settings.WINDOWS_WITH / 2)
        self.offset.y = player.rect.centery - (settings.WINDOWS_HEIGHT / 2)

        display_surface.blit(self.background, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            sprite_position = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, sprite_position)

        display_surface.blit(self.overlay, -self.offset)