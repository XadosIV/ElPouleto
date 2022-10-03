import pygame

class Camera():
	def __init__(self, game):
		self.game = game
		self.surf = self.game.surf
		self.player = self.game.player
		self.offset = [0,0]
		self.speed = 8

	def draw(self, surf, platforms, entities):
		if self.player.rect.x < self.game.width//4:
			self.offset[0] -= self.speed
			self.game.player.rect.x += self.speed
		elif self.player.rect.x > (self.game.width//4)*3:
			self.offset[0] += self.speed
			self.game.player.rect.x -= self.speed
		#self.offset[0] += self.game.player.velocity[0]
		#self.offset[1] += self.game.player.velocity[1]
		self.surf.fill((0,0,0))

		for platform in platforms:
			platform.draw(self.surf, self.offset)
		for entity in entities:
			entity.draw(self.surf, self.offset)

		pygame.display.flip()