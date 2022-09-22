import pygame
from entity import Entity
from platform import Platform
from tilemap import Tilemap
class Game():
	def __init__(self, surf):
		self.gravity = 1
		self.surf = surf
		self.entities = []
		self.platforms = []
		self.tilemap = Tilemap(self, "testmap1.csv")

	def update(self):
		if len(self.entities) == 0:
			self.entities.append(Entity(self))
			#self.platforms.append(Platform(self,100,100,100,100))
			#self.platforms.append(Platform(self,50,200,500,100))
			#self.platforms.append(Platform(self,600,350,200,100))
			for tile in self.tilemap.tiles:
				self.platforms.append(tile)
		for entity in self.entities:
			#print(f"{entity.rect.x},{entity.rect.y}")
			entity.update()
			platforms = self.platforms.copy()
			index = pygame.Rect.collidelist(entity.rect, platforms)
			print("--- frame ---")
			while index != -1:
				platform = platforms.pop(index)
				direction = self.determineSide(entity, platform.rect)
				if direction != "top":
					print(direction)
				if direction == "top":
					entity.onground = True
					entity.rect.y = platform.rect.midtop[1] - entity.rect.height
					entity.velocity[1] = 0
				elif direction == "bottom":
					entity.rect.y = platform.rect.midbottom[1]
					if not entity.onground:
						entity.velocity[1] = 0
				if direction == "left":
					entity.rect.x = platform.rect.midleft[0] - entity.rect.width
					entity.velocity[0] = 0
				elif direction == "right":
					entity.rect.x = platform.rect.midright[0]
					entity.velocity[0] = 0
				index = pygame.Rect.collidelist(entity.rect, platforms)
			if entity.velocity[1] != 0:
				entity.onground = False
		self.surf.fill((0,0,0))
		for platforms in self.platforms:
			platforms.draw(self.surf)
		for entity in self.entities:
			entity.draw()
		pygame.display.flip()

	def determineSide(self, entity, platform):
		#Résultat = côté de la platforme touché par l'entité

		#On regarde la collision avec la platform pour chaque côté de l'entité
		topleft_side = platform.collidepoint(entity.rect.topleft)
		topright_side = platform.collidepoint(entity.rect.topright)
		bottomleft_side = platform.collidepoint(entity.rect.bottomleft)
		bottomright_side = platform.collidepoint(entity.rect.bottomright)
		onground = entity.onground
		goingup = entity.velocity[1] < 0
		#Logique physique après simplification booléenne :

		if (topleft_side or topright_side) and (topleft_side or goingup) and (topright_side or goingup) and not (bottomleft_side) and not (bottomright_side):
			return "bottom"
		elif not (topleft_side) and not (bottomleft_side) and (topright_side or bottomright_side) and (topright_side or not (onground or not (goingup))) and (bottomright_side or not (goingup)): 
			return "left"
		elif not (topright_side) and not (bottomright_side) and (topleft_side or bottomleft_side) and (topleft_side or not (onground or not(goingup))) and (bottomleft_side or not (goingup)):
			return "right"
		else:
			return "top"


		#Note : ne pas être flemmard sur les calculs des collisions sur les côtés pour éviter le bug actuel quand on longe une plateforme
		#en sautant

		# => Vérifier à quel point l'entité est rentrée à chaque côté de la plateforme pour décider du sens de collision