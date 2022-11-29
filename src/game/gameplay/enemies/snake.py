import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

class Snake(Entity): #Initialisé comme une entité
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		#Point de spawn de l'ennemi
		self.rect.x = x 
		self.rect.y = y
		#Vitesse aléatoire de l'ennemi
		self.stats.speed = 200
		#Chargement de l'image
		self.sprite = self.images.get("enemies/snake") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
		self.life = 200 #Vie de l'ennemi
		self.damage = 50 
		self.type = "snake" #Le type de l'entité / son nom.
		self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
		self.direction_hurt = 1
		#Compteurs
		self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
		self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre

	def update(self):
		if self.life > 0:
			if self.cd_hurt != 0:
				self.cd_hurt -= 1
				self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt
			else:
				if self.sprite == self.images.get("enemies/snake_hurt"):
					self.sprite = self.images.get("enemies/snake")
				if self.velocity[0] == 0: #S'il ne bouge plus (Coincé contre un bloc)
					self.direction *= -1
				if self.direction == 1: #S'il va à droite
					if not self.game.tilemap.getTileByCoor(self.rect.bottomright): #Tant qu'il n'a pas un petit bout dans le vide (Bas-droite)
						self.direction *= -1
				else: 
					if not self.game.tilemap.getTileByCoor(self.rect.bottomleft): #Tant qu'il n'a pas un petit bout dans le vide (Bas-gauche)
						self.direction *= -1
				
				self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse

		else: #Supprime si plus de vie			
			if not self.timer_disappear.running:
				self.sprite = self.images.get("enemies/snake_hurt")
				self.game.enemies.remove(self)
			self.timer_disappear.start()	
			self.velocity[0] = 0
			if self.timer_disappear.ended:
				self.game.entities.remove(self)
		
		Entity.update(self)
		return self.velocity


	def hurt(self, damage, hitter):
		self.sprite = self.images.get("enemies/snake_hurt")
		self.life -= damage
		if hitter.rect.x > self.rect.x:
			self.direction_hurt = -1
		else:
			self.direction_hurt = 1
		self.cd_hurt = 30