import pygame
from pygame.locals import *
from stats import Stats

class Entity:
	def __init__(self, game):
		self.game = game
		self.velocity = [0,0]
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/placeholder.png"), (self.game.tilemap.tile_size, self.game.tilemap.tile_size))
		self.rect = self.sprite.get_rect()
		self.onground = False
		self.direction = 1
		self.cpt_saut = 0
		self.stats = Stats()
		self.cpt_glide = self.stats.glide
		self.game.entities.append(self)
		self.type = "entity"

	def get_copy(self):
		copy = Empty()
		copy.onground = self.onground
		copy.rect = self.rect.copy()
		copy.velocity = self.velocity
		return copy

	def update(self):
		#Gestion Physique
		self.velocity[1] += self.game.gravity*self.game.dt
		#print(self.game.gravity)
		return self.velocity

	def draw(self, surf, offset):
		#Affichage
		rect = [self.rect.x + offset[0], self.rect.y + offset[1]]

		if self.direction != 1:
			img = pygame.transform.flip(self.sprite, True, False)
		else:
			img = self.sprite
		self.game.surf.blit(img, rect)

class Empty():
	pass