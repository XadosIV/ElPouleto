import pygame
from entity import Entity
from platform import Platform

class Game():
	def __init__(self, surf):
		self.gravity = 1
		self.surf = surf
		self.entities = []
		self.platforms = []

	def update(self):
		if len(self.entities) == 0:
			self.entities.append(Entity(self))
			self.platforms.append(Platform(self,300,300,500,100))
			self.platforms.append(Platform(self,200,200,100,100))
		for entity in self.entities:
			entity.update()
			platforms = self.platforms.copy()
			index = pygame.Rect.collidelist(entity.rect, platforms)
			while index != -1:
				platform = platforms.pop(index)
				direction = self.determineSide(entity, platform.rect)
				if direction == "top":
					entity.onground = False
					entity.rect.y = platform.rect.midtop[1] - entity.rect.height
					entity.velocity[1] = 0
				elif direction == "bottom":
					entity.rect.y = platform.rect.midbottom[1]
					entity.velocity[1] = 0
				if direction == "left":
					entity.rect.x = platform.rect.midleft[0] - entity.rect.width
					entity.velocity[0] = 0
				elif direction == "right":
					entity.rect.x = platform.rect.midright[0]
					entity.velocity[0] = 0
				index = pygame.Rect.collidelist(entity.rect, platforms)

		self.surf.fill((0,0,0))
		for platforms in self.platforms:
			platforms.draw()
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

		#Si un des deux côtés du bas touche et qu'aucun des côtés du haut ne touche
		#C'est une collision verticale.
		if ((bottomleft_side or bottomright_side) and not (topleft_side) and not (topright_side)):
			return "top"

		elif ((bottomleft_side and topleft_side) and not (bottomright_side) and not (topright_side)):

			return "right"
			
		elif (bottomright_side and topright_side) and not (bottomleft_side) and not (topleft_side):
			return "left"

		elif (topleft_side and topright_side) and not (bottomleft_side) and not (bottomright_side):
			return "bottom"