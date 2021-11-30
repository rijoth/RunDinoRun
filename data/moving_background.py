import pygame

# moves background horizontally from right to left
class Moving_Background:
    def __init__(self, surface, surface_y,speed):
        self.surface_x = 0
        self.surface_y = surface_y
        self.surface = surface
        self.speed = speed
        self.surface_width = self.surface.get_width()
    def move(self, window):
        window.blit(self.surface, (self.surface_x, self.surface_y))
        window.blit(self.surface, (self.surface_x+self.surface_width,self.surface_y))
        if self.surface_x <= self.surface_width * -1:
            window.blit(self.surface, (self.surface_x+self.surface_width,self.surface_y))
            self.surface_x = 0
        self.surface_x -= self.speed