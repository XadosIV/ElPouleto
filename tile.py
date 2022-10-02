import pygame, csv, os

class Tile(pygame.sprite.Sprite):
	def __init__(self, image, x, y, game, tilesize):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pygame.transform.scale(pygame.image.load("./assets/"+image).convert(), (tilesize, tilesize))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x,y
		self.color = None
		
	def draw(self, surface):
		if self.color != None:
			pygame.draw.rect(self.game.surf, self.color, self.rect)
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))