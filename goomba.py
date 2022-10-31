import pygame
import copy as cp
from pygame.locals import *
from entity import Entity, Stats

import random

class Goomba(Entity): #Initialisé comme une entité
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		#Point de spawn de l'ennemi
		self.rect.x = x 
		self.rect.y = y
		#Vitesse aléatoire de l'ennemi
		self.stats.speed = random.randint(250,350) 
		#Chargement de l'image
		self.sprite = pygame.image.load("./assets/goomba.png")		
		self.life = 200 #Vie de l'ennemi
		self.type = "goomba" #Le type de l'entité / son nom.
		self.game.enemies.append(self) #Ajout dans la liste d'ennemis

	def update(self):
		#Controles
		if self.life > 0:
			if self.direction == 1: #S'il va à droite
				if not self.game.getTile(self.rect.bottomright): #Tant qu'il n'a pas un petit bout dans le vide (Bas-droite)
					self.direction *= -1
			else: 
				if not self.game.getTile(self.rect.bottomleft): #Tant qu'il n'a pas un petit bout dans le vide (Bas-gauche)
					self.direction *= -1
			if self.velocity[0] == 0: #S'il ne bouge plus (Coincé contre un bloc)
				self.direction *= -1
			
			self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse

			Entity.update(self)
		else: #Supprime si plus de vie
			self.delete()
		return self.velocity
		
	