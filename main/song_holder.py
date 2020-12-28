import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_entry import *

class SongHolder(Shape):
  def __init__(self, parent=None):
    super().__init__(parent)
    #================#
    self._song_entries = []
    self._space_between_song_entries = 15

  def add_song_entry(self, song_entry):
    song_entry.position = self._calculate_position_for_new_song_entry()
    song_entry.parent = self
    self._song_entries.append(song_entry)
    #================#
    self._rebuild_surface()

  def _calculate_position_for_new_song_entry(self):
    if len(self._song_entries) > 0:
      song_entry_position = tuple_math(self._song_entries[-1].parent_space_rect.bottomleft, '+', (0, self._space_between_song_entries))
      return song_entry_position
    else:
      return (0, 0)

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface((self._song_entries_max_width(), self._song_entries_total_height())).convert()
    self._surface.set_colorkey((0, 0, 0))
    
  def _song_entries_total_height(self):
    if len(self._song_entries) > 0:
      song_entries_total_height = sum([song_entry.parent_space_rect.height for song_entry in self._song_entries])
      song_entries_total_height_with_spaces = song_entries_total_height + self._space_between_song_entries * (len(self._song_entries) - 1)
      return song_entries_total_height_with_spaces
    else:
      return 0

  def _song_entries_max_width(self):
    if len(self._song_entries) > 0:
      return max([song_entry.parent_space_rect.width for song_entry in self._song_entries])
    else:
      return 0

  def draw(self):
    self._surface.fill((0, 0, 0))
    for song_entry in self._song_entries:
      self._surface.blit(song_entry.draw(), song_entry.parent_space_rect.topleft)
    return self._surface
    

  def process(self, events):
    for song_entry in self._song_entries:
      song_entry.process(events)

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_holder = SongHolder()
  song_holder.position = screen.get_rect().center
  song_holder.pivot = (0.5, 0.5)

  song_holder.add_song_entry(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_holder.add_song_entry(SongEntry('Sympathy For Devil', 'A2'))
  song_holder.add_song_entry(SongEntry('Another Break In The Wall', 'A3'))
  song_holder.add_song_entry(SongEntry('California Dreaming', 'B1'))
  song_holder.add_song_entry(SongEntry('No Woman No Cry', 'B2'))
  song_holder.add_song_entry(SongEntry('Voodoo Child', 'B3'))
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(song_holder.draw(), song_holder.world_space_rect.topleft)

    pygame.display.update()

      