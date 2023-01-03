from src.game.gameplay.projectile import Projectile
import pygame
from src.game.gameplay.utilities import Timer

#Classe abstraite
class Weapon():
	def __init__(self, weaponManager):
		self.weaponManager = weaponManager
		self.owner = weaponManager.owner
		self.data = weaponManager.data
		self.game = self.owner.game
		self.cd = Timer(20, self.game)

	def use(self):
		pass

class Peck(Weapon):
	def __init__(self, weaponManager):
		super(Peck, self).__init__(weaponManager)
		#Attaque de Cac définie par défaut lorsqu'aucune arme n'est équipée
		self.cd = Timer(5, self.game)
		self.damage = 50
		self.range = 40

	def use(self, direction=0):
		if self.cd.ended:
			self.getHitbox(direction) #Définit self.hitbox (Rect) et la place correctement au niveau du joueur
			colliders = self.hitbox.collidelistall(self.game.enemies)
			for index in colliders:
				enemy = self.game.enemies[index]
				enemy.hurt(self.damage, self.owner)
			self.cd.start(reset=True)

	def getHitbox(self, direction):
		if direction == 1:
			self.hitbox = pygame.Rect([1,1,self.owner.height,self.range+self.owner.width])
			self.hitbox.midbottom = self.owner.rect.midtop
		elif direction == -1:
			self.hitbox = pygame.Rect([1,1,self.owner.height,self.range+self.owner.width])
			self.hitbox.midtop = self.owner.rect.midbottom
		else:
			self.hitbox = pygame.Rect([1,1,self.range+self.owner.width,self.owner.height])
			if self.owner.direction == 1:
				self.hitbox.midleft = self.owner.rect.midleft
			else:
				self.hitbox.midright = self.owner.rect.midright



class Bow(Weapon):
	def __init__(self, weaponManager):
		super(Bow, self).__init__(weaponManager)
		self.damage = 100
		self.cd = Timer(20, self.game)

	def use(self, direction=0):
		if self.cd.ended:
			
			Projectile(self.owner, self.damage, direction)
			self.cd.start(reset=True)

class DoubleBow(Weapon):
	def __init__(self, weaponManager):
		super(DoubleBow, self).__init__(weaponManager)
		self.damage = 100
		self.cd = Timer(20, self.game)

	def use(self, direction=0):
		if self.cd.ended:
			if direction == 0:
				Projectile(self.owner, self.damage, direction, offset=(0,-5))
				Projectile(self.owner, self.damage, direction, offset=(0,5))
			else:
				Projectile(self.owner, self.damage, direction, offset=(-5,0))
				Projectile(self.owner, self.damage, direction, offset=(5,0))		
			self.cd.start(reset=True)