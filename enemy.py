import pygame
import copy as cp
from pygame.locals import *
from entity import Entity, Stats

import random

class Enemy(Entity):
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		self.rect.x = x
		self.rect.y = y
		self.stats.speed = random.randint(250,350)
		self.type = "enemy"
		self.game.enemies.append(self)

	def update(self):
		#Controles
		if self.velocity[0] == 0 and random.randint(1,10) == 1:
			self.direction = -1
			if self.onground:
				self.jump()
		
		if random.randint(1,50) == 7:
			if self.onground:
				self.jump()

		if random.randint(1,50) == 42:
			self.direction *= -1

		if random.randint(1,50) == 27:
			self.stats.speed = random.randint(250,350)

		self.velocity[0] = self.stats.speed * self.direction * self.game.dt
		Entity.update(self)

		return self.velocity

class Empty():
	pass