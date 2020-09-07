import os
import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
#================================================================#



#================================================================#
def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val


def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  btn.blit(font.render(text, False, pygame.Color('#000000')), (0, 0))
  return btn

def label(text, color):
  return font.render(text, False, color)
#================================================================#



#================================================================#
pygame.init()
pygame.key.set_repeat(10, 75)
#================================================================#


#================================================================#
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.Font('data/unispace bd.ttf', 32)
done = False
#================================================================#


#================================================================#
class Pathbar(object):
    def __init__(self):
        self.surface = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()

    def render(self):
      self.surface.fill(pygame.Color('#fefe03'))
      #=================#
      path = os.path.abspath(os.curdir) + "/"
      if len(path) > 30:
        path = ".." + path[-28:]
        self.surface.blit(label(path, pygame.Color('#000000')), (16, 0))
      #=================#
      return self.surface

    def process(self, e):
      pass

pathbar = Pathbar()
#================================================================#


#================================================================#
class Buttonbar(object):
    def __init__(self):
        self.surface = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()

    def render(self):
      self.surface.fill(pygame.Color('#000000'))
      #=================#
      self.surface.blit(label('X', pygame.Color('#fefe03')), (16 + 8, 0))
      self.surface.blit(button('Help'), (16 + 32, 0))

      self.surface.blit(label('Y', pygame.Color('#fefe03')), (176 + 8, 0))
      self.surface.blit(button('Menu'), (176 + 32, 0))

      self.surface.blit(label('B', pygame.Color('#fefe03')), (336 + 8, 0))
      self.surface.blit(button('Edit'), (336 + 32, 0))

      self.surface.blit(label('A', pygame.Color('#fefe03')), (496 + 8, 0))
      self.surface.blit(button('View'), (496 + 32, 0))
      #=================#
      return self.surface

    def process(self, e):
      pass

buttonbar = Buttonbar()
#================================================================#


#================================================================#
class Fpanel(object):
    def __init__(self):
        self.surface = pygame.surface.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] - 64)).convert()
        self.selection_bar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
        self.selection_index = 0
        self.flist = ['..'] + os.listdir(os.curdir)

    def render(self):
      self.surface.fill(pygame.Color('#0000a8'))
      self.selection_bar.fill(pygame.Color('#57ffff'))
      return self.surface

    def process(self, e):
      for e in events:
        if e.type == KEYDOWN and e.key == K_DOWN:
          self.selection_index += 1
        elif e.type == KEYDOWN and e.key == K_UP:
          self.selection_index -= 1
        elif e.type == KEYDOWN and e.key == K_RETURN and os.path.isdir(self.flist[self.selection_index]):
          os.chdir(self.flist[self.selection_index])
          self.flist = ['..'] + os.listdir(os.curdir)
          self.selection_index = 0
      #=================#
      self.selection_index %= len(self.flist)

    def __draw(self, surf, i):
      self.surface.blit(surf, (0, i * 32))


class Spanel(Fpanel):
  def __init__(self):
    super().__init__()
    self.scroll_area = [0, 12]
    self.scroll_index = 0
  
  def process(self, e):
    super().process(e)
    self.__scroll()

  def render(self):
    super().render()
    self.__draw(self.selection_bar, self.scroll_index)
    #=================#
    for i, f in enumerate(self.flist[self.scroll_area[0]:]):
      if i == scroll_index: self.__draw(label(f, pygame.Color('#000000')), i)
      else:                 self.__draw(label(f, pygame.Color('#57ffff')), i)
    #=================#
    return self.surface


  def __scroll(self):
    if self.selection_index < self.scroll_area[0]:
      self.scroll_area[0] = self.selection_index
      self.scroll_area[1] = self.scroll_area[0] + 12
    if self.selection_index > self.scroll_area[1]:
      self.scroll_area[1] = self.selection_index
      self.scroll_area[0] = self.scroll_area[1] - 12
    self.scroll_index = self.selection_index - self.scroll_area[0]
    

fpanel = Spanel()
#================================================================#
    
 


#================================================================#
while not done:
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  #=================#
  for e in events:
    if e.type == QUIT:
      done = True
    if e.type == KEYDOWN and e.key == K_ESCAPE:
      done = True
  #=================#
  pathbar.process(events)
  fpanel.process(events)
  buttonbar.process(events)
  #RENDER
  screen.fill(pygame.Color('#000000'))
  screen.blit(pathbar.render(), (0, 0))
  screen.blit(fpanel.render(), (0, 32))
  screen.blit(buttonbar.render(), (0, SCREEN_SIZE[1] - 32))
  #UPDATE
  pygame.display.update()
pygame.quit()
quit()
#================================================================#


