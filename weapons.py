import pygame
from projectile import Projectile

class Weapon():
	def __init__(self, owner):
		self.owner = owner
		self.game = self.owner.game
		self.data = None
		self.weaponName = "peck"
		self.damage = 50

	def use(self):
		if self.weaponName == "peck":
			rect = pygame.Rect([1,1,1,1])
			rect.width = 40
			rect.height = self.owner.height
			if self.owner.direction == 1:
				rect.midleft = self.owner.rect.midright
			else:
				rect.midright = self.owner.rect.midleft
			t=rect.collidelistall(self.game.enemies)
			for index in t:
				enemy = self.game.enemies[index]
				enemy.hurt(self.damage, self.owner)
		elif self.weaponName == "bow":
			Projectile(self.game, self.owner, self.damage)