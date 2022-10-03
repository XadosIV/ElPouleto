import pygame

class Camera():
	def __init__(self, game):
		self.game = game
		self.player = self.game.player