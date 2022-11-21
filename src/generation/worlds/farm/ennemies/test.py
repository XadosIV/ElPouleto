import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer

import random

class Fox(Entity):
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		#Point de spawn de l'ennemi
		self.rect.x = x 
		self.rect.y = y
		#Vitesse aléatoire de l'ennemi
		self.stats.speed = 250
		#Chargement de l'image
		self.sprite = self.images.get("enemies/goomba") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
		self.life = 400 #Vie de l'ennemi
		self.damage = 130 #Dégats en fonction de la vie actuelle (Pour test), calculé dans l'update
		self.home = self.rect
		self.type = "snake" #Le type de l'entité / son nom.
		self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
		self.direction_hurt = 1
		#Compteurs
		self.timer_home = Timer(60, self.game)
		self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
		self.disappear = 90 #Temps pendant lequel l'ennemi est mort avant de disparaitre

	def update(self):
		print(self.timer_home.running)
		if self.life > 0:
			if self.cd_hurt != 0:
				self.cd_hurt -= 1
				self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt
			else:		
				if (self.home.x - self.game.player.rect.x > 400 or self.game.player.rect.x - self.home.x > 400) and (self.home.y - self.game.player.rect.y > 200 or self.game.player.rect.y - self.home.y > 200):
					if self.rect.x == self.home.x:
						self.velocity[0] = 0
					if self.rect.x <= self.home.x:
						self.direction = 1
					else:
						self.direction = -1
				else:
					if self.rect.x == self.home.x and not self.timer_home.running:
						self.timer_home.start(reset=True)				
					if self.rect.x <= self.game.player.rect.x:
						self.direction = 1
					else:
						self.direction = -1
			
				self.damage = round(80 + self.game.player.stats.life * 0.1)

			"""if self.velocity[0] == 0 and (not self.home.x - self.game.player.rect.x > 400 or not self.game.player.rect.x - self.home.x > 400) and (not self.home.y - self.game.player.rect.y > 200 or not self.game.player.rect.y - self.home.y > 200): #S'il ne bouge plus et qu'on est proche de la tanière
				self.direction *= -1
			if self.direction == 1: #S'il va à droite
				if not self.game.tilemap.getTileByCoor(self.rect.bottomright): #Tant qu'il n'a pas un petit bout dans le vide (Bas-droite)
					self.direction *= -1
			else: 
				if not self.game.tilemap.getTileByCoor(self.rect.bottomleft): #Tant qu'il n'a pas un petit bout dans le vide (Bas-gauche)
					self.direction *= -1"""
			
			if self.timer_home.running:
				self.velocity[0] = 0
			elif not self.timer_home.running and (not self.home.x - self.game.player.rect.x > 400 or not self.game.player.rect.x - self.home.x > 400) and (not self.home.y - self.game.player.rect.y > 200 or not self.game.player.rect.y - self.home.y > 200):
				self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse
			Entity.update(self)

		else: #Supprime si plus de vie			
			if self.disappear == 90:
				self.sprite = pygame.transform.rotate(self.sprite, 90*self.direction_hurt)
				self.game.enemies.remove(self)
			self.disappear -= 1		
			self.velocity[0] = 0
			if self.disappear == 0:
				self.game.entities.remove(self)
		return self.velocity

	def hurt(self, damage, hitter):
		self.life -= damage
		if hitter.rect.x > self.rect.x:
			self.direction_hurt = -1
		else:
			self.direction_hurt = 1
		self.cd_hurt = 30
		return self.velocity