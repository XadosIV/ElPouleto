import pygame
from pygame.locals import *
from stats import Stats

class Entity:
	def __init__(self, game):
		self.game = game
		self.velocity = pygame.math.Vector2([0,0])
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/placeholder.png"), (self.game.tilemap.tile_size, self.game.tilemap.tile_size))
		self.rect = self.sprite.get_rect()
		self.onground = False
		self.direction = 1
		self.cpt_saut = 0
		self.stats = Stats()
		self.game.entities.append(self)
		self.type = "entity"

	def update(self):
		#Gestion Physique
		self.velocity[1] += self.game.gravity*self.game.dt
		return self.velocity

	def draw(self, surf, offset):
		#Affichage
		rect = [self.rect.x + offset[0], self.rect.y + offset[1]]

		if self.direction != 1:
			img = pygame.transform.flip(self.sprite, True, False)
		else:
			img = self.sprite
		self.game.surf.blit(img, rect)

	def jump(self, increment=False):
		self.velocity[1] = -self.stats.jumpforce*self.game.dt
		if increment:
			self.cpt_saut += 1