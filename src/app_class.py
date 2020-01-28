import pygame
import sys
import copy
from settings import *
from player_class import *
from enemy_class import *
# imports everything from all the different files


pygame.init()
vec = pygame.math.Vector2
# a vector which can be used for 1D motion, 2D motion (x, y), 3D motion (x, y, z)


class App:
    """Constructor Class for running the background, points, text, and different screens of the game"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        # when the player is first able to control Pac-Man
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        # the cells used to line up Pac-Man and the ghosts
        self.walls = []
        self.coins = []
        self.fruit = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        """Defines at which point the game is at, which includes the intro screen, actual game screen, and the game over screen"""
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
                # when the game is first launched 
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
                # when the actual game is running 
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
                # when the player loses the game
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()



    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        """A function used to write the text on the screen during all the different states"""
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        """A function that loads the map, player, enemies, coins, walls"""
        self.background = pygame.image.load('img/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        # changing the parameters will allow the background to scale to it 

        with open("walls.txt", 'r') as file:
            # opens the wall.txt file that is a layout of the walls, player, ghosts, and enemies
            for yidx, line in enumerate(file):
                # changes the columns and rows into values, the 1st row = 0, the 2nd row = 1, and etc.
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                        # creates a list with the position of the walls
                    elif char == "C":
                        # for the coins that pac man collects
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
                    elif char == 'F':
                        self.fruit.append(vec(xidx, yidx))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        """Draws and describes a grid"""
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))
         # drawing a grid in order to match up the layout  with the maze background

        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
        #                                                        coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        """A function that describes how the player and ghost get resetted back"""
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        # when the player loses a life, thet get reset to their initial position
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        # enemies get reset to their initial position when the player loses a life

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

        self.fruit = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'F':
                        self.fruit.append(vec(xidx, yidx))
        self.state = "playing"



    def start_events(self):
        """A function that describes what happens at the introduction screen"""
        for event in pygame.event.get():
        # to call the events that have happpened from the time it was last called
            if event.type == pygame.QUIT:
                self.running = False
                # stops the game if the exit button is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        """This function details the visuals of the introduction screen"""
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACEBAR TO START', self.screen, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [
                       WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()




    def playing_events(self):
        """This function describes the controls for the player"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                    # if the player presses the left arrow key, the character will move in a vec in the negative x-direction(left) by one 
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        """Updates the information on the player and enemies"""
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        """Visuals for during the actual game, including a score keeeper"""
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_fruit()
        # to draw the coins on the actual screen instead of the background
        # self.draw_grid()
        # ^^ used to make a grid to ensure that the units move within the maze image/ testing purposes 
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        # to describe the layout of the playing screen with the maze


    def remove_life(self):
        """When the player loses a life and when they reach 0"""
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0
                # resets both the player and the enemy when the player loses a life 

    def draw_coins(self):
        """Where the coins go"""
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
    
    def draw_fruit(self):
        """Where the fruits go"""
        for fruit in self.fruit:
            pygame.draw.circle(self.screen, (255, 10, 10),
                               (int(fruit.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(fruit.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 9)




    def game_over_events(self):
        """What happens when the player gets a 'game over'"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        """This function describes the layout of the 'game over' screen"""
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACEBAR to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()

