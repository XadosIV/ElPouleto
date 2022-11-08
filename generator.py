import pygame, csv, random
from goomba import Goomba

class Generator():
	def __init__(self, game, world, size=32): #map generator
		self.game = game
		self.world = world
		self.size = size

		self.path = f"./assets/worlds/{world}/"
		self.tileset = Tileset(self.path+"tileset.png")
		self.tilemap = Tilemap(size) #Contient tiles[] et tile_size
		
		self.start_x, self.start_y = 0,0 #Coordonnée de spawn du joueur
		self.enemies_coor = [] #Coordonnée où doivent spawn des ennemis
		self.items_coor = [] #Coordonnée où doivent spawn des items

		self.struct_spawned = []

		self.generate()
		self.spawns()

	def read_csv(self, file):
		tileId = []
		with open(self.path+file+".csv", "r") as data_raw:
			data = csv.reader(data_raw, delimiter=",")
			for row in data:
				tileId.append(list(row))
		return tileId

	def generate(self):
		tileId = self.read_csv("spawn")
		nb_struct = 4
		deb_tile = [0,16]
		for i in range(nb_struct):
			end_tiles = self.spawnStructure(tileId, coor=deb_tile)
			deb_tile = self.join(end_tiles[0])
			tileId = self.read_csv("structures/"+str(self.nextStruct()))
		
	def nextStruct(self):
		nb = random.randint(1,4)
		while nb in self.struct_spawned:
			nb = random.randint(1,4)
		self.struct_spawned.append(nb)
		return nb

	def join(self, deb):
		x,y = deb
		fin = [deb[0]+random.randint(15,25),deb[1]+random.randint(-3, 0)]
		segment = [fin[0]-deb[0], fin[1]-deb[1]]
		direction = [1 if segment[0] > 0 else -1, 1 if segment[1] > 0 else -1]		
		tileSurf = self.tileset.getSurf(5)
		if x > y:
			self.tilemap.tiles.append(Tile(tileSurf, x*self.size, y*self.size, self.game))
			while [x,y] != fin:
				x+=direction[0]
				distx = abs(fin[0]-x)
				disty = abs(fin[1]-y)
				self.tilemap.tiles.append(Tile(tileSurf, x*self.size, y*self.size, self.game))
				if y != fin[1]:
					if distx > disty:
						for i in range(min(2, disty)):
							if random.randint(1,4) == 1:
								y+=direction[1]
								self.tilemap.tiles.append(Tile(tileSurf, x*self.size, y*self.size, self.game))
					else:
						y+=direction[1]
						self.tilemap.tiles.append(Tile(tileSurf, x*self.size, y*self.size, self.game))
		return fin

	def join2(self, deb, fin):
		x,y = deb


	def spawnStructure(self, tileId, coor):
		if self.find_deb_tile(tileId):
			i,j = self.find_deb_tile(tileId)
			coor[1]-=i
		x,y = coor
		end_tiles = [] #Coordonnée des tuiles de sortie de la structure
		for row in tileId:
			x = coor[0]
			for tile in row:
				if tile == "0":
					#Coordonnée de spawn du joueur
					self.start_x, self.start_y = x * self.size, y * self.size
				elif tile == "1":
					self.items_coor.append( (x*self.size, y*self.size) )
				elif tile == "2":
					self.enemies_coor.append( (x*self.size, y*self.size) )
				elif tile == "4":
					end_tiles.append([x,y])
				elif tile != "-1" and tile != "3":
					tileSurf = self.tileset.getSurf(int(tile))
					noBottom = self.tileset.getNoBottom(int(tile))
					self.tilemap.tiles.append(Tile(tileSurf, x*self.size, y*self.size, self.game, noBottom=noBottom))
				x+=1
			y+=1
		self.tilemap.map_w, self.tilemap.map_h = 1000*self.size, 1000*self.size
		return end_tiles

	def find_deb_tile(self, tileId):
		for i in range(len(tileId)):
			for j in range(len(tileId[i])):
				if tileId[i][j] == "3":
					return [i,j]
		return []


	def spawns(self):
		for i in self.enemies_coor:
			Goomba(self.game, i[0], i[1])
		for i in self.items_coor:
			self.game.item_collection.spawnRandomItem(i[0], i[1])

class Tileset():
	def __init__(self, path, size=32):
		self.tileset = pygame.image.load(path) #Chargement de l'image tileset
		self.img_size = self.tileset.get_size()
		self.size = size
		self.rows = self.img_size[1]//size
		self.columns = self.img_size[0]//size
		self.tile_id = [] #Tableau ID => Surface pour chaque tuile
		self.noBottom_id = [] #Tableau ID => True/False noBottom
		self.load()

	def load(self):
		for row in range(self.rows):
			for column in range(self.columns):
				surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
				surf.convert_alpha()
				surf.blit(self.tileset, (0,0), (column*32,row*32,32,32))
				self.tile_id.append(surf)
				self.noBottom_id.append(row == self.rows-1)

	def getSurf(self, id):
		return self.tile_id[id]

	def getNoBottom(self, id):
		return self.noBottom_id[id]

class Tile():
	def __init__(self, surf, x, y, game, noBottom=False):
		self.game = game
		self.image = surf
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x,y
		self.type = "tile"
		self.noBottom = noBottom
		self.game.collisions.append(self)

	def draw(self, offset):
		self.game.surf.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

class Tilemap():
	def __init__(self, size):
		self.tiles = []
		self.tile_size = size
		self.map_w, self.map_h = 0,0