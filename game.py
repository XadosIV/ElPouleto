import pygame, copy
from entity import Entity
from platform import Platform
from tilemap import Tilemap
class Game():
	def __init__(self, surf):
		self.gravity = 1
		self.surf = surf
		self.entities = []
		self.platforms = []
		self.tilemap = Tilemap(self, "testmap2.csv")

	def update(self):
		if len(self.entities) == 0:
			self.entities.append(Entity(self))
			for tile in self.tilemap.tiles:
				self.platforms.append(tile)
		for entity in self.entities:
			velocity = entity.update()
			tab = self.split_velocity_cap([velocity[0],velocity[1]], 15)
			for t in tab:
				entity.rect.x += t[0]
				entity.rect.y += t[1]
				platforms = self.platforms.copy()
				entity_origin = entity.get_copy()
				indices = entity.rect.collidelistall(platforms)
				for i in indices:
					platform = platforms[i]
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
		self.surf.fill((0,0,0))
		for platforms in self.platforms:
			platforms.draw(self.surf)
		for entity in self.entities:
			entity.draw()
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
		x=(x//self.tilemap.tile_size)*16
		y=(y//self.tilemap.tile_size)*16
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

		if platform.y == 16:
			print("---")
			print(f"X = {platform.x//16-1}")
			print(topleft_side)
			print(topright_side)
			print(bottomleft_side)
			print(bottomright_side)

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