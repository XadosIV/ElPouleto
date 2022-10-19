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
		self.dash = {"cooldown":0, "start_dash":self.compteur, "end_dash":-1}
		self.lifebar = 5
		self.lifeCooldown = 0
		self.lifeLost = False

	def update(self):
		if self.lifebar > 0:
			self.compteur -= self.game.dt
			if self.compteur < 0:
				self.compteur = 1
				if self.dash["cooldown"] != 0:
					self.dash["cooldown"] -= 1
				if self.lifeLost == True:
					self.lifeCooldown -= 1
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
					if keys[K_SPACE] and self.dash["cooldown"] == 0 and self.velocity[0] != 0:
						self.dash["start_dash"] = self.compteur
						self.dash["cooldown"] = item['cooldown']
						self.dash["end_dash"] = self.dash["start_dash"] - 2*self.game.dt
					if self.dash["end_dash"] != -1:
						if self.dash["end_dash"] < 0:
							self.dash["end_dash"] = 1 - self.dash["end_dash"]
						if self.dash["cooldown"] != 0 and self.dash["end_dash"] <= self.compteur:			
							self.addBonus(item)
						if self.dash["end_dash"] >= self.compteur:
							self.removeBonus(item)
							self.dash["end_dash"] = -1

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

			#self.losingLife(self.game.enemies)
			self.updateSize(self.stats.size)
			Entity.update(self)

			return self.velocity


	def addBonus(self,item):
		#self.updateSize(self.stats.size)
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

	def losingLife(self, enemies):
		for enemy in enemies:
			if self.game.player.rect.colliderect(enemy) and not self.lifeCooldown > 2:
				self.lifebar -= 1
				self.lifeLost = True
				print(self.lifebar)
			elif self.lifeCooldown > 2:
				self.lifeLost = False

class Empty():
	pass