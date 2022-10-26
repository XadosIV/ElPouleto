import pygame
from pygame.locals import *
from entity import Entity
from stats import Stats
import os

class Player(Entity):
	def __init__(self, game, img_path="./assets/player/"):
		Entity.__init__(self, game)
		self.rect.x = 800
		self.rect.y = 200
		self.game = game
		self.inventory = []
		#Chargement des images
		self.width = -1
		self.loadImg(img_path)
		self.updateDim()
		self.sprite = self.imgs["poulet"]

		self.type = "player"
		self.compteur = 1
		self.interact = False
		self.lifeLost = False

	def loadImg(self, path):
		self.imgs = {}
		for name in os.listdir(path):
			self.imgs[name.split(".")[0]] = pygame.image.load(path+name)

	def updateDim(self):
		if self.width != self.game.tilemap.tile_size*self.stats.size:
			self.width = self.game.tilemap.tile_size*self.stats.size
			self.height = self.game.tilemap.tile_size*self.stats.size
			for img in self.imgs:
				self.imgs[img] = pygame.transform.scale(self.imgs[img], (self.width, self.height))
			self.sprite = self.imgs["poulet"]
			rect = self.sprite.get_rect()
			rect.bottom, rect.midbottom = self.rect.bottom, self.rect.midbottom
			self.rect = rect
		return (self.width, self.height)

	def update(self):
		if self.stats.life > 0:
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

			Entity.update(self)

		return self.velocity
		
	def addBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) + bonus["val"])
			else:
				setattr(self.stats, bonus["var"], bonus["val"])
			if bonus["var"] == "size":
					self.updateDim()

	def removeBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) - bonus["val"])
			else:
				setattr(self.stats, bonus["var"], self.stats.base_stats()[bonus["var"]])

	def endCooldownDash(self):
		self.stats.can_dash = True

	def losingLife(self, enemy):
		if self.game.player.rect.colliderect(enemy):
			self.lifeLost = True
			self.stats.life -= 100
			self.game.defer(self.endCooldownLife, 2000)
			self.game.defer(self.blink, 100, False)
				
	def endCooldownLife(self):
		self.lifeLost = False
	
	def blink(self, val):
		if self.lifeLost:
			if val:
				self.sprite = pygame.transform.scale(pygame.image.load("./assets/player/blink.png"), self.updateDim())
			else:
				self.sprite = pygame.transform.scale(pygame.image.load("./assets/player/poulet.png"), self.updateDim())
			self.game.defer(self.blink, 100, not val)
		else:
			self.sprite = pygame.transform.scale(pygame.image.load("./assets/player/poulet.png"), self.updateDim())

class Empty():
	pass