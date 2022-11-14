import pygame
from entity import Entity

class Projectile(Entity): #Initialisé comme une entité
	def __init__(self, game, owner, damage, speed=1000):
		super().__init__(game)
		self.owner = owner
		#Importation de l'image
		self.sprite = pygame.image.load("./assets/arrow.png")
		self.rect = self.sprite.get_rect() 
		self.rect.x = self.owner.rect.x #Rectangle qui part des coordonnées du player
		self.rect.y = self.owner.rect.y
		#Changement de sens en foncion de sa direction
		self.damage = damage
		if owner.direction == -1: 
			self.sprite = pygame.transform.flip(self.sprite, True, False)
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