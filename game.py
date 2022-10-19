import pygame, copy
from enemy import Enemy
from entity import Entity
from player import Player
from item import Item, Collection
from tilemap import Tilemap
from camera import Camera
import random

class Game():
	def __init__(self, surf):
		self.gravity = 30
		self.surf = surf
		self.width = surf.get_width()
		self.height = surf.get_height()
		self.entities = []
		self.collisions = []
		self.enemies = []		
		self.tilemap = Tilemap(self, "testmap3.csv")
		self.player = Player(self, 1)
		self.items = []
		self.camera = Camera(self)
		Enemy(self, 300, 100)
		self.item_collection = Collection(self)
		self.item_collection.spawnItem(2, 1056, 200)
		self.item_collection.spawnItem(1, 544, 200)
		self.item_collection.spawnItem(0, 320, 200)
		for tile in self.tilemap.tiles:
			self.collisions.append(tile)
		

	def update(self, events, dt):
		self.events = events
		self.dt = dt/1000
		for entity in self.entities:
			velocity = entity.update()
			tab = self.split_velocity_cap(velocity, self.tilemap.tile_size//4)
			top_collision = False
			for t in tab:
				entity.rect = entity.rect.move(t[0], t[1])
				indices = entity.rect.collidelistall(self.collisions)
				for i in indices:
					bloc = self.collisions[i]
					side = self.side(entity, bloc.rect)
					if side == "top":
						top_collision = True
						entity.rect.bottom = bloc.rect.top
						for t in tab:
							t[1] = 0
						velocity[1] = 0
					elif side == "bottom":
						entity.rect.top = bloc.rect.bottom
						for t in tab:
							t[1] = 0
						velocity[1] = 0
					elif side == "left":
						entity.rect.right = bloc.rect.left
						for t in tab:
							t[0] = 0
						velocity[0] = 0
					elif side =="right":
						entity.rect.left = bloc.rect.right
						for t in tab:
							t[0] = 0
						velocity[0] = 0
			entity.onground = top_collision

		for item in self.items:
			item.check()

		self.camera.draw(self.surf, self.collisions, self.entities)

	def split_velocity_cap(self, velocity, maxi):
		#Entrée : velocity Vector2, maxi Int
		#Sortie : Array "t" de Vector2 tel que t[0] = t[1] = t[...] = t[len(t) - 1]

		#Permet de découper un vecteur en plusieurs vecteurs plus petits de façon optimale
		max_val = max([abs(velocity[0]), abs(velocity[1])])
		if max_val == 0:
			return [pygame.math.Vector2(0,0)]
		i=int(max_val//maxi)
		i = i if max_val%maxi == 0 else i+1
		vec = velocity // i
		total = vec*i
		t=[vec]*i
		manque_x = round(velocity[0] - total[0])
		manque_y = round(velocity[1] - total[1])
		t.append(pygame.math.Vector2(manque_x, manque_y))
		return t

	def getTile(self,coor):
		#Renvoie la tile ou False si il n'y en a pas aux coordonnées
		x,y = coor[0], coor[1]
		x=(x//self.tilemap.tile_size)*self.tilemap.tile_size
		y=(y//self.tilemap.tile_size)*self.tilemap.tile_size
		for body in self.tilemap.tiles:
			if body.rect.x == x and body.rect.y == y:
				return body
		return False

	def side(self, entity, body):
		topleft = body.collidepoint(entity.rect.topleft)
		topmid = body.collidepoint(entity.rect.midtop)
		topright = body.collidepoint(entity.rect.topright)
		botleft = body.collidepoint(entity.rect.bottomleft)
		botmid = body.collidepoint(entity.rect.midbottom)
		botright = body.collidepoint(entity.rect.bottomright)
		midright = body.collidepoint(entity.rect.midright)
		midleft = body.collidepoint(entity.rect.midleft)
		top = int(topleft) + int(topmid) + int(topright) if not self.getTile(body.bottomleft) else 0
		bot = int(botleft) + int(botright) + int(botmid) if not self.getTile((body.x,body.y-self.tilemap.tile_size)) else 0
		left = int(topleft) + int(midleft) + int(botleft) if not self.getTile(body.topright) else 0
		right = int(topright) + int(midright) + int(botright) if not self.getTile((body.x-self.tilemap.tile_size,body.y)) else 0

		forces = [top, bot, left, right]
		if max(forces) > 0:
			if top == max(forces):
				return "bottom"
			elif bot == max(forces):
				return "top"
			elif left == max(forces):
				return "right"
			elif right == max(forces):
				return "left"