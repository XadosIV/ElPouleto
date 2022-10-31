import pygame
from entity import Entity

class Projectile(Entity): #Initialisé comme une entité
	def __init__(self, game, owner, speed=1000):
		super().__init__(game)
		self.sprite = pygame.image.load("./assets/arrow.png")
		self.rect = self.sprite.get_rect() 
		self.rect.x = owner.rect.x #Rectangle qui part des coordonnées du player
		self.rect.y = owner.rect.y
		if owner.direction == -1: #Changement de sens en foncion de sa direction
			self.sprite = pygame.transform.flip(self.sprite, True, False)
		self.type = "projectile"
		self.velocity[0] = speed*self.game.dt * owner.direction

	def update(self):
		if self.velocity[0] == 0: #S'il ne bouge plus (Coincé dans un bloc)
			self.delete()
		indices = self.rect.collidelistall(self.game.enemies) #Regarde si le projectile touche un ennemi
		for i in indices:
			entity = self.game.enemies[i]
			entity.life -= 100
			self.delete() #Enlève 100 PV à l'ennemi puis se supprime
		return self.velocity