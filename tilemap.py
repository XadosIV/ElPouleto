import pygame, csv, os
from tile import Tile

class Tilemap():
	def __init__(self, game, filename):
		self.game = game
		self.tile_size = 32
		self.start_x, self.start_y = 0,0
		self.tiles = self.load_tiles("./assets/"+filename)
		self.map_surf = game.surf
		self.map_surf.set_colorkey((0,0,0))

	def read_csv(self, filename):
		map = []
		with open(os.path.join(filename)) as data:
			data = csv.reader(data, delimiter=",")
			for row in data:
				map.append(list(row))
		return map

	def load_tiles(self, filename):
		tiles = []
		map = self.read_csv(filename)
		x,y = 0,0
		for row in map:
			x = 0
			for tile in row:
				if tile == "0":
					self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
				elif tile == "1":
					tiles.append(Tile("underground.png", x*self.tile_size, y*self.tile_size, self.game, self.tile_size))
				elif tile == "2":
					tiles.append(Tile("ground.png", x*self.tile_size, y*self.tile_size, self.game, self.tile_size, noBottom=True))
				x+=1
			y+=1
		self.map_w, self.map_h = x*self.tile_size, y*self.tile_size
		return tiles