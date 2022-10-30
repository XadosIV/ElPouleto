import pygame
from entity import Entity

class Projectile(Entity):
	def __init__(self, game, owner, speed=1000):
		super().__init__(game)
		self.sprite = pygame.image.load("./assets/arrow.png")
		self.rect = self.sprite.get_rect()
		self.rect.x = owner.rect.x
		self.rect.y = owner.rect.y
		if owner.direction == -1:
			self.sprite = pygame.transform.flip(self.sprite, True, False)
		self.type = "projectile"
		self.velocity[0] = speed*self.game.dt * owner.direction

	def update(self):
		if self.velocity[0] == 0:
			self.delete()
		indices = self.rect.collidelistall(self.game.enemies)
		for i in indices:
			entity = self.game.enemies[i]
			entity.delete()
			self.delete()
		return self.velocity