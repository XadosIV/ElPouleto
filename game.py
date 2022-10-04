import pygame, copy
from enemy import Enemy
from entity import Entity
from player import Player
from item import Item
from tilemap import Tilemap
from camera import Camera
import random

class Game():
	def __init__(self, surf):
		self.gravity = 1
		self.surf = surf
		self.width = surf.get_width()
		self.height = surf.get_height()
		self.entities = []
		self.collisions = []		
		self.tilemap = Tilemap(self, "testmap3.csv")
		self.player = Player(self, 1)
		self.items = []
		self.camera = Camera(self)
		self.collisions.append(self.player)
		Enemy(self, 300, 100)
		for tile in self.tilemap.tiles:
			self.collisions.append(tile)
		self.items.append(Item(self, 800, 100, "./assets/spring.png", {
				"name":"Extension mécanique pour jambes de poulet (Compatible windows 7)",
				"bonus": {
					"nb_saut_bonus":1
				}
			}))
		self.items.append(Item(self, 880, 0, "./assets/wings.png",{
				"name":"Il plane",
				"bonus": {
					"jumpforce":8
				}
			}))

	def update(self, events):
		self.events = events		
		for entity in self.entities:
			velocity = entity.update()
			tab = self.split_velocity_cap([velocity[0],velocity[1]], self.tilemap.tile_size-1)
			for t in tab:
				entity.rect.x += t[0]
				entity.rect.y += t[1]
				collisions = self.collisions.copy()
				entity_origin = entity.get_copy()
				indices = entity.rect.collidelistall(collisions)
				for i in indices:
					body = collisions[i]
					if body == entity:
						continue
					elif body.type == "tile":
						direction = self.determineSide(entity_origin, body.rect)
						if direction == "top":
							coory = body.rect.midtop[1] - entity.rect.height
							if self.tileEmpty(body.rect.x, coory):
								entity.onground = True
								entity.rect.y = body.rect.midtop[1] - entity.rect.height
								entity.velocity[1] = 0
								for t in tab:
									t[1] = 0
						elif direction == "bottom":
							coory = body.rect.midbottom[1]
							if self.tileEmpty(body.rect.x, coory):
								entity.rect.y = body.rect.midbottom[1]
								if not entity.onground:
									entity.velocity[1] = 0
									for t in tab:
										t[1] = 0
						if direction == "left":
							coorx = body.rect.midleft[0] - entity.rect.width
							if self.tileEmpty(coorx, body.rect.y): 
								entity.rect.x = body.rect.midleft[0] - entity.rect.width
								entity.velocity[0] = 0
								for t in tab:
									t[0] = 0
						elif direction == "right":
							coorx = body.rect.midright[0]
							if self.tileEmpty(coorx, body.rect.y): 
								entity.rect.x = body.rect.midright[0]
								entity.velocity[0] = 0
								for t in tab:
									t[0] = 0
			if entity.velocity[1] != 0:
				entity.onground = False

		for item in self.items:
			item.check(self.player)

		self.camera.draw(self.surf, self.collisions, self.entities)

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

	def tileEmpty(self,x,y):
		#Renvoie True si plateforme libre
		x=(x//self.tilemap.tile_size)*self.tilemap.tile_size
		y=(y//self.tilemap.tile_size)*self.tilemap.tile_size
		booleen = True
		for body in self.collisions:
			if body.rect.x == x and body.rect.y == y:
				booleen = False
		return booleen

	def determineSide(self, entity, body):
		#Résultat = côté de la plateforme touché par l'entité

		#On regarde la collision avec la plateforme pour chaque côté de l'entité
		topleft_side = body.collidepoint(entity.rect.topleft)
		topright_side = body.collidepoint(entity.rect.topright)
		bottomleft_side = body.collidepoint(entity.rect.bottomleft)
		bottomright_side = body.collidepoint(entity.rect.bottomright)
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