import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_holder import *


class Scroll(Shape):
  
  def __init__(self, child):
    super().__init__()
    #================#
    self.child = child
    self._surface = pygame.surface.Surface((0, 0)).convert()
    self._surface.set_colorkey((0, 0, 0))
    #================#
    self._scroll_offset = (0, 0)
    self._scroll_step = 10

  @property
  def size(self):
    return self._surface.get_size()

  @size.setter
  def size(self, value):
    self._surface = pygame.surface.Surface(value).convert()
    self._surface.set_colorkey((0, 0, 0))

  def draw(self):
    self._surface.fill((0, 0, 0))
    self._surface.blit(self.child.draw(), self._scroll_offset)
    return self._surface
    
  def process(self, events):
    self.child.process(events)
    for e in events:
      if e.type == KEYDOWN and e.key == K_DOWN:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (0, -self._scroll_step))
      if e.type == KEYDOWN and e.key == K_UP:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (0, self._scroll_step))



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_holder_scroller = Scroll(SongHolder())
  song_holder_scroller.size = tuple_math(SCREEN_SIZE, '/', (1, 2))
  song_holder_scroller.position = screen.get_rect().center
  song_holder_scroller.pivot = (0.5, 0.5)

  song_holder_scroller.child.add_song_entry(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_holder_scroller.child.add_song_entry(SongEntry('Sympathy For Devil', 'A2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Another Break In The Wall', 'A3'))
  song_holder_scroller.child.add_song_entry(SongEntry('California Dreaming', 'B1'))
  song_holder_scroller.child.add_song_entry(SongEntry('No Woman No Cry', 'B2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Voodoo Child', 'B3'))
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()

    song_holder_scroller.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(song_holder_scroller.draw(), song_holder_scroller.world_space_rect.topleft)

    pygame.display.update()
