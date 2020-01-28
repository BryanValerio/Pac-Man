import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        """This class is all about the enemies and their intial positons, their colors, their differnt personalities/ behavior"""
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        """Updates the position of the enemies"""
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()
        # to avoid the game crashing when the 'scared' one reaches its target
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        # keeps track of where the enemy is in context to the maze       

    def draw(self):
        """This functions describes how the enemies/ ghost will look"""
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        """Determines the speed of the enemy based on their different personality types"""
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        """Determines the target of the enemies based on their different personality types"""
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        # gives the two enemies that target the player the grid position of the player
        else:
        # for the enemy with the 'scared' personality trait, who wants to be far away from the player
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            # if the player is in the bottom right, it wants to go to the top left
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            # if the target is in the top right, it wants to go to the bottom left 
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            # if the player is on the bottom left, it wants to go to the top right
            else:
                return vec(COLS-2, ROWS-2)
            # if the player is on the top left, it wants to go to the bottom right

    def time_to_move(self):
        """Determines whether or not the enemy is able to move"""
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        # for the x-direction
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        # for the y-direction
        return False
        # to make the enemy stay within the bounds


    def move(self):
        """Tells how the enemies move, including their different personality traits"""
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        # will try and follow the player
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        # will try and follow the player
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)
        # will try and avoid the player


    def get_path_direction(self, target):
        """Enemies trying to find the quickest way to the  for all other personality types"""
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        """Find the next cell in order to get closer to the player"""
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
            # a Breadth First Search algorithm used which takes a starting point (the enemy's position) and the target (the player)
            # they all need to be integers, hence all the int()
        return path[1]

    def BFS(self, start, target):
        """Details the Breadth First Search Function/ Algorithm"""
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
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
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                # the four cardinal direction which are north, south, east, west
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                # when using BFS, the y-position goes before the x-position
                                # if grid != 1, it means it is a wall 
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})

        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest


    def get_pix_pos(self):
        """Position of the ghost relative to the rest of the board"""
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 +
                   self.app.cell_height//2)
        # where ghost starts relative to the board

    def set_colour(self):
        """Sets the color of the ghost depending the on the number it receives"""
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)

    def set_personality(self):
        """This function determines the the personality of the different ghosts, which affects their movement"""
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        else:
            return "scared"
