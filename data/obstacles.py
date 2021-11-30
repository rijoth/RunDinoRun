import pygame
from random import randint, choice
from data import sprite_sheet

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.animation_index = 0    
        if type == 'cactus1':
            sprite_1 = pygame.image.load("resources/images/cactus1.png").convert_alpha()
            self.frame = sprite_1
            y_pos = 182

        if type == 'cactus2':
            sprite_1 = pygame.image.load("resources/images/cactus2.png").convert_alpha()
            self.frame = sprite_1
            y_pos = 182    

        if type == 'cactus3':
            sprite_1 = pygame.image.load("resources/images/cactus3.png").convert_alpha()
            self.frame = sprite_1
            y_pos = 182

        if type == 'blank':
            self.image = pygame.Surface((10, 10))
            self.image.set_alpha(0)
            self.rect = self.image.get_rect(midbottom=(700, 1280))
            y_pos = 182          

        if type == 'asteroid':
            sprite_2 = pygame.image.load("resources/images/asteroid.png").convert_alpha()
            self.sheet = sprite_sheet.SpriteSheet(sprite_2)
            self.frame = self.sheet.get_image(self.animation_index, 48, 48, 1, (0,0,0))
            y_pos = randint(0, 5)

        self.type = type
        self.gravity = 0 # only for asteroid
        if type != 'blank':
            self.image = self.frame
            self.rect = self.image.get_rect(midbottom = (randint(700, 1280), y_pos))

    def animation_state(self):
        if self.type == 'asteroid':
            self.animation_index += 0.4
            if self.animation_index >= 6: self.animation_index = 0
            self.frame = self.sheet.get_image(int(self.animation_index), 48, 48, 1, (0,0,0))
            self.image = self.frame
    
    def apply_gravity(self):
        if self.type == 'asteroid':
            self.gravity += 0.25
            self.rect.y = self.gravity

    def update(self):
        if self.type == 'asteroid':
            self.rect.x -= 5
        else:
            self.rect.x -= 4

        self.animation_state()
        self.apply_gravity()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()