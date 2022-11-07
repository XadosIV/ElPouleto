import pygame

class Camera():
	def __init__(self, game):
		self.game = game
		self.surf = self.game.surf
		self.player = self.game.player
		self.offset = [0,-300]
		self.speed_max = 64

	def draw(self, surf, platforms, entities):
		player_abs_pos = (self.player.rect.x + self.offset[0], self.player.rect.y + self.offset[1])
		if self.player.rect.x + self.offset[0] < self.game.width*0.45:
			#déplacer cam à gauche
			self.offset[0] += (1 - (player_abs_pos[0]/(self.game.width*0.45))) * self.speed_max
		elif self.player.rect.x + self.offset[0] > (self.game.width*0.55):
			self.offset[0] -= ((player_abs_pos[0] - (self.game.width*0.55))/(self.game.width*0.45)) * self.speed_max
			#déplacer cam à droite
		if self.player.rect.y + self.offset[1] < self.game.height*0.45:
			#déplacer cam vers haut
			self.offset[1] += (1 - (player_abs_pos[1]/(self.game.height*0.45))) * self.speed_max
		elif self.player.rect.y + self.offset[1] > (self.game.height*0.55):
			#déplacer cam vers bas
			self.offset[1] -= ((player_abs_pos[1] - (self.game.height*0.55))/(self.game.height*0.45)) * self.speed_max
		
		self.offset[0] = round(self.offset[0],2)
		self.offset[1] = round(self.offset[1],2)
		#Limits
		if self.offset[0] < -(self.game.tilemap.map_w - self.game.width):
			self.offset[0] = -(self.game.tilemap.map_w - self.game.width)
		if self.offset[0] > 0:
			self.offset[0] = 0
		if self.offset[1] < -(self.game.tilemap.map_h - self.game.height):
			self.offset[1] = -(self.game.tilemap.map_h - self.game.height)
		if self.offset[1] > 0:
			self.offset[1] = 0

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

		self.player.draw(self.offset)

		pygame.display.flip()

#Au lieu d'une cam avec le poulet au centre : Le poulet est en bas de la caméra
#Quand appui sur S (sans appui sur espace) => Le poulet peut regarder vers le bas