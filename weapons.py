import pygame
from projectile import Projectile

class Weapon():
	def __init__(self, owner):
		self.owner = owner
		self.game = self.owner.game
		self.weapon = self.owner.stats.weapons[0]
		self.damage = self.weapon["damage"]
		self.weaponName = self.weapon["name"]
	
	def change(self):
		indexNewWeapon = self.owner.stats.weapons.index(self.weapon) + 1
		if indexNewWeapon == len(self.owner.stats.weapons):
			indexNewWeapon = 0
		self.weapon = self.owner.stats.weapons[indexNewWeapon]
		self.damage = self.weapon["damage"]
		self.weaponName = self.weapon["name"]

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