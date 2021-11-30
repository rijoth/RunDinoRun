import pygame
import time
from data import sprite_sheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet_image = pygame.image.load("resources/images/WalkingDino.png").convert_alpha()
        self.player_sheet = sprite_sheet.SpriteSheet(sprite_sheet_image)
        self.frame_index = 0
        self.player_frame = self.player_sheet.get_image(self.frame_index, 38, 38, 1, (0,0,0))
        self.image = self.player_frame
        self.rect = self.image.get_rect(midbottom=(50, 180))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("resources/audio/jump.wav")
        self.jump_sound.set_volume(0.25)

    def animation_state(self):
        self.frame_index += 0.35
        if self.frame_index >= 10: self.frame_index = 0
        self.player_frame = self.player_sheet.get_image(int(self.frame_index), 38, 38, 1, (0,0,0))
        self.image = self.player_frame  

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 180:
            self.jump_sound.play()
            self.gravity = -12

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 180:
            self.rect.bottom = 180

    def update(self):
        self.animation_state()   
        self.apply_gravity()
        self.player_input()
