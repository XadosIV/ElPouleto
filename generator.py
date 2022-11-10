import pygame, csv, random
from goomba import Goomba

class Generator():
	def __init__(self, game, world, size=32): #map generator
		self.game = game
		self.world = world
		self.size = size

		self.path = f"./assets/worlds/{world}/"
		self.tileset = Tileset(self.path+"tileset.png")
		self.tilemap = Tilemap(self) #Contient tiles[] et tile_size
		
		self.start_x, self.start_y = 0,0 #Coordonnée de spawn du joueur
		self.enemies_coor = [] #Coordonnée où doivent spawn des ennemis
		self.items_coor = [] #Coordonnée où doivent spawn des items

		self.struct_spawned = []

		self.generate()
		self.spawns()
		self.optimize()

	def optimize(self):
		#Retire des collisions tout les blocs touchant d'autres blocs de tout les côtés, inutile de les compter
		#dans les collisions puisque celles-ci n'arriveront jamais.
		#Ces tuiles seront mises en déco pour être quand même affiché
		for tile in self.tilemap.tiles:
			up = self.tilemap.getTileId(tile.x, tile.y-1)
			down = self.tilemap.getTileId(tile.x, tile.y+1)
			left = self.tilemap.getTileId(tile.x-1, tile.y)
			right = self.tilemap.getTileId(tile.x+1, tile.y)
			upleft = self.tilemap.getTileId(tile.x-1, tile.y-1)
			upright = self.tilemap.getTileId(tile.x+1, tile.y-1)
			downleft = self.tilemap.getTileId(tile.x-1, tile.y+1)
			downright = self.tilemap.getTileId(tile.x+1, tile.y+1)
			if up == down == left == right == upleft == upright == downleft == downright:
				if up != -1:
					tile.deco = True
					self.game.collisions.remove(tile)
					self.tilemap.deco.append(tile)

	def read_csv(self, file):
		tileId = []
		with open(self.path+file+".csv", "r") as data_raw:
			data = csv.reader(data_raw, delimiter=",")
			for row in data:
				tileId.append(list(row))
		return tileId

	def join2(self, deb, fin):
		ground_id = 5
		x,y = deb
		xend,yend = fin
		while [xend,yend] != [x,y]:
			distance = [xend-x, yend-y]
			self.tilemap.add(ground_id, x, y)
			x+=1

	def generate(self):
		self.join2([0,27], [45,27])
		tileId = self.read_csv("spawn")
		nb_struct = 4
		deb_tile = [0,30]
		end_tiles = self.spawnStructure(tileId, coor=deb_tile)
		deb_tile = [end_tiles[0][0]-1,end_tiles[0][1]]
		for i in range(nb_struct):
			tileId = self.read_csv("structures/"+str(self.nextStruct()))
			end_tiles = self.spawnStructure(tileId, coor=deb_tile)
			deb_tile = [end_tiles[0][0]-1,end_tiles[0][1]]
		tileId = self.read_csv("end")
		self.spawnStructure(tileId, coor=deb_tile)
		self.fill()

	def fill(self):
		map = self.tilemap.map
		for x in range(len(map[0])):
			tile = map[len(map)-1][x]
			if tile == -1:
				self.fillUp(x, len(map)-1)

	def fillUp(self, x, y):
		if y == -1:
			return -1
		tile = self.tilemap.map[y][x]
		if tile == -1:
			nextTile = self.fillUp(x, y-1)
			if self.tileset.getNoBottom(nextTile):
				return -1
			else:
				self.tilemap.add(nextTile, x, y)

				return nextTile
		else:
			return tile

	def nextStruct(self):
		nb = random.randint(1,4)
		while nb in self.struct_spawned:
			nb = random.randint(1,4)
		self.struct_spawned.append(nb)
		return nb

	def join(self, deb):
		x,y = deb
		fin = [deb[0]+random.randint(5,15),deb[1]+random.randint(-3, 0)]
		segment = [fin[0]-deb[0], fin[1]-deb[1]]
		direction = [1 if segment[0] > 0 else -1, 1 if segment[1] > 0 else -1]		
		ground_id = 5
		if x >= y:
			self.tilemap.add(ground_id, x, y)
			while [x,y] != fin:
				x+=direction[0]
				distx = abs(fin[0]-x)
				disty = abs(fin[1]-y)
				self.tilemap.add(ground_id, x, y)
				if y != fin[1]:
					if distx > disty:
						for i in range(min(2, disty)):
							if random.randint(1,4) == 1:
								y+=direction[1]
								self.tilemap.add(ground_id, x, y)
					else:
						y+=direction[1]
						self.tilemap.add(ground_id, x, y)
		return fin

	def spawnStructure(self, tileId, coor):
		if self.find_deb_tile(tileId):
			i,j = self.find_deb_tile(tileId)
			coor[1]-=i
		x,y = coor
		end_tiles = [] #Coordonnée des tuiles de sortie de la structure
		decoid = 15
		for row in tileId:
			x = coor[0]
			for tile in row:
				if tile == "0":
					#Coordonnée de spawn du joueur
					self.start_x, self.start_y = x * self.size, y * self.size
					id = self.complete(tileId, x, y, coor)
					self.tilemap.add(id, x, y)
				elif tile == "1":
					self.items_coor.append( (x*self.size, y*self.size) )
					id = self.complete(tileId, x, y, coor)
					self.tilemap.add(id, x, y)
				elif tile == "2":
					self.enemies_coor.append( (x*self.size, y*self.size) )
					id = self.complete(tileId, x, y, coor)
					self.tilemap.add(id, x, y)
				elif tile == "4":
					end_tiles.append([x,y])
				elif tile != "-1" and tile != "3":
					self.tilemap.add(int(tile), x, y)
					if self.tileset.getNoBottom(int(tile)):
						id = self.complete(tileId, x, y, coor)
						self.tilemap.add(id, x, y)
				x+=1
			y+=1
		return end_tiles

	def complete(self, tileid, x,y, offset):
		x=x-offset[0]
		y=y-offset[1]
		cases = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
		adj = []
		for case in cases:
			j=case[1]
			i=case[0]
			if len(tileid) <= j or j < 0:
				adj.append(-1)
			elif len(tileid[j]) <= i or i < 0:
				adj.append(-1)
			else:
				adj.append(tileid[j][i])

		#Compter et trouver le plus grand
		dic = {}
		for elem in adj:
			#Ne pas compter les tuiles non-décoratives
			if self.tileset.getDeco(int(elem)):
				if elem in dic:
					dic[elem]+=1
				else:
					dic[elem]=1
		keymax = 0
		for (k,v) in dic.items():
			if (v == max(dic.values())):
				return int(k)
		return -1
		#Christine se retournerait dans sa tombe mais ça marchait aussi
		#return list(dic.keys())[list(dic.values()).index(max(dic.values()))]

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
		self.deco = []
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
				self.noBottom_id.append(row == self.rows-2)
				self.deco.append(row == self.rows-1)

	def getSurf(self, id):
		if id == -1:
			return False
		return self.tile_id[id]

	def getNoBottom(self, id):
		if id == -1:
			return False
		return self.noBottom_id[id]

	def getDeco(self, id):
		if id == -1:
			return False
		return self.deco[id]

class Tile():
	def __init__(self, surf, x, y, game, noBottom, deco):
		self.game = game
		self.image = surf
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x*32,y*32
		self.type = "tile"
		self.noBottom = noBottom
		self.deco = deco
		if not deco:
			self.game.collisions.append(self)

	def draw(self, offset):
		self.game.surf.blit(self.image, self.rect.move(offset))

class Tilemap():
	def __init__(self, generator):
		self.generator = generator
		self.game = generator.game
		self.tiles = []
		self.deco = []
		self.tileset = generator.tileset
		self.tile_size = self.tileset.size
		self.map_w, self.map_h = 0,0
		self.map = []

	def add_in_map(self, id, x, y):
		while len(self.map)-1 < y:
			self.map.append([])
		for j in range(len(self.map)):
			while len(self.map[j])-1 < x:
					self.map[j].append(-1)
		self.map[y][x] = id
		self.map_w = len(self.map[0])*self.tile_size
		self.map_h = len(self.map)*self.tile_size

	def add(self, id, x, y):
		if id == -1 or x < 0 or y < 0:
			return
		surf = self.tileset.getSurf(id)
		noBottom = self.tileset.getNoBottom(id)
		deco = self.tileset.getDeco(id)
		tile = Tile(surf, x, y, self.game, noBottom=noBottom, deco=deco)
		if not deco:
			self.tiles.append(tile)
			self.add_in_map(id, x, y)
		else:
			self.deco.append(tile)

	def getTileId(self, x, y):
		if y >= len(self.map):
			return -1
		elif x >= len(self.map[0]):
			return -1
		return self.map[y][x]

	def getTile(self,x,y=None):
		#Renvoie la tile ou False
		#x,y = coordonnée dans la map
		if y == None:
			x,y = x
		x=x*self.tile_size
		y=y*self.tile_size
		for body in self.tiles:
			if body.rect.x == x and body.rect.y == y:
				return body
		return False

	def getTileByCoor(self,x,y=None):
		#Renvoie la tile ou False
		#x,y = coordonnée absolue
		if y == None:
			x,y = x
		x=(x//self.tile_size)*self.tile_size
		y=(y//self.tile_size)*self.tile_size
		for body in self.tiles:
			if body.rect.x == x and body.rect.y == y:
				return body
		return False