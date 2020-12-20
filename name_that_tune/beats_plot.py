import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class BeatsPlot(Shape):
  def __init__(self, beats, beats, width, height, parent=None):
    super().__init__(parent)
    #================#
    self.beats = beats
    self._background_color = pygame.Color('#AA0000')
    self._foreground_color = pygame.Color('#000080')  
    #================#
    self._surface = pygame.surface.Surface((width, height)).convert()

  def draw(self):
    self._draw_background()
    self._draw_beats()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._background_color)

  def _draw_beats(self):
    beats_total_time = self.beats[-1][1].time
    scale_x = self.width / beats_total_time
    middle_note_in_beats = math.floor(average([beat[0].note for beat in self.beats]))
    for beat in self._beats:
      beat_height = 50
      beat_width  = (beat[1].time - beat[0].time) * scale_x - 1
      beat_left   = beat[0].time * scale_x
      beat_top    = (middle_note_in_beats - beat[0].note) * beat_height + self.height / 2 - beat_height
      beat_key    = find(keys.items(), lambda x: x[1] == beat[0].note)[1][0]
      #=========#
      self._surface.blit(label(beat_key, self.foreground, self.background, (beat_width, beat_height)), (beat_left, beat_top))

  def _calculate_beat_key(self, beat):
    piano_keys = Piano.generate_keys_from_beats(self.beats)
    beat_key = find_value(piano_keys.items(), lambda x: x[1] == beat[0].note)
    

  
      