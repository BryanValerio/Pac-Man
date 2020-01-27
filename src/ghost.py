import pygame
from settings import *
import random

vec = pygame.math.Vector2

class Enemy:
    """This class is all about the enemies and their intial positons, their colors, their differnt personalities/ behavior"""
    def __init__(self, base, position, number):
        self.base = base
        self.grid_position = position
        self.starting_position = [pos.x, pos.y]
        self.pix_position = self.get_pix_position()
        self.radius = int(self.base.cell_width//2.3)
        self.number = number
        self.color = self.set_color()
        self.direction = vec(0, 0)
        self.personality = self.set_personality
        self.target = None
        self.speed = self.set_speed()


    def update(self):
        """Updates the position of the enemies"""
        self.target = self.set_target()
        if self.target != self.grid_position:
            self.pix_position += self.direction * self.speed
            if self.time_to_move():
                self.move()
        # to avoid the game crashing when the 'scared' one reaches its target
        self.grid_position[0] = (self.pix_position[0]-top_bottom_space+self.base.cell_width//2)//self.base.cell_width+1
        self.grid_position[1] = (self.pix_position[1]-top_bottom_space+self.base.cell_height//2)//self.base.cell_height+1 
        # keeps track of where the enemy is in context to the maze       


    def get_pix_position(self):
        """Position of the ghost relative to the rest of the board"""
        return vec((self.grid_position.x*self.base.cell_width)+top_bottom_space//2+self.base.cell_width//2, 
        (self.grid_position.y*self.base.cell_height)+top_bottom_space//2+self.base.cell_height//2)
        # where ghost starts relative to the board


    def time_to_move(self):
        """Determines whether or not the enemy is able to move"""
        if int(self.pix_position.x+top_bottom_space//2) % self.base.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction = vec(0,0):
                return True
        # for the x-direction
        if int(self.pix_position.y+top_bottom_space//2) % self.base.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction = vec(0, 0):
                return True
        return False
        # for the y-direction

        # to make the enemy stay within the bounds


    def move(self):
        """Tells how the enemies move, including their different personality traits"""
        if self.personality == "random":
            self.direction = self.get_random_direction()
        # will go in a random direction as dictated by a the function 'get_random_direction'
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)
        # will try and follow the player
    
    def get_path_direction(self, target):
        """Enemies trying to find the quickest way to the  for all other personality types"""
        next_cell = self.find_next_cell(target)
        xdirection = next_cell[0] - self.grid_position[0]
        ydirection = next_cell[1] - self.grid_position[1]
        return vec(xdirection, ydirection)

    def find_next_cell(self):
        """Find the next cell in order to get closer to the player"""
        path = self.BFS( [int(self.grid_position.x), int(self.grid_position.y)], [int(target[0]), int(target[1])])
            # a Breadth First Search algorithm used which takes a starting point (the enemy's position) and the target (the player)
            # they all need to be integers, hence all the int()
        return path[1]

    
    def BFS(self, start, target):
        """Details the Breadth First Search Function/ Algorithm"""
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.base.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        
        queue = [start]
        path = []
        visited = []

        while queue:
            current = queue[0]
            # the first thing appended will be the first thing that is given
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors: [[0, -1], [1, 0], [0, 1], [-1, 0]]
                # the four cardinal direction which are north, south, east, west
                for neighbor in neighbors:
                    if neighbor[0] + current[0] >= 0 and neighbor[0] + current[0] < len(grid[0]):
                        if neighbor[1] + current[1] >= 0 and neighbor[1] + current[1] < len(grid[0]):
                            next_cell = [neighbor[0] + current[0], neighbor[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                # when using BFS, the y-position goes before the x-position
                                # if grid != 1, it means it is a wall 
                                    queue.append(next_cell)
                                    path.append({'Current': current, next_cell, 'Next': next_cell})
        
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target
                    target = step['Current']
                    shortest.insert(0, step['Current'])
        
        return shortest

    def set_target(self):
        if self.personality == 'speedy' pr self.personality == 'slow':
            return self.base.player.grid_position
        # gives the two enemies that target the player the grid position of the player
        else:
        # for the enemy with the 'scared personality trait, who wants to be far away from the player
            if self.base.player.grid_position.[0] > columns//2 and self.base.player.grid_position.[1] > rows//2:
                return vec(1, 1)
            # if the player is in the bottom right, it wants to go to the top left
            if self.base.player.grid_position.[0] > columns//2 and self.base.player.grid_position.[1] < rows//2:
                return vec(1, rows-2)
            # if the target is in the top right, it wants to go to the bottom left 
            if self.base.player.grid_position.[0] < columns//2 and self.base.player.grid_position.[1] > rows//2:
                return vec(columns-2, 1)
            # if the player is on the bottom left, it wants to go to the top right
            else:
                return vec(columns-2, rows-2)
            # if the player is on the top left, it wants to go to the bottom right
    
    def set_speed(self):
        if self.personality == ['speedy', 'scared']:
            speed = 3
        else:
            speed = 1
        return speed
        




    def get_random_direction(self):
        """Generates a random direction for the ghost with the personality of 'random'"""
        while True:
            number = random.randint(-2, 1)
            if number == -2 :
                x_direction, y_direction = 1, 0 
            elif number == -1:
                x_direction, y_direction = 0, 1
            elif number == 0:
                x_direction, y_direction = -1, 0
            else:
                x_direction, y_direction = 0, -1
            # a sequence that generates random numbers and then makes it equal to movement in a certain direction
            next_position = vec(self.grid_position.x + x_direction, self.grid_position.y + y_direction)
            if next_position not in self.base.walls
                break
            # makes sure that the ghost does not phase through walls
        return vec(x_direction, y_direction)


    def draw(self):
        """How the enemies look"""
        if self.number == 0:
            pygame.draw.circle(self.base.screen, self.color, (int(self.pix_position.x), int(self.pix_position.y)), self.radius)


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
    
    def set_personality(self):
        """The different personality types"""
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"