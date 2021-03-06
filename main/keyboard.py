import pygame
from pygame.locals import *

class Keyboard(object):
  def __init__(self):
    self.on_esc = []
    self.on_space = []
    self.on_tab = []

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE:
        for f in self.on_esc: f()
      if e.type == KEYDOWN and e.key == K_SPACE:
        for f in self.on_space: f()
      if e.type == KEYDOWN and e.key == K_TAB:
        for f in self.on_tab: f()
