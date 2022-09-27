import pygame
import copy as cp
from pygame.locals import *

class Entity:
	def __init__(self, game):
		self.game = game
		self.velocity = [0,0]
		self.sprite = pygame.image.load("./assets/placeholder.png")
		self.rect = self.sprite.get_rect()
		self.rect.x = 100
		self.rect.y = 100
		self.jumpforce = 20
		self.onground = False

		self.debug = False

	def get_copy(self):
		copy = Empty()
		copy.onground = self.onground
		copy.rect = cp.deepcopy(self.rect)
		copy.velocity = self.velocity
		return copy

	def update(self):
		#Controles
		keys = pygame.key.get_pressed()
		if keys[K_f]:
			self.debug = not self.debug

		if keys[K_q]:
			self.velocity[0] = -5
		elif keys[K_d]:
			self.velocity[0] = 5
		else:
			self.velocity[0] = 0

		if self.debug:
			if keys[K_z]:
				self.velocity[1] = -5
			elif keys[K_s]:
				self.velocity[1] = 5
			else:
				self.velocity[1] = 0
		else:
			if keys[K_z] and self.onground:
				self.velocity[1] = -self.jumpforce

			#Gestion Physique
			self.velocity[1] += self.game.gravity
			if self.velocity[1] > self.rect.height:
				self.velocity[1] = self.rect.height - 1 #Cap de vitesse de chute = hauteur de l'entité -1
													#Permet d'éviter que l'entité ne touche aucun bord d'un mur
													#Empêchant de détecter de quel côté a eu lieu la collision

		return self.velocity
		
	def draw(self):
		#Affichage
		self.game.surf.blit(self.sprite, self.rect)

class Empty():
	pass