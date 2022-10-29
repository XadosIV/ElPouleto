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
			#déplacer cam à gauche
			self.offset[0] += (1 - (player_abs_pos[0]/(self.game.width*0.45))) * self.speed_max
		elif self.player.rect.x + self.offset[0] > (self.game.width*0.55):
			self.offset[0] -= ((player_abs_pos[0] - (self.game.width*0.55))/(self.game.width*0.45)) * self.speed_max
			#déplacer cam à droite
		if self.player.rect.y + self.offset[1] < self.game.height*0.45:
			self.offset[1] += (1 - (player_abs_pos[1]/(self.game.height*0.45))) * self.speed_max
		elif self.player.rect.y + self.offset[1] > (self.game.height*0.55):
			self.offset[1] -= ((player_abs_pos[1] - (self.game.height*0.55))/(self.game.height*0.45)) * self.speed_max

		#Limits
		if self.offset[0] > 0:
			self.offset[0] = 0
		if self.offset[0] < -(self.game.tilemap.map_w - self.game.width):
			self.offset[0] = -(self.game.tilemap.map_w - self.game.width)
		if self.offset[1] > 0:
			self.offset[1] = 0
		if self.offset[1] < -(self.game.tilemap.map_h - self.game.height):
			self.offset[1] = -(self.game.tilemap.map_h - self.game.height)

		self.surf.fill((135,206,235))

		item_infobulles = []
		for platform in platforms:
			platform.draw(self.offset)
		for entity in entities:
			if entity.type != "player":
				entity.draw(self.offset)
			if entity.type == "item":
				if entity.show_info:
					item_infobulles.append(entity.infobulle)
		for infobulle in item_infobulles:
			infobulle.draw(self.offset)

		self.player.updateSprite()
		self.player.draw(self.offset)
		pygame.draw.rect(self.surf, (70, 70, 70), [30, 30, 200, 30])
		pygame.draw.rect(self.surf, (255, 0, 0), [35, 35, 190*(self.game.player.stats.life/self.game.player.stats.lifemax), 20])
		pygame.display.flip()