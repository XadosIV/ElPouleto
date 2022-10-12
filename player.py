import pygame
import copy as cp
from pygame.locals import *
from entity import Entity
from stats import Stats

class Player(Entity):
	def __init__(self, game, nb):
		Entity.__init__(self, game)
		self.rect.x = 736
		self.rect.y = 100
		self.game = game
		self.inventory = []
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size*self.stats.size,self.game.tilemap.tile_size*self.stats.size))
		self.type = "player"
		self.not_movable = 0

	def update(self):
		if self.not_movable > 0:
			self.not_movable -= self.game.dt
		if self.onground and self.velocity[1] >= 0:
			self.cpt_saut = 0

		#Controles
		keys = pygame.key.get_pressed()
		events = pygame.event.get()
		#Controles horizontaux
		if keys[K_q]:
			self.velocity[0] = -self.stats.speed*self.game.dt
			self.direction = -1
		elif keys[K_d]:
			self.velocity[0] = self.stats.speed*self.game.dt
			self.direction = 1
		else:
			self.velocity[0] = 0
		if keys[K_z]:
			if self.onground:
				self.jump(False)
			else:
				pass
		"""if keys[K_SPACE]:
			for item in self.inventory:
				if item['name'] == "PoussÃ©e d'Ã©nergie": #Problème avec les accents ptdr
					self.addBonus(item)
					#Wait 3 frames ?
					self.removeBonus(item)"""
		
		for item in self.inventory:
			if item['name'] == "PoussÃ©e d'Ã©nergie": #Problème avec les accents ptdr
				if keys[K_SPACE]:
					self.addBonus(item)
				else:
					self.removeBonus(item)

		#Controles Verticaux
		for event in self.game.events:
			if event.type == pygame.KEYDOWN and not self.onground:
				if event.key == K_z and self.cpt_saut < self.stats.jump_max-1:
					self.jump(True)

		Entity.update(self)
		self.updateSize(self.stats.size)

		return self.velocity

	def addBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) + bonus["val"])
			else:
				setattr(self.stats, bonus["var"], bonus["val"])

	def removeBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) - bonus["val"])
			else:
				setattr(self.stats, bonus["var"], self.stats.base_stats()[bonus["var"]])

	def jump(self, increment):
		self.velocity[1] = -self.stats.jumpforce*self.game.dt
		if increment:
			self.cpt_saut += 1		

	def updateSize(self, size):
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size*size,self.game.tilemap.tile_size*size))

class Empty():
	pass