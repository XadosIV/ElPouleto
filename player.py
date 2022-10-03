import pygame
import copy as cp
from pygame.locals import *
from entity import Entity

class Player(Entity):
	def __init__(self, game, nb):
		Entity.__init__(self, game)
		self.jumpforce = 20
		self.rect.x = 736
		self.rect.y = 100
		self.game = game
		self.inventory = []
		self.nb_saut_bonus = 0
		self.cpt_saut = 0
		self.speed = 10
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
		self.type = "player"

	def update(self):
		if self.onground and self.velocity[1] >= 0:
			self.cpt_saut = 0

		#Controles
		keys = pygame.key.get_pressed()
		events = pygame.event.get()
		#Controles horizontaux
		if keys[K_q]:
			self.velocity[0] = -self.speed
			self.direction = -1
		elif keys[K_d]:
			self.velocity[0] = self.speed
			self.direction = 1
		else:
			self.velocity[0] = 0
		if keys[K_z] and self.onground:
			self.jump(False)

		#Controles Verticaux
		for event in self.game.events:
			if event.type == pygame.KEYDOWN and not self.onground:
				if event.key == K_z and self.cpt_saut < self.nb_saut_bonus:
					self.jump(True)

		Entity.update(self)

		return self.velocity

	def addBonus(self,item):
		for (k,v) in item["bonus"].items():
			setattr(self, k, getattr(self, k) + v)

	def jump(self, increment):
		self.velocity[1] = -self.jumpforce
		if increment:
			self.cpt_saut += 1

class Empty():
	pass