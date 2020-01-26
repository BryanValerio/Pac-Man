import pygame
import sys
from settings import *

pygame.init
vec = pygame.math.Vector2


class Base:
  def __init__(self):
    self.screen = pygame.diplay.set_mode((width, height))
    self.clock = pygame.time.Clock()
    # to control the FPS of the game when it runs 
    self.running = True
    self.state = 'intro'
  # initiates the game
    self.load()



  def run(self):
    while self.running:
      if self.state == 'intro':
        self.intro_events()
        self.intro_update()
        self.intro_draw()
      elif self.state == 'playing':
        self.playing_events()
        self.playing_update()
        self.playing_draw()
      else:
        self.running = False
      self.clock.tick(FPS)
    pygame.quit()
    sys.exit()
  # calls to the intro screen state and to the actual playing state



  def draw_text(self, letters, screen, position, size, color, font_name, 
                centered = False):
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
    


  def intro_events(self):
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
    self.screen.fill((0, 0, 0))
    self.draw_text('PUSH SPACEBAR TO START', self.screen, [width//2, height//2], 
                   start_text_size, (165, 130, 55), start_font, centered = True)
    self.draw_text('HIGHSCORE', self.screen, [2, 0], 
                   start_text_size, (255, 255, 255), start_font)
    pygame.display.update()
  # defines the intro screen and how it is set up 



  def playing_events(self):
    for event in pygame.event.get():
    # to call the events that have happpened from the time it was last called
      if event.type == pygame.quit():
        self.running = 'False'

  def playing_update(self):
    pass

  def playing_draw(self):
    self.screen.fill((0, 0, 0))
    pygame.display.update()