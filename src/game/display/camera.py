import pygame
from pygame.locals import *

class Camera():
	def __init__(self, game):
		self.game = game
		self.surf = self.game.surf
		self.player = self.game.player
		self.offset = [0,0] #Décalage entre les coordonnées en jeu et sur l'écran
		self.speed = 64 # vitesse de la caméra
		self.camsurf = pygame.Surface([90,64]) #Dimension du rectangle qui suivera le joueur
		self.camrect = self.camsurf.get_rect()
		self.origin = [720,480] #Placement du rectangle sur l'écran (1/2 écran horizontal, 2/3 vertical)
		self.decalage_max = 150
		self.decalage_y = 0 #Compteur de décalage de la caméra lors de l'appui sur S
		self.camrect.center = [self.origin[0], self.origin[1]]
		self.show_down = False #Booléen true si la caméra regardait vers le bas la frame précédente (permet de remettre le offset d'origine)

	def move_cam(self): #Logique des mouvements de la caméra
		inputs = self.game.inputs

		playrect = self.player.rect.move(self.offset) #Coordonnée du joueur sur l'écran

		#Le but étant de garder "camrect" dans le joueur, on redéplace correctement le offset pour atteindre le joueur
		#On ajoute ou retire un % de la vitesse de la caméra au offset, afin d'avoir un mouvement fluide  et de plus en plus rapide
		#au fur et à mesure que le joueur s'éloigne de la caméra.
		if self.camrect.top > playrect.top:
			#déplacer cam en haut
			self.offset[1] += (1 - playrect.top/self.camrect.top) * self.speed
		elif self.camrect.bottom < playrect.bottom:
			#déplacer cam en bas
			self.offset[1] -= ((playrect.bottom - self.camrect.bottom) / self.camrect.top) * self.speed
		if self.camrect.left > playrect.left:
			#déplacer cam à gauche
			self.offset[0] += (1 - playrect.left/self.camrect.left) * self.speed
		elif self.camrect.right < playrect.right:
			#déplacer cam à droite
			self.offset[0] -= ((playrect.right - self.camrect.right) / self.camrect.left) * self.speed

		#Déplacement de la caméra selon les inputs du joueur
		cam_vel_y = 0
		if inputs["lookUp"] and self.decalage_y <= self.decalage_max: #Vers le haut
			cam_vel_y += 10

		if inputs["lookDown"] and self.decalage_y >= -self.decalage_max: #Vers le bas
			cam_vel_y -= 10
		#Si pas d'input, on replace la caméra vers son endroit initial

		if cam_vel_y == 0 and self.decalage_y != 0:
			cam_vel_y = 10 if self.decalage_y < 0 else -10

		#Application
		self.decalage_y += cam_vel_y
		self.camrect.y += cam_vel_y


		#Limites
		if self.offset[0] < -(self.game.tilemap.map_w - self.game.width): #Limite droite à la taille de la carte
			self.offset[0] = -(self.game.tilemap.map_w - self.game.width)
		if self.offset[0] > 0: #Limite gauche à zéro
			self.offset[0] = 0
		if self.offset[1] < -(self.game.tilemap.map_h - self.game.height): #Limite basse à la taille de la carte
			self.offset[1] = -(self.game.tilemap.map_h - self.game.height)

	def draw(self):
		self.move_cam() # Mouvement de la caméra à mettre à jour avant de dessiner la frame

		self.surf.fill(self.game.generator.data["bgColor"]) #Fond couleur du monde

		item_infobulles = []
		for deco in self.game.tilemap.deco:
			deco.draw(self.offset)
		for platform in self.game.collisions: #La carte est dessinée
			platform.draw(self.offset)
		for entity in self.game.entities: #Toutes les entitées sont dessinées sauf le joueur
			if entity.type != "player":
				entity.draw(self.offset)
			if entity.type == "item":
				if entity.show_info: #Si l'item a besoin d'afficher une infobulle, on la stocke pour l'afficher plus tard
					item_infobulles.append(entity.infobulle)

		for infobulle in item_infobulles: #Affichage des infobulles récupérées
			infobulle.draw(self.offset)

		self.player.draw(self.offset) #Le joueur est affiché au dessus du reste

		pygame.display.flip() #On met à jour l'affichage

#Au lieu d'une cam avec le poulet au centre : Le poulet est en bas de la caméra
#Quand appui sur S (sans appui sur espace) => Le poulet peut regarder vers le bas