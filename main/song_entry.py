import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class SongEntry(Shape):
  def __init__(self, name, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self.name = name
    #================#
    self._padding = (24, 48)
    #================#
    self.background_color = background_color
    self.text_color = text_color
    #================#
    self._song_name_font = pygame.font.Font('fonts/FSEX300.ttf', 24)
    self._rendered_song_name = self._song_name_font.render(self.name, False, self.text_color)
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())

  @property
  def padding(self):
    return self._padding

  @padding.setter
  def padding(self, value):
    self._padding = value
    self._surface = pygame.surface.Surface(self._calculate_surface_size())

  @property
  def inflate(self):
    return tuple_math(self._padding, '*', -1)
  
  def _calculate_surface_size(self):
    size_for_name = self._rendered_song_name.get_size()
    size_for_name_with_padding = tuple_math(size_for_name, '+', self._padding)
    return size_for_name_with_padding

  def process(self, events):
    pass

  def draw(self):
    self._draw_rect()
    self._draw_text()
    return self._surface

  def _draw_rect(self):
    self._surface.fill(self.background_color)
    pygame.draw.rect(self._surface, self.text_color, self._surface.get_rect(), 4)

  def _draw_text(self):
    self._surface.blit(self._rendered_song_name, self._song_name_position())

  def _song_name_position(self):
    surface_rect_padding_respect = self._surface.get_rect().inflate(self.inflate[0], self.inflate[1])
    song_name_rect = self._rendered_song_name.get_rect(center=surface_rect_padding_respect.center)
    return song_name_rect.topleft



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  song_entry = SongEntry('You Cant Always Get What You Want')
  song_entry.pivot = (0.5, 0.5)
  song_entry.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_entry.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_entry.draw(), song_entry.world_space_rect.topleft)
    pygame.display.update()
