import pygame
import copy as cp
from pygame.locals import *
from entity import Entity
from stats import Stats

class Player(Entity):
	def __init__(self, game, nb):
		Entity.__init__(self, game)
		self.rect.x = 800
		self.rect.y = 200
		self.game = game
		self.inventory = []
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size*self.stats.size,self.game.tilemap.tile_size*self.stats.size))
		self.type = "player"
		self.compteur = 1
		self.interact = False
		self.lifeLost = False
		self.blinking = False

	def update(self):
		if self.stats.lifebar > 0:
			if self.stats.lifebar > self.stats.lifemax:
				self.stats.lifebar = self.stats.lifemax
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
			
			#Dash
			for item in self.inventory:			
				if self.game.item_collection.items.index(item) == 2:
					if keys[K_SPACE] and self.stats.can_dash and self.velocity[0] != 0:
						self.stats.can_dash = False
						self.addBonus(item)
						self.game.defer(self.removeBonus, 90, item)
						self.game.defer(self.endCooldownDash, 3000)

			#Controles Verticaux
			for event in self.game.events:
				if event.type == pygame.KEYDOWN:
					if event.key == K_z and self.cpt_saut < self.stats.jump_max-1 and not self.onground:
						self.jump(True)
					if event.key == K_e:
						self.interact = True
				if event.type == pygame.KEYUP:
					if event.key == K_e:
						self.interact = False
			
			for enemy in self.game.enemies:
				if not self.lifeLost:
					self.losingLife(enemy)								

			self.updateSize(self.stats.size)
			Entity.update(self)

			if self.lifeLost and not self.blinking:
				self.blink(True)
				self.game.defer(self.blink, 500, False)				

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

	def updateSize(self, size):
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size*size,self.game.tilemap.tile_size*size))
		rect = self.sprite.get_rect()
		rect.bottom, rect.midbottom = self.rect.bottom, self.rect.midbottom
		self.rect = rect

	def endCooldownDash(self):
		self.stats.can_dash = True

	def losingLife(self, enemy):
		if self.game.player.rect.colliderect(enemy):
			self.lifeLost = True
			self.stats.lifebar -= 1
			self.game.defer(self.endCooldownLife, 2000)	
				
	def endCooldownLife(self):
		self.lifeLost = False
	
	def blink(self, val):
		if val:
			self.sprite = pygame.transform.scale(pygame.image.load("./assets/blink.png"), (self.game.tilemap.tile_size*self.stats.size,self.game.tilemap.tile_size*self.stats.size))
			self.blinking = True			
		else:
			self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size*self.stats.size,self.game.tilemap.tile_size*self.stats.size))
			self.blinking = False

class Empty():
	pass