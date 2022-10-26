import pygame

class Camera():
	def __init__(self, game):
		self.game = game
		self.surf = self.game.surf
		self.player = self.game.player
		self.offset = [self.player.rect.x-720,self.player.rect.y]
		self.speed_max = self.game.tilemap.tile_size #32

	def draw(self, surf, platforms, entities):
		player_abs_pos = (self.player.rect.x + self.offset[0], self.player.rect.y + self.offset[1])
		if self.player.rect.x + self.offset[0] < self.game.width*0.45:
			#déplacer cam à gauche et player sur la droite absolue
			self.offset[0] += (1 - (player_abs_pos[0]/(self.game.width*0.45))) * self.speed_max
		elif self.player.rect.x + self.offset[0] > (self.game.width*0.55):
			self.offset[0] -= ((player_abs_pos[0] - (self.game.width*0.55))/(self.game.width*0.45)) * self.speed_max
			#déplacer cam à droite et player à gauche absolue
		if self.player.rect.y + self.offset[1] < self.game.height*0.45:
			self.offset[1] += (1 - (player_abs_pos[1]/(self.game.height*0.45))) * self.speed_max
		elif self.player.rect.y + self.offset[1] > (self.game.height*0.55):
			self.offset[1] -= ((player_abs_pos[1] - (self.game.height*0.55))/(self.game.height*0.45)) * self.speed_max
		self.surf.fill((135,206,235))

		for platform in platforms:
			platform.draw(self.surf, self.offset)
		for entity in entities:
			if entity.type != "player":
				entity.draw(self.surf, self.offset)
		self.player.draw(self.surf, self.offset)
		pygame.draw.rect(self.surf, (70, 70, 70), [50, 50, 150, 50])
		pygame.draw.rect(self.surf, (255, 0, 0), [55, 55, 140*(self.game.player.stats.life/self.game.player.stats.lifemax), 40])
		pygame.display.flip()