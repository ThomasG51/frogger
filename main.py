import pygame
import sys
import settings
from camera_group import CameraGroup
from simple_sprite import SimpleSprite
from long_sprite import LongSprite
from car import Car
from player import Player
from random import choice
from random import randint

# init
pygame.init()
display_surface = pygame.display.set_mode(size=(settings.WINDOWS_WITH, settings.WINDOWS_HEIGHT))
pygame.display.set_caption(title="Frogger Like")
clock = pygame.time.Clock()
pop_car_event = pygame.event.custom_type()
pygame.time.set_timer(event=pop_car_event, millis=80)
car_position_list = []

# sprite groups
camera_group = CameraGroup()
collision_group = pygame.sprite.Group()

# sprites
player = Player(groups=camera_group, position=(2062, 3274), collision_group=collision_group)

for file_name, positions in settings.SIMPLE_OBJECTS.items():
    path = f"graphics/objects/simple/{file_name}.png"
    for position in positions:
        SimpleSprite(groups=[camera_group, collision_group], surface_path=path, position=position)

for file_name, positions in settings.LONG_OBJECTS.items():
    path = f"graphics/objects/long/{file_name}.png"
    for position in positions:
        LongSprite(groups=[camera_group, collision_group], surface_path=path, position=position)

# music
music = pygame.mixer.Sound("audio/music.mp3")
music.play(loops=True)

# win text
font = pygame.font.Font(None, 50)
win_text_surface = font.render("YOU WIN", True, "White")
win_text_rect = win_text_surface.get_rect(center=(settings.WINDOWS_WITH/2, settings.WINDOWS_HEIGHT/2))

# game loop
while True:
    #delta time
    delta_time = clock.tick() / 1000

    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pop_car_event:
            random_car_position = choice(settings.CAR_START_POSITIONS)
            if random_car_position not in car_position_list:
                car_position_list.append(random_car_position)
                position_x = random_car_position[0]
                position_y = random_car_position[1] + randint(-10, 10)  # ajout d'un peu d'offset aléatoire
                Car(groups=[camera_group, collision_group], position=(position_x, position_y))
            if len(car_position_list) > 5:
                del car_position_list[0]

    if player.position.y >= 1180:
        # update
        camera_group.update(delta_time=delta_time)

        # draw
        display_surface.fill(color="Black")
        camera_group.draw_with_offset(display_surface=display_surface, player=player)
    else:
        # draw
        display_surface.fill(color="Teal")
        display_surface.blit(source=win_text_surface, dest=win_text_rect)
        music.stop()

    # display
    pygame.display.update()
