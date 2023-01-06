import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer

import random

class Fox(Entity):
	def __init__(self, game, x, y):
		Entity.__init__(self, game)
		self.score = 100
		#Point de spawn de l'ennemi
		self.rect.x = x 
		self.rect.y = y
		#Vitesse
		self.stats.speed = 150
		#Chargement de l'image
		self.sprite = self.images.get("enemies/fox") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
		self.stats.life = 400 #Vie de l'ennemi
		self.damage = 130 #Dégats en fonction de la vie actuelle (Pour test), calculé dans l'update
		self.home = self.rect.copy()
		self.inHome = True
		self.type = "fox" #Le type de l'entité / son nom.
		self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
		self.direction_hurt = 1
		#Compteurs
		self.timer_home = Timer(30, self.game) #Temps avant que le renard sorte de son home
		self.timer_tooFar = Timer(30, self.game) #Temps avant que le renard se TP à son home 
		self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
		self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre

	def update(self):
		self.inHome=False
		if self.stats.life > 0: #S'il est en vie
			if self.cd_hurt != 0: #Si touché par le joueur
				self.cd_hurt -= 1
				self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt #Knockback
			else:
				vecRect = pygame.math.Vector2(self.rect.center) #Vecteur du fox
				vecPlayer = pygame.math.Vector2(self.game.player.rect.center) #Vecteur du joueur
				vecHome = pygame.math.Vector2(self.home.center) #Vecteur du home
				distHome = vecHome.distance_to(vecRect) #Distance des deux vecteurs
				distPlayer = vecPlayer.distance_to(vecRect) #Distance des deux vecteurs

				if self.rect.y != self.home.y and ((distHome > 400 and distPlayer > 400) or distPlayer > 400): #S'il sort de la range de chez lui ou du joueur
					if not self.timer_tooFar.running: #Timer start pour qu'il se TP quand il est trop loin trop longtemps
						self.timer_tooFar.start()
						self.direction *= -1
					if self.timer_tooFar.ended and self.timer_tooFar.running: #On TP le fox
						self.rect.center = self.home.center 
						self.velocity[0] = 0
						self.timer_tooFar.reset() #On reset le timer une fois que le fox est chez lui

				if vecHome.distance_to(vecPlayer) > 400: #Quand player pas dans la range
					self.timer_home.reset() #On reset le timer une fois que le joueur n'est plus dans la range

					if distHome < 16: # Range d'entrée dans le home
						self.rect.center = self.home.center
						self.velocity[0] = 0
						self.inHome = True
					else:
						if self.velocity[0] == 0 and self.onground: #Le faire sauter quand il rencontre un mur et quand il sort de sa tanière
							self.jump()
						if self.rect.y == self.home.y: #S'il est à la même hauteur que son home
							if self.rect.x < self.home.x: #Direction du home
								self.direction = 1
							else:
								self.direction = -1
							
						self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse
				else: #Quand player in range
					if not self.timer_home.running:
						self.timer_home.start()
					if self.rect.x < self.game.player.rect.x: #Direction vers le joueur
						self.direction = 1
					else:
						self.direction = -1
			
					self.damage = round(80 + self.game.player.stats.life * 0.1) #Dégats en fonction des PV actuels du joueur

					if not self.timer_home.ended:
						self.velocity[0] = 0 
					else:
						if abs(self.game.player.rect.x-self.rect.x) > 16:
							if self.onground and self.velocity[0] == 0:
								self.jump()
							self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse			

		else: #Supprime si plus de vie			
			if not self.timer_disappear.running: #Sprite de mort si life < 0
				self.sprite = self.images.get("enemies/fox_dead")
				self.game.enemies.remove(self)
				self.game.score += self.score
			self.timer_disappear.start()	
			self.velocity[0] = 0
			if self.timer_disappear.ended:
				self.game.entities.remove(self)

		return Entity.update(self)

	def hurt(self, damage, hitter):
		self.stats.life -= damage
		if hitter.rect.x > self.rect.x:
			self.direction_hurt = -1
		else:
			self.direction_hurt = 1
		self.cd_hurt = 30
		return self.velocity

	def draw(self, offset):
		#Draw Home and Fox only if not in Home
		if self.inHome:
			sprite = self.images.get("enemies/fox_home2")
		else:
			sprite = self.images.get("enemies/fox_home")
		rect = pygame.Rect(self.home.x,self.home.y, 32,32)
		rect=rect.move(offset)
		self.game.surf.blit(sprite, rect)
		if not self.inHome:
			super(Fox, self).draw(offset)
