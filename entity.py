import pygame
from pygame.locals import *
from stats import Stats

class Entity:
	def __init__(self, game):
		self.game = game 
		self.velocity = pygame.math.Vector2([0,0]) #Vitesse de l'entité horizontalement/verticalement
		#Importation de l'image (De base c'est un carré rouge)
		self.sprite = pygame.image.load("./assets/placeholder.png") 
		self.rect = self.sprite.get_rect() 
		self.onground = False
		self.direction = 1 #Direction : 1 = Droite, -1 = Gauche
		self.cpt_saut = 0 #Compteur de saut de l'entité
		#Importation des stats
		self.stats = Stats() 
		self.game.entities.append(self) #Ajout dans la liste d'entités
		self.type = "entity" #Le type de l'entité / son nom.

	def update(self):
		#Gestion Physique
		if self.velocity[1] > 1:
			self.onground = False #S'il est en l'air il est pas au sol
		self.velocity[1] += self.game.gravity*self.game.dt #Fait tomber les entités
		return self.velocity

	def draw(self, offset):
		#Affichage
		rect = [self.rect.x + offset[0], self.rect.y + offset[1]] #Coordonnées du player en fonction de la caméra

		if self.direction != 1: #Mettre dans le bon sens l'entité
			img = pygame.transform.flip(self.sprite, True, False)
		else:
			img = self.sprite
		self.game.surf.blit(img, rect)

	def jump(self, increment=False): 
		#Saut
		self.onground = False
		self.velocity[1] = -self.stats.jumpforce*0.033 #Contrebalance la gravité pour faire sauter
		if increment: #Pour plusieurs sauts
			self.cpt_saut += 1

	def delete(self):
		#Supprimer l'entité
		self.game.entities.remove(self)
		if self in self.game.enemies:
			self.game.enemies.remove(self)
		del self