import pygame
from pygame.locals import *
from entity import Entity, Stats

import random

class Fox(Entity):
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		self.rect.x = x
		self.rect.y = y
		self.stats.speed = 400
		self.damage = 130
		self.type = "fox"
		self.game.enemies.append(self)

	def update(self):
		if self.life > 0:
			if self.cd_hurt != 0:
				self.cd_hurt -= 1
				self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt
			else:
				if self.velocity[0] == 0: #S'il ne bouge plus (Coincé contre un bloc)
					self.direction *= -1
				if self.direction == 1: #S'il va à droite
					if not self.game.tilemap.getTileByCoor(self.rect.bottomright): #Tant qu'il n'a pas un petit bout dans le vide (Bas-droite)
						self.direction *= -1
				else: 
					if not self.game.tilemap.getTileByCoor(self.rect.bottomleft): #Tant qu'il n'a pas un petit bout dans le vide (Bas-gauche)
						self.direction *= -1
				
				self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse

			self.damage = 80 + self.game.player.stats.life * 0.1
			Entity.update(self)

		return self.velocity