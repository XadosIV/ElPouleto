import pygame
import math
from src.game.gameplay.entity import Entity

class Projectile(Entity): #Initialisé comme une entité
	def __init__(self, owner, damage, angle, speed=1000, offset=(0,0)):
		super().__init__(owner.game)
		self.owner = owner
		#Importation de l'image
		self.sprite = self.images.get("items/arrow")
		self.rect = self.sprite.get_rect()
		if angle >= -90 and angle <= 90:
			self.rect.left = self.owner.rect.left + offset[0] #Rectangle qui part des coordonnées du owner
		elif (angle <=180 and angle > 90) or (angle >=-180 and angle < -90):
			self.rect.right = self.owner.rect.right + offset[0] #Rectangle qui part des coordonnées du owner
		self.sprite = pygame.transform.flip(pygame.transform.rotate(self.sprite, angle), True, False)
		if self.owner == self.game.player:
			if angle == 90 or angle == -270 or angle == -90 or angle == 270:
				self.sprite = pygame.transform.flip(self.sprite, False, True)
				

		self.rect.centery = self.owner.rect.centery + offset[1]
		#Changement de sens en foncion de sa direction
		self.damage = damage
		self.type = "projectile" #Le type de l'entité / son nom.
		if angle == 0:
			self.velocity[0] = -(speed*self.game.dt) #Vitesse dans la bonne direction direction du projectile 
		elif angle == 180 or angle == -180:
			self.velocity[0] = speed*self.game.dt #Vitesse dans la bonne direction direction du projectile 
		elif angle == 90 or angle == -270:
			self.velocity[1] = speed*self.game.dt #Vitesse dans la bonne direction direction du projectile 
		elif angle == -90 or angle == 270:
			self.velocity[1] = -(speed*self.game.dt) #Vitesse dans la bonne direction direction du projectile 
		else:
			self.velocity[0] = -(speed*self.game.dt * (math.cos(angle/(360/(math.pi*2))))) #Vitesse dans la bonne direction direction du projectile 
			self.velocity[1] = -(speed*self.game.dt * (math.sin(angle/(360/(math.pi*2)))))


	def update(self):
		if self.velocity == [0,0] or self.rect.inflate((1,1)).collidelistall(self.game.collisions): #S'il ne bouge plus il est supprimé (Coincé dans un bloc)
			self.delete()
		if self.owner == self.game.player:
			indices = self.rect.collidelistall(self.game.enemies) #Regarde si le projectile touche un ennemi
			for i in indices:
				entity = self.game.enemies[i]
				entity.hurt(self.damage, self.owner)
				self.delete() #Enlève "damage" PV à l'ennemi puis se supprime
		else:
			indices = self.rect.collidelistall([self.game.player]) #Regarde si le projectile touche le joueur
			for i in indices:
				entity = self.game.player
				entity.hurt(self.damage)
				self.delete() #Enlève "damage" PV à l'ennemi puis se supprime
			
		return self.velocity