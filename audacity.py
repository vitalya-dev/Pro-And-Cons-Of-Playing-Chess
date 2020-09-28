import threading
import struct
import wave
import pygame
from pygame.locals import *


#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE = 32
MAX_COLS = (int)(SCREEN_SIZE[0] / (FONT_SIZE / 2))
MAX_ROWS = (int)(SCREEN_SIZE[1] / FONT_SIZE)
#================================================================#


#================================================================#
pygame.init()
pygame.key.set_repeat(10, 75)
#================================================================#

#================================================================#
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
#================================================================#


#================================================================#
def linspace(start, stop, num=50):
  delta = stop - start
  div = num - 1
  step = delta / div
  return [start + i * step for i in range(num)]

def read_wav(filename):
    SIZES = {1: 'B', 2: 'h', 4: 'i'}
    CHUNK_SIZE_4096 = 4096
    CHUNK_SIZE_1 = 1
    #======================#
    wav_r = wave.open(filename, 'r')
    #======================#
    channels  = wav_r.getnchannels()
    sampwidth = wav_r.getsampwidth()
    #======================#
    fmt_1 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_4096
    fmt_2 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_1
    #======================#
    ret = []
    while wav_r.tell() < wav_r.getnframes():
      if wav_r.getnframes() - wav_r.tell() >= CHUNK_SIZE_4096:
        decoded = struct.unpack(fmt_1, wav_r.readframes(CHUNK_SIZE_4096))
      else:
        decoded = struct.unpack(fmt_2, wav_r.readframes(CHUNK_SIZE_1))
      for i in decoded: ret.append(i)
    return ret


def dim_in_pixels(cols, rows):
  return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)


def done(v=None):
  if not hasattr(done, 'val'): done.val = False
  if v == None: return done.val
  done.val = v;
  
def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val
#================================================================#


#================================================================#
def button(text, background, foreground):
  return font.render(text, False, pygame.Color(foreground), pygame.Color(background))

def label(text, foreground):
  return font.render(text, False, pygame.Color(foreground))
#================================================================#

class Window(object):
  def __init__(self, cols, rows, background):
    self.surface = pygame.surface.Surface(dim_in_pixels(cols, rows)).convert()
    self.background = pygame.Color(background)
    self.keys_down = pygame.key.get_pressed()
    self.draws = []

  def draw(self, s, c):
    self.draws.append({'surface': s, 'coord': c})

  def render(self):
    self.surface.fill(self.background)
    for d in self.draws:
      self.surface.blit(d['surface'], dim_in_pixels(*d['coord']))
    return self.surface

  def process(self, events):
    self.keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE and hasattr(self,  'on_esc'):    self.on_esc()
      if e.type == KEYDOWN and e.key == K_SPACE  and hasattr(self,  'on_space'):  self.on_space()

class Plot(object):
  def __init__(self, cols, rows, background, foreground):
    self.cols = cols
    self.rows = rows
    self.background = pygame.Color(background)
    self.foreground = pygame.Color(foreground)

  def plot(self, ys):
    surface = pygame.surface.Surface(dim_in_pixels(self.cols, self.rows)).convert()
    surface.fill(self.background)
    threading.Thread(target=self._plot_thread, args=(surface, ys,)).start()
    return surface

  def _plot_thread(self, surface, ys):
    normalize = self._normalize(ys)
    for x, y in zip(linspace(0, self.cols, len(ys)), ys):
      pygame.draw.line(surface, self.foreground, normalize(x, 0), normalize(x, y), 1)
    
  def _normalize(self, ys):
    scale_factor = (1/2 * self.rows) / max(abs(max(ys)), abs(min(ys)))
    return lambda x, y: dim_in_pixels(x, self.rows / 2 - y * scale_factor)
#================================================================#

if __name__ == '__main__':
  window = Window(MAX_COLS, MAX_ROWS, '#000080')
  window.on_esc = lambda: done(True)
  window.draw(Plot(MAX_COLS, MAX_ROWS, '#000080', 'green').plot(read_wav("Live Ouside Instrumental 2.wav")), (0, 0))

  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)    
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()
