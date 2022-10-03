import pygame
import copy as cp
from pygame.locals import *

class Entity:
	def __init__(self, game):
		self.game = game
		self.velocity = [0,0]
		self.sprite = pygame.transform.scale(pygame.image.load("./assets/placeholder.png"), (self.game.tilemap.tile_size, self.game.tilemap.tile_size))
		self.rect = self.sprite.get_rect()
		self.onground = False
		self.color = None
		self.direction = 1
		self.game.entities.append(self)
		self.type = "entity"

	def get_copy(self):
		copy = Empty()
		copy.onground = self.onground
		copy.rect = cp.deepcopy(self.rect)
		copy.velocity = self.velocity
		return copy

	def update(self):
		#Gestion Physique
		self.velocity[1] += self.game.gravity
		if self.velocity[1] > self.rect.height:
			self.velocity[1] = self.rect.height - 1 #Cap de vitesse de chute = hauteur de l'entité -1
													#Permet d'éviter que l'entité ne touche aucun bord d'un mur
													#Empêchant de détecter de quel côté a eu lieu la collision
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