import pygame

from src.game.gameplay.entity import Entity
from src.game.gameplay.player import Player
from src.game.gameplay.item import Item, Collection
from src.game.display.camera import Camera
from pygame.locals import *
from src.generation.generator import Generator
from src.game.gameplay.utilities import Timer, Galery
from src.game.gameplay.bindings import Bindings
from src.constants import TILE_SIZE

import random

class Game():
	def __init__(self, surf):
		pygame.font.init()
		self.gravity = 30 # Nombre de pixels par seconde (pour les entités en chute)
		self.surf = surf #Surface de la fenêtre
		#Dimensions
		self.width = surf.get_width()
		self.height = surf.get_height()
		self.galery = Galery()
		self.listener = Bindings(self) #Ecoute les touches à chaque frame pour en déterminer les actions du joueur
		self.item_collection = Collection(self) #Liste de tout les objets
		self.timers = [] #Liste de tout les timers, à update à chaque début de frame.
		self.generator = Generator(self)
		self.player = Player(self)
		self.game_ended = False
		self.world = "farm"
		self.newWorld(self.world)

	def newWorld(self, typename):
		self.entities = [] #Toutes les entitées à update à chaque frame
		self.collisions = [] #Tout les objets pouvant rentrer en contact avec les entités
		self.enemies = [] #Ennemis du joueur
		self.items = [] #Objets apparus dans le monde
		self.data = self.generator.generate(typename) #Génération de la carte
		self.tilemap = self.data["tilemap"]
		self.generator.spawns(self.data["enemies"], self.data["items"], self.data["world"], self.data["tilemap"])
		self.player.teleport(self.data["spawn"][0], self.data["spawn"][1])
		self.entities.append(self.player)

		self.camera = Camera(self) #Création de la caméra

	def update(self, events, keys, dt):
		self.events = events #Récupération des évèments de la frame
		self.keys = keys #Récupération des touches appuyés durant la frame
		self.dt = min(dt/1000, 0.05) #Calcul du Dt (avec un maximum à 0.05)
		self.inputs = self.listener.getInputs() #Update les touches appuyés sur la frame

		coord = [(self.player.rect.x//32), (self.player.rect.y//32)]
		if coord in self.data["exitWorld"] and self.world == "farm":
			self.world = "hell"
			self.newWorld(self.world)
		if coord in self.data["exitWorld"] and self.world == "hell":
			self.game_ended = True



		#Update des timers
		for timer in self.timers:
			timer.update()

		updatable_rect = self.surf.get_clip() #Rectangle dans lequel les entités sont mises à jour (optimisation)
		updatable_rect.inflate_ip(640,640) #Ce rectangle correspond à la taille de la fenêtre + 320 pixels de chaque côté (~10 tuiles)

		#Mise à jour des entités
		for entity in self.entities:
			#On update uniquement les entités dans le rectangle updatable ou si c'est le joueur
			if updatable_rect.colliderect(entity.rect.move(self.camera.offset)) or entity.type == "player":
				#Update et récupération de la vélocité
				velocity = entity.update()
				velocity[1] = int(velocity[1])
				#Coupe de la vélocité en plusieurs petits vecteurs afin de ne pas avoir de soucis de collisions
				tab = self.split_velocity_cap(velocity, TILE_SIZE//4)
				onground = entity.onground
				for t in tab: #On parcours chaque petit vecteur
					entity.rect = entity.rect.move(t[0], t[1]) #On applique le petit vecteur à l'entité
					indices = entity.rect.collidelistall(self.collisions) #On récupère ses collisions
					for i in indices:
						bloc = self.collisions[i]
						side = self.side(entity, bloc.rect)
						#Il y a une collision avec la tuile "bloc" sur le côté "side" de l'entité
						if side == "bot":
							if ((entity.type == "player" and self.inputs["passBot"]) or (entity.flying)) and bloc.noBottom:
								#On ne gère pas la collision haute si c'est le joueur, que le bloc testé n'est pas plein
								#et que le joueur souhaite le traverser (via les appuis sur S et SPACE)
								continue
							else:
								onground = True #On est donc sur un sol
								entity.rect.bottom = bloc.rect.top #On replace l'entité
								#On bloque la vélocité verticale puisqu'on a rencontré un mur.
								for t in tab:
									t[1] = 0
								velocity[1] = 0
						elif side == "top":
							if not bloc.noBottom and not bloc.topOnly: #Les blocs non plein sont traversable depuis le bas, on ne gère donc pas
								# la collision dans ce cas.
								entity.rect.top = bloc.rect.bottom # On replace l'entité
								#On bloque la vélocité verticale puisqu'on a rencontré un mur.
								for t in tab:
									t[1] = 0
								velocity[1] = 0
						elif side == "right":
							if not bloc.noBottom: #Idem, les blocs non plein sont traversables depuis les côtés
								entity.rect.right = bloc.rect.left #On replace l'entité
								#On bloque la vélocité horizontale
								for t in tab:
									t[0] = 0
								velocity[0] = 0
						elif side =="left":
							if not bloc.noBottom: #Idem, les blocs non plein sont traversables depuis les côtés
								entity.rect.left = bloc.rect.right #On replace l'entité
								#On bloque la vélocité horizontale
								for t in tab:
									t[0] = 0
								velocity[0] = 0
				#Après avoir appliqué tout les vecteurs, on donne à l'entité sa nouvelle valeur onground
				entity.onground = onground

		#On update les items
		for item in self.items:
			item.check()

		
		if not self.game_ended:
			self.camera.draw() #On affiche la frame.
		else: 
			self.surf.fill((0,0,0))
			font = pygame.font.SysFont(None, 24)
			endText = font.render("Vous avez réussi à compléter les 2 niveaux de El Pouleto !\nJ'espère que vous n'avez pas trop galéré !", True, "white")
			self.surf.blit(endText, (300, self.surf.get_size()[1]/2 -12)) #Centrer le texte
			pygame.display.flip()


	def split_velocity_cap(self, velocity, maxi):
		#Entrée : velocity Vector2, maxi Int
		#Sortie : Array "t" de Vector2 tel que t[0] = t[1] = t[...] = t[len(t) - 2] et t[len(t) -1] vecteur correcteur (= reste de division)

		#Permet de découper un vecteur en plusieurs vecteurs plus petits
		max_val = max([abs(velocity[0]), abs(velocity[1])])
		if max_val == 0:
			return []
		i=int(max_val//maxi)
		i = i if max_val%maxi == 0 else i+1
		vec = velocity / i
		total = vec*i
		t=[vec]*i
		manque_x = round(velocity[0] - total[0])
		manque_y = round(velocity[1] - total[1])
		t.append(pygame.math.Vector2(manque_x, manque_y))
		t_non_null = []
		for i in range(len(t)):
			if not(t[i].x == 0 and t[i].y == 0):
				t_non_null.append(t[i])
		return t_non_null

	def side(self, entity, body):
		#Permet de donner le côté de la collision entre entity et body (le côté sera du point de vue de l'entité)
		#renvoyer "left" signifie que body est sur la gauche de entity

		#On grandit virtuellement la taille du bloc si l'entité est plus grosse que lui.
		if body.height < entity.rect.height:
			dif = entity.rect.height - body.height
			resizer = dif//32+1 * TILE_SIZE
			goingup = entity.velocity[1] < 0
			body = body.union(body.move((0,-resizer if goingup else resizer)))
		#On récupère la collision sur tout les points de l'entité.
		topleft = body.collidepoint(entity.rect.topleft) #contient le point en haut à gauche de l'entité
		topmid = body.collidepoint(entity.rect.midtop)
		topright = body.collidepoint(entity.rect.topright)
		botleft = body.collidepoint(entity.rect.bottomleft)
		botmid = body.collidepoint(entity.rect.midbottom)
		botright = body.collidepoint(entity.rect.bottomright)
		midright = body.collidepoint(entity.rect.midright)
		midleft = body.collidepoint(entity.rect.midleft)

		#On récupère l'identifiant des tuiles autour de la tuile "body"
		x,y = body.x//32, body.y//32
		tileId_Bas = self.tilemap.getTileId(x,y+1)
		tileId_Haut = self.tilemap.getTileId(x,y-1)
		tileId_Gauche = self.tilemap.getTileId(x-1,y)
		tileId_Droite = self.tilemap.getTileId(x+1,y)
		tileId_Me = self.tilemap.getTileId(x,y)
		#On récupère si oui ou non ce bloc est transparent
		nobottom_bot = self.tilemap.tileset.getNoBottom(tileId_Bas)
		nobottom_top = self.tilemap.tileset.getNoBottom(tileId_Haut)
		nobottom_left = self.tilemap.tileset.getNoBottom(tileId_Gauche)
		nobottom_right = self.tilemap.tileset.getNoBottom(tileId_Droite)
		nobottom_me = self.tilemap.tileset.getNoBottom(tileId_Me)
		#On récupère si oui ou non ce bloc est traversable seulement par le bas
		topOnly_bot = self.tilemap.tileset.getTopOnly(tileId_Bas)
		topOnly_top = self.tilemap.tileset.getTopOnly(tileId_Haut)
		topOnly_left = self.tilemap.tileset.getTopOnly(tileId_Gauche)
		topOnly_right = self.tilemap.tileset.getTopOnly(tileId_Droite)
		topOnly_me = self.tilemap.tileset.getTopOnly(tileId_Me)
		#Définiton des forces de chaque côté
		top = int(topleft) + int(topmid) + int(topright) #sur le haut de l'entité / bas du bloc
		bot = int(botleft) + int(botright) + int(botmid) #sur le bas de l'entité / haut du bloc
		left = int(topleft) + int(midleft) + int(botleft) #sur la gauche de l'entité / droite du bloc
		right = int(topright) + int(midright) + int(botright) #sur la droite de l'entité / gauche du bloc

		#Annulation des forces impossible selon le vecteur de l'entité
		if entity.velocity[1] < 0: #l'entité va vers le haut, une collision vers le bas de celle-ci n'est pas possible
			bot = 0
		elif entity.velocity[1] > 0: #l'entité va vers le bas, une collision sur le haut de celle-ci n'est pas possible
			top = 0
		if entity.velocity[0] > 0: #l'entité va vers la droite, une collision à gauche de celle-ci n'est pas possible
			left = 0
		elif entity.velocity[0] < 0: #l'entité va vers la gauche, une collision à droite de celle-ci n'est pas possible
			right = 0

		#Annulation des côtés impossible selon les blocs adjacents
		if tileId_Bas != -1 and (not nobottom_bot): #Si il y a un bloc PLEIN en bas du bloc touché, la collision en haut de l'entité n'est pas possible
			top = 0
		if tileId_Haut != -1 and (not nobottom_top): #Si il y a un bloc PLEIN en haut du bloc touché, la collision en bas de l'entité n'est pas possible
			bot = 0

		if nobottom_me: #Dans le cas d'un bloc transparent
			if tileId_Gauche != -1 and (not nobottom_left): #Si il y a un bloc plein à gauche, la collision à droite de l'entité n'est pas possible
				right = 0
			if tileId_Droite != -1 and (not nobottom_right): #Si il y a un bloc plein à droite, la collision à gauche de l'entité n'est pas possible
				left = 0
		else: #Dans le cas d'un bloc plein
			if tileId_Gauche != -1 and (not nobottom_left): #Si il y a un bloc plein à gauche, la collision à droite de l'entité n'est pas possible
				right = 0
			if tileId_Droite != -1 and (not nobottom_right): #Si il y a un bloc plein à droite, la collision à gauche de l'entité n'est pas possible
				left = 0

		if topOnly_me: #Dans le cas d'un bloc traversable par le bas seulement
			if tileId_Gauche != -1 and (not topOnly_left): #Si il y a un bloc plein à gauche, la collision à droite de l'entité n'est pas possible
				right = 0
			if tileId_Droite != -1 and (not topOnly_right): #Si il y a un bloc plein à droite, la collision à gauche de l'entité n'est pas possible
				left = 0
		else: #Dans le cas d'un bloc plein
			if tileId_Gauche != -1 and (not topOnly_left): #Si il y a un bloc plein à gauche, la collision à droite de l'entité n'est pas possible
				right = 0
			if tileId_Droite != -1 and (not topOnly_right): #Si il y a un bloc plein à droite, la collision à gauche de l'entité n'est pas possible
				left = 0

		#On met toutes les forces dans un tableau pour les comparer
		forces = [top, bot, left, right]

		#La plus grande force est choisie
		forceMax = max(forces)
		if forceMax > 0: #Si la plus grande force est à zéro, on ne renvoie rien. => Le bloc ne touche pas l'entité
			if top == forceMax:
				return "top"
			elif bot == forceMax:
				return "bot"
			elif left == forceMax:
				return "left"
			elif right == forceMax:
				return "right"


	def drawText(self, text, color, width, font, bg=(0,0,0)):
		#Trouvé ici: https://www.pygame.org/wiki/TextWrap
		#Réarrangé à nos besoins
		y = 0
		lineSpacing = -2

		# get the height of the font
		fontHeight = font.size("Tg")[1]

		imgs_y = []
		while text:
			i = 1

			if y + fontHeight > 180:
				break

			# determine maximum width of line
			while font.size(text[:i])[0] < width and i < len(text):
				i += 1

			# if we've wrapped the text, then adjust the wrap to the last word      
			if i < len(text): 
				i = text.rfind(" ", 0, i) + 1

			# render the line and blit it to the surface
			image = font.render(text[:i], True, color)
			imgs_y.append((image, y))
			y += fontHeight + lineSpacing

			# remove the text we just blitted
			text = text[i:]

		render_img = pygame.Surface((width, y))
		render_img.fill(bg)

		for im in imgs_y:
			render_img.blit(im[0], (0, im[1]))

		return render_img