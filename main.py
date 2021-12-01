"""
Game: Run Dino Run
Author: Rijo Thomas
Email: evolvedantgames@gmail.com
Made with PyGame
"""

import pygame, sys, shelve
from random import randint, choice
from data import moving_background, obstacles, sprite_sheet, player

pygame.init()
# scaled window size
screen = pygame.display.set_mode((640, 480))
# orginal window size
window = pygame.Surface((320, 240))
pygame.display.set_caption("RUN DINO RUN")

# game icon
icon_surf = pygame.image.load("resources/images/sun.png").convert_alpha()
pygame.display.set_icon(icon_surf)

pygame.display.init()
clock = pygame.time.Clock()

# creating groups
obstacle_grp = pygame.sprite.Group()
player_grp = pygame.sprite.GroupSingle()
player_grp.add(player.Player())

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(200, 1000))

# game font
game_font = pygame.font.Font("resources/fonts/ThaleahFat.ttf", 15)
title_font = pygame.font.Font("resources/fonts/ThaleahFat.ttf", 25)
copyright_font = pygame.font.Font("resources/fonts/monogram.ttf", 15)

# score time
start_time = 0

# Score
score = 0
try:
    with shelve.open("highscore.dat") as file:
        high_score = int(file['highscore'])
        file.close()
except:
    high_score = 0

# score
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = game_font.render(f'{current_time} / {high_score}', False, (25,18,30))
    score_rect = score_surf.get_rect(center=(260, 10))
    window.blit(score_surf, score_rect)
    return current_time

# bg music
bg_music = pygame.mixer.Sound("resources/audio/bgm.mp3")
bg_music.set_volume(0.5)
bg_music_playing = False

# backgrounds
background1_surf = pygame.image.load("resources/images/background1.png").convert_alpha()
background2_surf = pygame.image.load("resources/images/background2.png").convert_alpha()
background3_surf = pygame.image.load("resources/images/background3.png").convert_alpha()
ground_surf = pygame.image.load("resources/images/ground.png").convert_alpha()
ground_width = ground_surf.get_width()
ground_surf_x = 0


# moving background
background1 = moving_background.Moving_Background(background1_surf, 0, 1)
background2 = moving_background.Moving_Background(background2_surf, 70, 2)
background3 = moving_background.Moving_Background(background3_surf, 90, 3)
ground = moving_background.Moving_Background(ground_surf, 160, 4) 

# title
title_text = title_font.render(" RUN DINO RUN ", None,(141,132,22), (69,65,78))
title_text_rect = title_text.get_rect(center=(160, 40))

cc_text = copyright_font.render("© evolvedantgames.itch.io", None, (171, 235, 198))
cc_text_rect = title_text.get_rect(center=(160, 230))

# main menu
game_active = False
selected = "start"
def main_menu():
    if selected == "start":
        start_option = game_font.render("- START -", False, (141,132,22))
        start_rect = start_option.get_rect(center=(160, 120))
        window.blit(start_option, start_rect)
    else:
        start_option = game_font.render("START", False, (171, 235, 198))
        start_rect = start_option.get_rect(center=(160, 120))
        window.blit(start_option, start_rect)
    if selected == "quit":
        quit_option = game_font.render("- QUIT -", False, (141,132,22))
        quit_rect = quit_option.get_rect(center=(160, 140))
        window.blit(quit_option, quit_rect)
    else:
        quit_option = game_font.render("QUIT", False, (171, 235, 198))
        quit_rect = quit_option.get_rect(center=(160, 140))
        window.blit(quit_option, quit_rect)  


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == obstacle_timer:
                # obstacle_grp.add(obstacles.Obstacle(choice(['cactus', 'asteroid'])))
                obstacle_grp.add(obstacles.Obstacle(choice(['cactus1','cactus2','cactus3', 'blank', 'blank', 'blank'])))
        else:
            start_time = int(pygame.time.get_ticks()/1000)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected == "start":
                        game_active = True
                    if selected == "quit":
                        pygame.quit()
                        sys.exit()

    if game_active:
        # playing bgm
        if not bg_music_playing:
            bg_music.play(loops=-1)
            bg_music_playing = True

        window.fill((0,0,0))
        # window.blit(background1_surf, (0,0))
        background1.move(window)
        background2.move(window)
        background3.move(window)
        ground.move(window)
        score = display_score()

        # drawing and updating obstacles
        obstacle_grp.draw(window)
        obstacle_grp.update()

        player_grp.draw(window)
        player_grp.update()
        
        # collision mask
        player_mask = pygame.Surface((10, player_grp.sprite.rect.height - 10))
        player_mask.set_alpha(0)
        player_mask.fill((255, 255, 255))
        player_mask_rect = player_mask.get_rect(topleft=(player_grp.sprite.rect.x + 15, player_grp.sprite.rect.y + 5))
        window.blit(player_mask, player_mask_rect)
        
        # collision
        for sprite in obstacle_grp.sprites():
            if player_mask_rect.colliderect(sprite.rect):
                obstacle_grp.empty()
                game_active = False

        # game_active = collision_sprite()
    else:
        bg_music_playing = False
        bg_music.stop()
        window.fill((0,0,0))
        background1.move(window)
        background2.move(window)
        background3.move(window)
        ground.move(window)     
        main_menu()

        if score > high_score:
            high_score = score
            file = shelve.open("highscore.dat")
            file['highscore'] = high_score
            file.close()
        high_score_text = game_font.render(f'High Score: {high_score}', False, (181,74,74))
        high_score_text_rect = high_score_text.get_rect(center=(160, 100))
        window.blit(title_text, title_text_rect)
        window.blit(high_score_text, high_score_text_rect)
        window.blit(cc_text, cc_text_rect)

    # blitting orginal screen to scaled window
    scaled_window = pygame.transform.scale(window, screen.get_size())
    screen.blit(scaled_window, (0,0))

    pygame.display.update()
    clock.tick(60)