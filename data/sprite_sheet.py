import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        # blit portion of spritesheet in surface
        image.blit(self.sheet, (0 , 0), (frame * width, 0, width, height))
        # scale image if required
        image = pygame.transform.scale(image, (width * scale, height * scale))
        # remove black background from surface
        image.set_colorkey(color) 

        return image