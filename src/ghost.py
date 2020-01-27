import pygame
from settings import *

vec = pygame.math.Vector2

class Enemy:
    """This class is all about the enemies and their intial positons, their colors, their differnt personalities/ behavior"""
        def __init__(self, base, position, number):
            self.base = base
            self.grid_position = position
            self.pix_position = self.get_pix_position()
            self.radius = int(self.base.cell_width//2.3)
            self.number = number
            self.color = self.set_color()


        def update(self):
            pass

        def draw(self):
            if self.number == 0:
                pygame.draw.circle(self.base.screen, self.color, (int(self.pix_position.x), int(self.pix_position.y)), self.radius)

        def get_pix_position(self):
            """Position of the ghost relative to the rest of the board"""
            return vec((self.grid_position.x*self.base.cell_width)+top_bottom_space//2+self.base.cell_width//2, 
            (self.grid_position.y*self.base.cell_height)+top_bottom_space//2+self.base.cell_height//2)
            # where ghost starts relative to the board

        def set_color(self):
            """The color of the different enemies"""
            if self.color == 0:
                return (43, 75, 200)
            if self.color == 1:
                return (200, 200, 30)
            if self.color == 2:
                return (185, 32, 31)
            if self.color == 3:
                return (210, 155, 30)      