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
		self.stats.speed = 300
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
				if self.home.x - self.game.player.rect.x > 400 or self.game.player.rect.x - self.home.x > 400:
					if self.rect.x < self.home.x:
						self.direction = 1
					else:
						self.direction = -1
					self.velocity[0] = 0
				else:
					if self.rect.x == self.home.x and not self.timer_home.running:
						self.timer_home.start(reset=True)	
						print("yooo")			
					if self.rect.x < self.game.player.rect.x:
						self.direction = 1
					else:
						self.direction = -1
			
				self.damage = round(80 + self.game.player.stats.life * 0.1)
			
			if self.timer_home.running:
				self.velocity[0] = 0
			elif not self.timer_home.running and (not self.home.x - self.game.player.rect.x > 400 or not self.game.player.rect.x - self.home.x > 400):
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