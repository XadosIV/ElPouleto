import pygame
from pygame.locals import *
from src.game.gameplay.stats import Stats

class Entity:
	def __init__(self, game):
		self.game = game
		self.fall = 0
		self.images = self.game.galery
		self.velocity = pygame.math.Vector2([0,0]) #Vitesse de l'entité horizontalement/verticalement
		#Importation de l'image (De base c'est un carré rouge)
		self.sprite = pygame.image.load("resources/placeholder.png") 
		self.rect = self.sprite.get_rect() 
		self.onground = False
		self.flying = False #Définit si on doit lui appliquer une gravité ou non et si l'entité passe à travers les blocs transparents
		self.direction = 1 #Direction : 1 = Droite, -1 = Gauche
		self.cpt_saut = 0 #Compteur de saut de l'entité
		#Importation des stats
		self.stats = Stats() 
		self.game.entities.append(self) #Ajout dans la liste d'entités
		self.type = "entity" #Le type de l'entité / son nom.

	def update(self):
		#Gestion Physique
		if not self.flying:
			if self.velocity[1] > 1:
				self.onground = False #S'il est en l'air il est pas au sol
			self.fall += self.game.gravity*self.game.dt
			if self.fall >= 1:
				self.fall -= 1
				self.velocity[1] += 1
		return self.velocity

	def draw(self, offset):
		#Affichage
		if self.direction != 1: #Mettre dans le bon sens l'entité
			img = pygame.transform.flip(self.sprite, True, False)
		else:
			img = self.sprite
		self.game.surf.blit(img, self.rect.move(offset))

	def jump(self, increment=False): 
		#Saut
		self.onground = False
		self.velocity[1] = -self.stats.jumpForce
		if increment: #Pour plusieurs sauts
			self.cpt_saut += 1

	def delete(self):
		#Supprimer l'entité
		if self in self.game.entities:
			self.game.entities.remove(self)
		if self in self.game.enemies:
			self.game.enemies.remove(self)
		del self