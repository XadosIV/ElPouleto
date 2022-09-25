import pygame, csv, os

class Tile(pygame.sprite.Sprite):
	def __init__(self, image, x, y, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("./assets/"+image).convert()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x,y
		self.color = None
		self.game = game

	def draw(self, surface):
		if self.color != None:
			pygame.draw.rect(self.game.surf, self.color, self.rect)
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))