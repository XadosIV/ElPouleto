import pygame
from src.game.gameplay.entity import Entity

class Projectile(Entity): #Initialisé comme une entité
	def __init__(self, owner, damage, speed=1000, offset=(0,0)):
		super().__init__(owner.game)
		self.owner = owner
		#Importation de l'image
		self.sprite = self.images.get("items/arrow")
		self.rect = self.sprite.get_rect()
		if owner.direction == -1:
			self.sprite = pygame.transform.flip(self.sprite, True, False)
			self.rect.right = self.owner.rect.left + offset[0] #Rectangle qui part des coordonnées du player
		else:
			self.rect.left = self.owner.rect.right + offset[0] #Rectangle qui part des coordonnées du player

		self.rect.centery = self.owner.rect.centery + offset[1]
		#Changement de sens en foncion de sa direction
		self.damage = damage
		self.type = "projectile" #Le type de l'entité / son nom.
		self.velocity[0] = speed*self.game.dt * owner.direction #Vitesse dans la bonne direction direction du projectile 

	def update(self):
		if self.velocity[0] == 0: #S'il ne bouge plus il est supprimé (Coincé dans un bloc)
			self.delete()
		indices = self.rect.collidelistall(self.game.enemies) #Regarde si le projectile touche un ennemi
		for i in indices:
			entity = self.game.enemies[i]
			entity.hurt(self.damage,self.owner)
			self.delete() #Enlève "damage" PV à l'ennemi puis se supprime
		return self.velocity