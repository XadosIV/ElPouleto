import pygame
from pygame.locals import *
from entity import Entity
from stats import Stats
import os
from projectile import Projectile

class Player(Entity):
	def __init__(self, game, img_path="./assets/player/"):
		super().__init__(game)
		self.rect.x = 800
		self.rect.y = 200
		self.game = game
		self.inventory = []
		#Chargement des images
		self.width = None
		self.loadImg(img_path)
		self.updateDim()
		self.type = "player"
		self.interact = False
		self.invincible = 0
		self.gliding = False
		self.show_items = True
		self.cpt_frame = 0

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
			self.sprite = self.imgs["poulet0"]
			rect = self.sprite.get_rect()
			rect.bottom, rect.midbottom = self.rect.bottom, self.rect.midbottom
			self.rect = rect
		return (self.width, self.height)

	def update(self):
		if self.stats.life > 0:
			if self.invincible > 0:
				self.invincible -= 1

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
			#Verticaux
			if keys[K_z]:
				if self.onground:
					self.jump(False)

			has_jumped = False
			for event in self.game.events:
				if event.type == pygame.KEYDOWN:
					#Double saut
					if event.key == K_z and self.cpt_saut < self.stats.jump_max-1 and not self.onground and self.velocity[1] > 0:
						has_jumped = True
						self.jump(True)
				#Interaction
					if event.key == K_SPACE:
						Projectile(self.game, self)

					if event.key == K_e:
						self.interact = True
				if event.type == pygame.KEYUP:
					if event.key == K_e:
						self.interact = False

			#Planer
			if self.onground or not keys[K_z]:
				self.gliding = self.stats.glide

			if keys[K_z] and self.stats.glide != 0 and self.velocity[1] > 0 and not has_jumped:
				self.gliding -= self.game.dt

			#Dash
			for item in self.inventory:
				if self.game.item_collection.items.index(item) == 2:
					if keys[K_v] and self.stats.can_dash and self.velocity[0] != 0:
						self.stats.can_dash = False
						self.addBonus(item)
						self.game.defer(self.removeBonus, 90, item)
						self.game.defer(self.endCooldownDash, 3000)

			if self.invincible == 0:
				for enemy in self.game.enemies:
					if self.game.player.rect.colliderect(enemy):
						self.stats.life -= 100
						self.invincible = 60

			if self.gliding > 0 and self.gliding < self.stats.glide and self.velocity[1] >= 0:
				self.velocity[1] -= (self.game.gravity*0.8)*self.game.dt
			
			Entity.update(self)
		return self.velocity
		
	def updateSprite(self):
		self.cpt_frame += 1
		if self.cpt_frame == 16:
			self.cpt_frame = 0
		self.show_items = True
		if self.stats.life <= 0:
			self.sprite = self.imgs["dead"]
			self.show_items = False
		else:
			if not self.onground:
				self.sprite = self.imgs["glide"]
			else:
				if self.velocity[0] == 0:
					self.sprite = self.imgs["poulet0"]
				else:
					self.sprite = self.imgs["poulet"+str(self.cpt_frame//4)]

			if self.invincible != 0:
				if self.invincible % 6 in [0,5,4]: #3 premières frames + toutes les 3 frames
					self.sprite = self.imgs["blink"]
					self.show_items = False

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

	def get_item_sprite(self, name):
		if name in self.imgs.keys():
			return self.imgs[name]
		else:
			return self.imgs["item_ph"] #Renvoie un placeholder (image transparente) si pas d'image.

	def draw(self, offset):
		super().draw(offset)
		if self.show_items:
			rect = [self.rect.x + offset[0], self.rect.y + offset[1]]
			for item in self.inventory:
				img = self.get_item_sprite(item["sprite"])
				if self.direction != 1:
					img = pygame.transform.flip(img, True, False)
				self.game.surf.blit(img, rect)