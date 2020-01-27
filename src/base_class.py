import pygame
import sys
import copy
from player import *
from ghost import *
from settings import *

pygame.init
vec = pygame.math.Vector2
# a vector which can be used for 1D motion, 2D motion (x, y), 3D motion (x, y, z)


class Base:
  """This class holds the code for running the actual game with everything coming together"""
  def __init__(self):
    self.screen = pygame.display.set_mode((width, height))
    self.clock = pygame.time.Clock()
    # to control the FPS of the game when it runs 
    self.running = True
    self.state = 'intro'
  # initiates the game
    self.cell_width = maze_width//columns
    self.cell_height = maze_height//rows
    # information on the cells in order to match the grid to the maze image
    self.enemies = []
    self.enemy_position = []
    self.player_position = None
    # where the player starts
    self.walls = []
    self.coins = []

    self.load()

    self.player = Player(self, copy.copy(self.player_position))

    self.make_enemies()


  def run(self):
    """Information on the state of the game, whether it is on the start screen or the actual game screen"""
    while self.running:
      if self.state == 'intro':
        self.intro_events()
        self.intro_update()
        self.intro_draw()
      # for when the game is first loaded up
      elif self.state == 'playing':
        self.playing_events()
        self.playing_update()
        self.playing_draw()
      # for when the actual game is occuring
      elif self.state == 'game over':
        self.game_over_events()
        self.game_over_update()
        self.game_over_draw()
      # for when it is a game over
      else:
        self.running = False
      self.clock.tick(FPS)
    pygame.quit()
    sys.exit()
  # calls to the intro screen state and to the actual playing state



  def draw_text(self, letters, screen, position, size, color, font_name, centered = False):
    """Says where the text used in the game goes"""
    font = pygame.font.Sysfont(font_name, size)
    text = font.render(letters, False, color)
    text_size = text.get_size()
    if centered:
      position[0] = position[0]-text_size[0]//2
      position[1] = position[1]-text_size[1]//2
    screen.blit(text, position)
  # specific information for the starting text on the intro screen like position
  # size, etc. 

  def load(self):
    """Loads in the maze image, the player, the enemies, walls, etc."""
    self.background = pygame.image.load('img/maze.png')
    self.background = pygame.transform.scale(self.background, (maze_width, maze_height))
    # to load in the maze background

    with open('walls.txt', 'r') as file:
    # opens up the file with the information on the walls of the maze
      for yidx, line in enumerate(file):
        # stores the lines as numbers, 1st row is yidx = 0, 2nd row = 1, etc. 
          for xidx, char in enumerate(line):
            if char == '1':
            # returns it back as a string 
              self.walls.append(vec(xidx, yidx))
              # creates a list with the position of the walls
            elif char == 'C':
              # for the coins that pac man collects
              self.coins.append(vec(xidx, yidx))
            elif char == 'P':
              self.player_postion = [xidx, yidx]
            elif char in ['2', '3', '4', '5']:
              self.enemy_position.append(vec(xidx, yidx))
            elif char == 'B':
              pygame.draw.rect(self.background, (0, 0, 0), (xidx*self.cell_width, yidx*self.cell_width, self.cell_width, self.cell_height))


  def make_enemies(self):
    for idx, position in enumerate(self.enemy_position):
      self.enemies.append(Enemy(self, vec(position), idx))


  def draw_grid(self):
    """Draws and describes a grid"""
    for x in range(width//self.cell_width):
      pygame.draw.line(self.background, (107, 107, 107), (x*self.cell_width, 0), (x*self.cell_width, height))
    for x in range(height//self.cell_height):
      pygame.draw.line(self.background, (107, 107, 107), (0, x*self.cell_height), (width, x*self.cell_height))
    # drawing lines in order to match up the path with the maze background

    # for coin in self.coins:
      # pygame.draw.rect(self.background, (165, 178, 42), (coin.x*self.cell_width, coin.y*self.cell_height, self.cell_width, self.cell_height))


  def reset(self):
    self.player.lives = 3
    self.player.current_score = 0
    self.player.grid_postition = vec(self.player.starting_position)
    self.player.pix_position = self.player.get_pix_position()
    self.player.direction *= 0
    for enemy in self.enemies:
        enemy.grid_pos = vec(enemy.starting_position)
        enemy.pix_position = enemy.get_pix_position()
        enemy.direction *= 0
  
    self.coins = []
    
    with open("src/walls.txt", 'r') as file:
        for yidx, line in enumerate(file):
            for xidx, char in enumerate(line):
                if char == 'C':
                    self.coins.append(vec(xidx, yidx))
    self.state = "playing"




  def intro_events(self):
    """What happens at the introduction screen"""
    for event in pygame.event.get():
    # to call the events that have happpened from the time it was last called
      if event.type == pygame.quit():
        self.running = 'False'
        # stops the game if the exit button is pressed 
      if event.type == pygame.keydown and event.key == pygame.k_space:
        self.state = 'playing'

  def intro_update(self):
    pass

  def intro_draw(self):
    """Visuals of the introduction screen"""
    self.screen.fill((0, 0, 0))
    self.draw_text('PUSH SPACEBAR TO START', self.screen, [width//2, height//2], 
                   start_text_size, (165, 130, 55), start_font, centered = True)
    self.draw_text('HIGH SCORE', self.screen, [2, 0], 
                   start_text_size, (255, 255, 255), start_font)
    pygame.display.update()
  # defines the intro screen and how it is set up 



  def playing_events(self):
    """Controls for the player"""
    for event in pygame.event.get():
      if event.type == pygame.quit():
        self.running = 'False'
      if event.type == pygame.keydown:
        if event.key == pygame.k_left:
          self.player.move(vec(-1, 0))
        if event.key == pygame.k_right:
          self.player.move(vec(1, 0))
        if event.key == pygame.k_up:
          self.player.move(vec(0, -1))
        if event.key == pygame.k_down:
          self.player.move(vec(0, 1))
  # the start of when the actual playing begins as well as the movement

  def playing_update(self):
    """Updates the information on the player and enemies"""
    self.player.update()
    for enemy in self.enemies:
      enemy.update()

    for enemy in self.enemies:
      if enemy.grid_postition == self.player.grid_postition:
        self.remove_life()

  def playing_draw(self):
    """Visuals for during the actual game, including a score keeeper"""
    self.screen.fill(0, 0, 0)
    self.screen.blit(self.background, (top_bottom_space//2, top_bottom_space//2))
    self.draw_coins()
    # to draw the coins on the actual screen instead of the background
    # self.draw_grid()
    # ^^ used to make a grid to ensure that the units move within the maze image/ testing purposes 
    self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, (255, 255, 255), start_font)
    self.draw_text('HIGH SCORE: 0', self.screen, [width//2, 0], 18, (255, 255, 255), start_font, 
                )
    self.player.draw()
    for enemy in self.enemies:
      enemy.draw()
    pygame.display.update()
  # to describe the layout of the playing screen with the maze

  
  def remove_life(self):
    """When the player loses a life and when they reach 0"""
    self.player.lives -= 1
    if self.player.lives == 0:
      self.state == 'game over'
    else:
      self.player.grid_postition = vec(self.player_position)
      self.player.pix_position = self.player.get_pix_position()
      self.player.direction *= 0
      for enemy in self.enemies:
        enemy.grid_postition = vec(enemy.starting_position)
        enemy.pix_position = enemy.get_pix_position()
        enemy.direction *= 0
      # resets both the player and the enemy when the player loses a life 


  def draw_coins(self):
    """Where the coins go"""
    for coin in self.coins:
      pygame.draw.circle(self.screen, (123, 123, 10),
       (int(coin.x*self.cell_width)+self.cell_width//2+top_bottom_space//2, int(coin.y*self.cell_height)+self.cell_height//2+top_bottom_space//2), 5)

  def game_over_events(self):
    """What happens when the player gets a 'game over'"""
    for event in pygame.event.get():
      if event.type == pygame.quit:
        self.running = False
      if event.type == pygame.keydown and event.key == pygame.k_space:
        self.reset()
      if event.type == pygame.keydown and event.key == pygame.k_escape:
        self.running = False

  def game_over_update(self):
    pass

  def game_over_draw(self):
    """The game over screen with different prompts for the player"""
    self.screen.fill(0, 0, 0)
    quit_text = "Press the escape button to quit"
    again_text = "Press SPACEBAR to PLAY AGAIN"
    self.draw_text("GAME OVER", self.screen, [width//2, 100],  52, (255, 0, 9), "arial", centered=True)
    self.draw_text(again_text, self.screen, [width//2, height//2],  36, (190, 190, 190), "arial", centered=True)
    self.draw_text(quit_text, self.screen, [width//2, height//1.5],  36, (190, 190, 190), "arial", centered=True)
    
    pygame.display.update()

