import pygame
import copy as cp
from pygame.locals import *
from entity import Entity, Stats

import random

class Goomba(Entity):
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		self.rect.x = x
		self.rect.y = y
		self.stats.speed = random.randint(250,350)
		self.sprite = pygame.image.load("./assets/goomba.png")
		self.type = "goomba"
		self.game.enemies.append(self)

	def update(self):
		#Controles
		if self.direction == 1:
			if not self.game.getTile(self.rect.bottomright):
				self.direction *= -1
		else:
			if not self.game.getTile(self.rect.bottomleft):
				self.direction *= -1
		if self.velocity[0] == 0:
			self.direction *= -1
		
		self.velocity[0] = self.stats.speed * self.direction * self.game.dt

		Entity.update(self)

		return self.velocity