import pygame
from projectile import Projectile
import weaponClasses

class WeaponManager():
	def __init__(self, owner):
		self.owner = owner
		self.data = None
		self.script = None
		self.owner.weapon = weaponClasses.__dict__["Peck"](self)

	def set(self, data):
		self.data = data
		self.script = self.data["script"]
		self.owner.weapon = weaponClasses.__dict__[self.script](self)