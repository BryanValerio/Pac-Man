import pygame
from settings import *


vec = pygame.math.Vector2


class Player:
    """All the functions with define the player, a.k.a Pac-Man, as well as the process of collecting the coins, the location, and where the player can move"""
    def __init__(self, base, position):
        self.base = base
        self.grid_position = position
        self.pix_position = self.get_pix_position()
        # where Pac-Man starts relative to the board
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2


    def get_pix_position(self):
        """Player's position relative to the board"""
        return vec((self.grid_position.x*self.base.cell_width)+top_bottom_space//2+self.base.cell_width//2, 
        (self.grid_position.y*self.base.cell_height)+top_bottom_space//2+self.base.cell_height//2)
    # where Pac-Man starts relative to the board


    def update(self):
        """Updates the movements of the player and keeps track of where the player is"""
        if self.able_to_move:
            self.pix_position += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction == self.stored_direction
            self.able_to_move = self.can_move()
        # calls to the next function in order to check that the player is within bounds  

        self.grid_position[0] = (self.pix_position[0]-top_bottom_space+self.base.cell_width//2)//self.base.cell_width+1
        self.grid_position[1] = (self.pix_position[1]-top_bottom_space+self.base.cell_height//2)//self.base.cell_height+1
        # keep track of where the player is currently to the grid   
           
        if self.on_coin():
            self.eat_coin()
    

    def on_coin(self):
        """Defines whether or not the player is on a coin and what happens"""
        if self.grid_position in self.base.coins:
            return True
        else:
            return False

    def eat_coin(self):
        """Adds a point to the current score if the player is on a coin"""
        self.base.coins.remove(self.grid_position)
        self.current_score += 1
        


    def time_to_move(self):
        """Determines whether or not the player is within the bounds of the maze"""
        if int(self.pix_position.x+top_bottom_space//2) % self.base.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_position.y+top_bottom_space//2) % self.base.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True
        # to make the player stay within the bounds

    def can_move(self):
        """Detects whether there is a wall in front of the player"""
        for wall in self.base.walls:
            if vec(self.grid_position+self.direction) == wall:
                return False  
        return True     

    def draw(self):
        """The player-controlled object"""
        pygame.draw.circle(self.base.screen, (190, 190, 15), (int(self.pix_position.x), int(self.pix_position.y)), self.base.cell_width//2-2)
        # the controllable thing

        # pygame.draw.rect(self.base.screen, (255, 0, 0), (self.grid_position[0]*self.base.cell_width+top_bottom_space//2, self.grid_position[1]*self.base.cell_height+top_bottom_space//2, self.base.cell_width, self.base.cell_height), 1)
        # ^^ the reactangle keeping track of the player


    def move(self, direction):
        """Movement stored for use is detecting collisions"""
        self.stored_direction = direction
