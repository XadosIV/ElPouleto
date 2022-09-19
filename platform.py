import pygame
import random

class Platform:
	def __init__(self, game, centerx,centery, width, height):
		x = centerx - width//2
		y = centery - height//2
		self.rect = pygame.Rect(x,y,width,height)
		self.game = game

	def update(self):
		pass

	def draw(self):
		#Affichage
		#self.game.surf.blit(self.sprite, self.rect)
		pygame.draw.rect(self.game.surf, (0,0,255), self.rect)
		print("yo")