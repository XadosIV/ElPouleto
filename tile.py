import pygame, csv, os

class Tile(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("./assets/"+image).convert()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x,y

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))