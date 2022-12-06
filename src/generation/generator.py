import pygame, csv, random, json, importlib, os
from src.constants import WORLDS_PATH, TILE_SIZE, ENEMIES_PACKAGE

class Generator():
	def __init__(self, game):
		self.game = game

	def newSeed(self, seed=None):
		if seed != None:
			seed = seed
		else:
			seed = random.randint(1, 1000000000) #On génère jusqu'à un milliard de seed.
		random.seed(seed) #Application de la seed
		return seed

	def spawns(self, enemiesCoor, itemsCoor, world, tilemap):
		enemies, flyingEnemies = self.importEnemiesByWorld(world)
		for i in enemiesCoor:
			if tilemap.getTileByCoor(i[0], i[1]+TILE_SIZE):
				random.choice(enemies)(self.game, i[0], i[1]) #ennemi terrestre
			else:
				random.choice(flyingEnemies)(self.game, i[0], i[1]) #sinon ennemi aérien
		for i in itemsCoor:
			self.game.item_collection.spawnRandomItem(i[0], i[1])

	def generate(self, world, seed=None): #world : String du dossier du monde à lire
		seed = self.newSeed(seed) #Charge une nouvelle seed
		path = WORLDS_PATH+world+"/" #Le chemin vers le dossier du monde
		info = self.readInfo(path) #Récupère les informations dans le 'info.json'
		tileset = self.loadTileset(path) #Charge le jeu de tuile du monde
		data = self.generateTilemap(path, tileset, info) #Génère une tilemap pseudo-aléatoire 
		data["seed"] = seed #On met la seed dans les données à renvoyer
		data["world"] = world #Idem pour le monde
		data["bgColor"] = info["bgColor"]
		data["name"] = info["name"]
		return data #On renvoie les données du monde généré

	def generateTilemap(self, path, tileset, info):
		tilemap = Tilemap(self.game, tileset) #Crée une tilemap pour générer le monde
		startTile = [0,100] #Coordonnées logique où commencer la génération
		
		returnData = {
			"enemies":[],
			"items":[],
			"spawn":[],
			"tilemap":tilemap
		}

		#Génération du spawn
		data = self.spawnStructure(startTile, "spawn", path, tilemap)
		debTile = data["endTile"]
		debTile[0]-=1
		self.merge(returnData, data)
		
		#Génération des structures
		structures_spawned = [] #Structures ayant déjà été générés
		structures_max = len(os.listdir(path+"structures")) #Nombre de structures uniques dans le monde
		for i in range(info["nbStructures"]):
			struct_id = self.nextStruct(structures_max, structures_spawned) #Prochaine structure à générer
			if struct_id == -1:
				break #Le nombre de structure a été dépassé nextStruct, inutile de continuer.
			else:
				data = self.spawnStructure(data["endTile"], "structures/"+str(struct_id), path, tilemap)
				debTile = data["endTile"]
				debTile[0]-=1
				self.merge(returnData, data)

		#Génération de la structure de fin
		data = self.spawnStructure(data["endTile"], "end", path, tilemap)
		self.merge(returnData, data)
		
		#Remplissage des sols
		self.fill(tilemap)
		
		#Retirer certaines collisions inutiles
		self.optimize(tilemap)
		return returnData

	def merge(self, returnData, data):
		#Fusionne les données 'data' dans le 'grand dictionnaire' 'returnData'
		#Aucun return n'est nécessaire => returnData est une référence, elle est modifiée dans le script d'origine.
		returnData["enemies"]+=data["enemies"]
		returnData["items"]+=data["items"]
		if len(data["spawn"]) != 0:
			returnData["spawn"] = data["spawn"]

	def spawnStructure(self, coor, name, path, tilemap):
		#Load structure data
		csvData = []
		with open(path+name+".csv", "r") as data_raw:
			data = csv.reader(data_raw, delimiter=",")
			for row in data:
				csvData.append(list(row))

		#startTile Coordonnées (= get Offset)
		offset = 0
		for i in range(len(csvData)):
				if "3" in csvData[i]:
					offset = -i

		# Coordonnées
		x,y = coor
		y += offset

		#Initialisation des tableaux à remplir pendant le parcours des données et renvoyer à la fin
		enemiesTiles = [] #Coordonnées des tuiles "enemies"
		itemsTiles = [] #Coordonnées des tuiles "items"
		spawnCoor = [] #Coordonnées du spawn s'il existe, sinon tableau vide.
		endTile = [] #Coordonnée de fin de la structure, sinon tableau vide

		#Ajout de la structure dans la tilemap
		for row in csvData: #Parcours des données
			x = coor[0]
			for tile in row:
				if tile == "0":
					#Coordonnée de spawn du joueur
					spawnCoor = [x * TILE_SIZE, y * TILE_SIZE] #récupère la valeur de la tuile de contrôle
					id = self.complete(csvData, x-coor[0], y-offset-coor[1], tilemap.tileset) #vérifie si on peut compléter par un bloc de déco la place.
					tilemap.add(id, x, y) #Ajout de la tuile logique renvoyé par self.complete
				elif tile == "1":
					#Coordonnée où faire spawn un item
					itemsTiles.append( (x*TILE_SIZE, y*TILE_SIZE) )
					id = self.complete(csvData, x-coor[0], y-offset-coor[1], tilemap.tileset)
					tilemap.add(id, x, y)
				elif tile == "2":
					#Coordonnée où faire spawn un ennemi
					enemiesTiles.append( (x*TILE_SIZE, y*TILE_SIZE) )
					id = self.complete(csvData, x-coor[0], y-offset-coor[1], tilemap.tileset)
					tilemap.add(id, x, y)
				elif tile == "4":
					#Tuile de fin à renvoyer
					endTile = [x,y]
				elif tile != "-1" and tile != "3": #Cas où ce n'est pas un bloc vide ni un bloc de contrôle (dernier non géré ici = 3)
					tilemap.add(int(tile), x, y) #On ajoute le bloc à la tilemap
					if tilemap.tileset.getNoBottom(int(tile)): #Si c'est un bloc transparent
						id = self.complete(csvData, x-coor[0], y-offset-coor[1], tilemap.tileset) #On vérifie si on peut compléter par un bloc de déco
						tilemap.add(id, x, y) #On l'ajoute si on peut (sinon ça l'ajoute quand même avec -1 et le add de tilemap l'ignore.)
				x+=1
			y+=1

		return {
			"endTile":endTile,
			"spawn":spawnCoor,
			"enemies":enemiesTiles,
			"items":itemsTiles
		}

	def complete(self, tileid, x,y, tileset):
		#Regarde les blocs adjacents au bloc [x,y]-[offset] et renvoie le bloc décoratif adjacent le plus présent.
		#Permet de 'compléter' les murs des structures ayant des blocs de contrôles.
		# (On ne pouvait pas mettre sur la même case une tuile de mur et une tuile de contrôle.)
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
			if tileset.getDeco(int(elem)):
				if elem in dic:
					dic[elem]+=1
				else:
					dic[elem]=1
		########
		keymax = 0
		for (k,v) in dic.items():
			if (v == max(dic.values())):
				return int(k)
		return -1
		#Christine se retournerait dans sa tombe mais ça marchait aussi
		#return list(dic.keys())[list(dic.values()).index(max(dic.values()))]

	def readInfo(self, path): #Lit et renvoie les données du fichier 'info.json', contenant des données sur le monde.
		with open(path+"info.json") as f:
			raw_json = f.read()
		return json.loads(raw_json)

	def loadTileset(self, path): #Renvoie une instance chargée du jeu de tuile du monde
		return Tileset(path + "tileset.png")

	def importEnemiesByWorld(self, world):
		enemies = []
		flyingEnemies = []
		#read json
		with open("./src/generation/data/enemies.json", "r") as f:
			raw_json = f.read()
		#get world_array
		enemiesByWorld = json.loads(raw_json)
		worldEnemies = enemiesByWorld[world]
		#Import and append classes in enemies
		for name in worldEnemies:
			file = "."+name.lower()
			module = importlib.import_module(file, ENEMIES_PACKAGE)
			try:
				if module.__dict__["flying"]:
					flyingEnemies.append(module.__dict__[name])
				else:
					enemies.append(module.__dict__[name])
			except Exception as e:
				enemies.append(module.__dict__[name])

		return enemies,flyingEnemies

	def optimize(self, tilemap):
		#Retire des collisions tout les blocs touchant d'autres blocs de tout les côtés, inutile de les compter...
		#dans les collisions puisque celles-ci n'arriveront jamais.
		#Ces tuiles seront mises en déco pour être quand même affiché
		for tile in tilemap.tiles:
			up = tilemap.getTileId(tile.x, tile.y-1)
			down = tilemap.getTileId(tile.x, tile.y+1)
			left = tilemap.getTileId(tile.x-1, tile.y)
			right = tilemap.getTileId(tile.x+1, tile.y)
			upleft = tilemap.getTileId(tile.x-1, tile.y-1)
			upright = tilemap.getTileId(tile.x+1, tile.y-1)
			downleft = tilemap.getTileId(tile.x-1, tile.y+1)
			downright = tilemap.getTileId(tile.x+1, tile.y+1)
			if up == down == left == right == upleft == upright == downleft == downright:
				if up != -1:
					tile.deco = True
					self.game.collisions.remove(tile)
					tilemap.deco.append(tile)

	def fill(self, tilemap):
		#Parcours la tilemap pour remplir ses sols de blocs (= ne pas avoir de "structures flottantes")
		map = tilemap.map
		for x in range(len(map[0])):
			tile = map[len(map)-1][x]
			if tile == -1:
				self.fillUp(x, len(map)-1, tilemap)

	def fillUp(self, x, y, tilemap):
		#Fonction récursive 'remontant' les tuiles une par une jusqu'à trouver une tuile de bloc
		#Si la tuile trouvée est pleine, on remplie les blocs parcourus par cette même tuile
		if y == -1:
			return -1
		tile = tilemap.map[y][x]
		if tile == -1:
			nextTile = self.fillUp(x, y-1, tilemap)
			if tilemap.tileset.getNoBottom(nextTile):
				return -1
			else:
				tilemap.add(nextTile, x, y)

				return nextTile
		else:
			return tile

	def nextStruct(self, max, spawned=[]):
		#Renvoie un nombre aléatoire entre 1 et max qui n'est pas contenu dans 'spawned'
		#Renvoie -1 si ce nombre n'existe pas.
		#Permet de choisir le nombre de la prochaine structure généré.
		if len(spawned) < max:
			nb = random.randint(1,max)
			while nb in spawned:
				nb = random.randint(1,max)
			return nb
		else:
			return -1


class Tileset():
	def __init__(self, path):
		#Les tuiles du tileset ont des règles spécifiques selon les lignes : 
		#Première ligne : Tuiles de contrôles : 
		# 0 = Spawn du joueur		#3 = Entrée de la structure
		# 1 = Spawn d'un item 		#4 = Sortie de la structure
		# 2 = Spawn d'un ennemi

		#Seconde ligne : Les tuiles classiques, ont toutes les collisions et sont gérés normalements.

		#Troisieme ligne : Les tuiles transparentes (noBottom) : 
		#	- Aucune collisions latérales
		#	- On peut les traverser de bas en haut
		#	- Le joueur peut les traverser de haut en bas en appuyant sur bas + saut
		#	- Les ennemis volants peuvent les traverser de haut en bas

		#Quatrième ligne : Les tuiles de décoration arrières
		#	- N'ont aucune collisions et servent uniquement de décoration d'ARRIERE PLAN.

		#Cinquième ligne : Les tuiles de décoration avants
		#	- Idem mais sont affichés au premier plan par rapport au joueur

		#Sixième ligne : Les tuiles de dégats
		#	- Comme des tuiles classiques en terme de collision et gestion
		#	- Si le joueur rentre en collision, la tuile inflige des dégats fixe définis dans les stats du monde
		#	=> Le joueur est ensuite replacé dans un espace correcte (comme lors d'une chute)

		self.tileset = pygame.image.load(path) #Chargement de l'image tileset
		self.img_size = self.tileset.get_size()
		self.rows = self.img_size[1]//TILE_SIZE
		self.columns = self.img_size[0]//TILE_SIZE
		self.tile_id = [] #Tableau ID => Surface pour chaque tuile
		self.noBottom_id = [] #Tableau ID => True/False noBottom, indique si la tuile est transparente
		self.deco = [] #Tableau ID => True/False, indique si la tuile est une déco ou doit être géré normalement
		self.damage = [] #Tableau ID => True/False, indique si la tuile doit infliger des dégâts
		self.load()

	def load(self):
		for row in range(self.rows):
			for column in range(self.columns):
				surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, TILE_SIZE)
				surf.convert_alpha()
				surf.blit(self.tileset, (0,0), (column*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE))
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
		self.rect.x, self.rect.y = x*TILE_SIZE,y*TILE_SIZE
		self.type = "tile"
		self.noBottom = noBottom
		self.deco = deco
		if not deco:
			self.game.collisions.append(self)

	def draw(self, offset):
		self.game.surf.blit(self.image, self.rect.move(offset))

class Tilemap():
	def __init__(self, game, tileset):
		self.game = game
		self.tiles = []
		self.deco = []
		self.tileset = tileset
		self.map_w, self.map_h = 0,0
		self.map = []

	def add_in_map(self, id, x, y):
		while len(self.map)-1 < y:
			self.map.append([])
		for j in range(len(self.map)):
			while len(self.map[j])-1 < x:
					self.map[j].append(-1)
		self.map[y][x] = id
		self.map_w = len(self.map[0])*TILE_SIZE
		self.map_h = len(self.map)*TILE_SIZE

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
		x=x*TILE_SIZE
		y=y*TILE_SIZE
		for body in self.tiles:
			if body.rect.x == x and body.rect.y == y:
				return body
		return False

	def getTileByCoor(self,x,y=None):
		#Renvoie la tile ou False
		#x,y = coordonnée absolue
		if y == None:
			x,y = x
		x=(x//TILE_SIZE)*TILE_SIZE
		y=(y//TILE_SIZE)*TILE_SIZE
		for body in self.tiles:
			if body.rect.x == x and body.rect.y == y:
				return body
		return False