import pygame, copy
from enemy import Enemy
from entity import Entity
from player import Player
from item import Item
from tilemap import Tilemap
import random

class Game():
	def __init__(self, surf):
		self.gravity = 1
		self.surf = surf
		self.entities = []
		self.platforms = []		
		self.tilemap = Tilemap(self, "testmap3.csv")
		self.player = Player(self, 1)
		self.objects = []
		self.indiceObject = 0
		self.platforms.append(self.player)
		self.platforms.append(Enemy(self, 300, 100))	
		for tile in self.tilemap.tiles:
			self.platforms.append(tile)
		#self.objectsNotGet.append(Item(self, 800, 100))

		#self.objectsNotGet.append(Item(self, 880, 0))

	def update(self, events):
		self.events = events		
		for entity in self.entities:
			velocity = entity.update()
			tab = self.split_velocity_cap([velocity[0],velocity[1]], self.tilemap.tile_size-1)
			for t in tab:
				entity.rect.x += t[0]
				entity.rect.y += t[1]
				platforms = self.platforms.copy()
				entity_origin = entity.get_copy()
				indices = entity.rect.collidelistall(platforms)
				for i in indices:
					platform = platforms[i]
					if platform == entity:
						continue
					direction = self.determineSide(entity_origin, platform.rect)
					if direction == "top":
						coory = platform.rect.midtop[1] - entity.rect.height
						if not self.test_platform_coor(platform.rect.x, coory):
							continue
						else:
							entity.onground = True
							platform.color = (255,255,50)
							entity.rect.y = platform.rect.midtop[1] - entity.rect.height
							entity.velocity[1] = 0
							for t in tab:
								t[1] = 0
					elif direction == "bottom":
						coory = platform.rect.midbottom[1]
						if not self.test_platform_coor(platform.rect.x, coory):
							continue
						else:
							platform.color = (50,255,50)
							entity.rect.y = platform.rect.midbottom[1]
							if not entity.onground:
								entity.velocity[1] = 0
								for t in tab:
									t[1] = 0
					if direction == "left":
						coorx = platform.rect.midleft[0] - entity.rect.width
						if not self.test_platform_coor(coorx, platform.rect.y): 
							continue
						else:
							platform.color = (255,50,255)
							entity.rect.x = platform.rect.midleft[0] - entity.rect.width
							entity.velocity[0] = 0
							for t in tab:
								t[0] = 0
					elif direction == "right":
						coorx = platform.rect.midright[0]
						if not self.test_platform_coor(coorx, platform.rect.y): 
							continue
						else:
							platform.color = (50,255,255)
							entity.rect.x = platform.rect.midright[0]
							entity.velocity[0] = 0
							for t in tab:
								t[0] = 0
			if entity.velocity[1] != 0:
				entity.onground = False
		
		for item in self.objectsNotGet:			
			if self.player.rect.x == item.rect.x and self.player.rect.y == item.rect.y:
				item.updateTaken()
			if item.taken == True:
				self.objectsGet.append(item)
				self.objectsNotGet.pop(self.indiceObject)
			self.indiceObject += 1
			print(self.objectsGet)

		self.surf.fill((0,0,0))
		for platforms in self.platforms:
			platforms.draw(self.surf)
		for entity in self.entities:
			entity.draw(self.surf)

		self.indiceObject = 0
		pygame.display.flip()

	def split_velocity_cap(self, velocity, maxi):
		t = []
		while velocity != [0,0]:
			if velocity[0] > 0:
				x = min(velocity[0], maxi)
			else:
				x = max(velocity[0], -maxi)
			if velocity[1] > 0:
				y = min(velocity[1], maxi)
			else:
				y = max(velocity[1], -maxi)
			velocity[0] -= x
			velocity[1] -= y
			t.append([x,y])
		return t

	def test_platform_coor(self,x,y):
		#Renvoie True si plateforme libre
		x=(x//self.tilemap.tile_size)*self.tilemap.tile_size
		y=(y//self.tilemap.tile_size)*self.tilemap.tile_size
		booleen = True
		for platform in self.platforms:
			if platform.rect.x == x and platform.rect.y == y:
				booleen = False
		return booleen

	def determineSide(self, entity, platform):
		#Résultat = côté de la platforme touché par l'entité

		#On regarde la collision avec la platform pour chaque côté de l'entité
		topleft_side = platform.collidepoint(entity.rect.topleft)
		topright_side = platform.collidepoint(entity.rect.topright)
		bottomleft_side = platform.collidepoint(entity.rect.bottomleft)
		bottomright_side = platform.collidepoint(entity.rect.bottomright)
		onground = entity.onground
		goingup = entity.velocity[1] < 0

		#Si deux côtés du bas touche et qu'aucun des côtés du haut ne touche
		#C'est une collision sur le haut de la plateforme.
		if ((bottomleft_side and bottomright_side) and not (topleft_side) and not (topright_side)):
			return "top"

		#Par raisonnement inverse, on détecte la collision du bas.
		elif (topleft_side and topright_side) and not (bottomleft_side) and not (bottomright_side):
			return "bottom"

		#Idem sur les côtés, si on a un côté de l'entité entièrement dans la plateforme et l'autre côté pas du tout, on trouve les collisions
		elif ((bottomleft_side and topleft_side) and not (bottomright_side) and not (topright_side)):
			return "right"
			
		elif (bottomright_side and topright_side) and not (bottomleft_side) and not (topleft_side):
			return "left"

		#Gestion des coins

		#bas droit de l'entité touche
		elif bottomright_side and not bottomleft_side and not topleft_side and not topright_side:
			if entity.onground or not goingup:
				return "top"
			else:
				return "left"

		#bas gauche de l'entité touche
		elif bottomleft_side and not bottomright_side and not topleft_side and not topright_side:
			if entity.onground or not goingup:
				return "top"
			else:
				return "right"

		#haut droit de l'entité touche
		elif topright_side and not bottomleft_side and not topleft_side and not bottomright_side:
			if goingup: #Si il monte/saute
				return "bottom"
			else:
				return "left"

		#haut gauche de l'entité touche
		elif topleft_side and not bottomleft_side and not topright_side and not bottomright_side:
			if goingup: #Si il monte/saute
				return "bottom"
			else:
				return "right"

		else:
			#Si il est dans la plateforme, on bidouille en mettant par défaut qu'il arrive sur la plateforme.
			return "top"