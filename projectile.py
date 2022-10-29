import pygame
from entity import Entity

class Projectile(Entity):
	def __init__(self, game, owner, speed=1000):
		super().__init__(game)
		self.rect = owner.rect
		self.type = "projectile"
		self.velocity[0] = speed*self.game.dt * owner.direction

	def update(self):
		return self.velocity