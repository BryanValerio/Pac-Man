import pygame
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        """All the functions with define the player, a.k.a Pac-Man, as well as the process of collecting the coins, the location, and where the player can move"""
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        # where Pac-Man starts relative to the board
        self.direction = vec(0, 0)
        # can change how the player automatically moves
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1

    def update(self):
        """Updates the movements of the player and keeps track of where the player is"""
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # calls to the next function in order to check that the player is within bounds  

        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        # keep track of where the player is currently to the grid   

        if self.on_coin():
            self.eat_coin()
        # removes the coin once the player is over the tile

        if self.on_fruit():
            self.eat_fruit()
        # removes the fruit once the player is over the tile

    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        """A function used to write the text on the screen during all the different states"""
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def draw(self):
        """The player-controlled object"""
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.app.cell_width//2-2)
        # Drawing player lives

        self.draw_text('Lives Left: ', self.app.screen, (30, height - 15), 18, (255, 255, 255), 'arialblack')

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (100 + 20*x, HEIGHT - 15), 7)
        # to display the number of the lives the player still has

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        """Defines whether or not the player is on a coin and what happens"""
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
        # in the x-direction
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        # in the y-direction

        return False

    def eat_coin(self):
        """Adds a point to the current score if the player is on a coin"""
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_fruit(self):
        """Defines whether or not the player is on a fruit and what happens"""
        if self.grid_pos in self.app.fruit:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
        # in the x-direction 

            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        # in the y-direction

        return False

    def eat_fruit(self):
        """Adds points to the current score if the player is on a coin"""
        self.app.fruit.remove(self.grid_pos)
        self.current_score += 5

    def move(self, direction):
        """Movement stored for use is detecting collisions"""
        self.stored_direction = direction

    def get_pix_pos(self):
        """Player's position relative to the board"""
        return vec((self.grid_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)
        # where Pac-Man starts relative to the board

    def time_to_move(self):
        """Determines whether or not the player is able to move"""
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        # for the x-direction

        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        # for the y-direction

        # checks to see if the player is still within the bounds

    def can_move(self):
        """Detects whether there is a wall in front of the player"""
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
