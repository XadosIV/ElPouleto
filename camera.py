import pygame

class Camera():
	def __init__(self, game):
		self.game = game
		self.surf = self.game.surf
		self.player = self.game.player
		self.offset = [0,0]
		self.speed = 8

	def draw(self, surf, platforms, entities):
		if self.player.rect.x + self.offset[0] < self.game.width//3:
			#déplacer cam à gauche et player sur la droite absolue
			self.offset[0] += self.speed
		elif self.player.rect.x + self.offset[0] > (self.game.width//3)*2:
			self.offset[0] -= self.speed
			#déplacer cam à droite et player à gauche absolue
		if self.player.rect.y + self.offset[1] < self.game.height // 3:
			self.offset[1] += self.speed
		elif self.player.rect.y + self.offset[1] > (self.game.height//3)*2:
			self.offset[1] -= self.speed
		self.surf.fill((0,0,0))

		for platform in platforms:
			platform.draw(self.surf, self.offset)
		for entity in entities:
			entity.draw(self.surf, self.offset)

		pygame.display.flip()