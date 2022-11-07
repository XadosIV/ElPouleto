import pygame
from pygame.locals import *
from entity import Entity
from stats import Stats
import os
from projectile import Projectile
from weapons import Weapon

class Player(Entity): #Initialisé comme une entité
	def __init__(self, x,y, game, img_path="./assets/player/"):
		super().__init__(game)
		self.type = "player" #Le type de l'entité / son nom.
		#Point de spawn du joueur
		self.rect.x = x
		self.rect.y = y
		#Inventaire, stockant les données des objets obtenus par le joueur
		self.inventory = []
		self.weapon = Weapon(self)
		self.secondary_weapon = None
		self.world_power = None
		#Chargement des images
		self.imgs = self.loadImg(img_path) #Contient toutes les images contenues dans img_path
		self.updateDim(force=True) #Redimensionne toutes les images de self.imgs
		#Variables locales
		self.interact = False #True si E appuyé <=> Permet au joueur d'interagir avec le jeu (item, parler, etc...)
		self.last_onground_pos = [x,y] #Position où  faire respawn le joueur en cas de chute dans le vide
		#Compteurs
		self.invincible = 0 #Compteur de frames d'invincibilité, décrémente de deltaTime à chaque frame si != 0
		self.dashing = 0 #Compteur de frames de dash
		self.gliding = 0 #Compteur de secondes de vol, décrémente de deltaTime à chaque frame si != 0
		self.cd_dash = 0 #Compteur de frames avant réutilisation du dash
		self.cpt_frame = 0 #Compteur de frames, pour les animations du poulet.
		self.not_dead = 60 #Compteur de frames, pour la résurrection du joueur.
		self.death_cd = 0 #Compteur de frames, pour pas qu'il y aie 2 résurrections en trop peu de temps
		#Affichage
		self.show_items = True #True = objets affichés sur le joueur		
		

	def loadImg(self, path):
		#Charge toutes les images contenues dans path et les renvoie sous forme de dictionnaire name -> image
		imgs = {}
		for name in os.listdir(path):
			imgs[name.split(".")[0]] = pygame.image.load(path+name)
		return imgs


	def updateDim(self, force=False):
		# Redimensionne si nécessaire le joueur (tout ses sprites)
		if force or self.width != self.game.tilemap.tile_size*self.stats.size:
			#Calcul de la taille selon les stats du poulet
			self.width = self.game.tilemap.tile_size*self.stats.size
			self.height = self.game.tilemap.tile_size*self.stats.size
			#Redimensionner les images
			for img in self.imgs:
				self.imgs[img] = pygame.transform.scale(self.imgs[img], (self.width, self.height))
			#Définir le sprite par défaut
			self.sprite = self.imgs["poulet0"]
			#Update le rectangle
			rect = self.sprite.get_rect()
			#Repositionner à la position précédente, par le bas afin de ne pas clip dans les blocs dans le cas d'un aggrandissement
			rect.bottom, rect.midbottom = self.rect.bottom, self.rect.midbottom
			self.rect = rect
		#Renvoie ses dimensions
		return (self.width, self.height)

	def update(self): #Executé à chaque frame par Game (renvoie la vélocité de l'entité pour les calculs de physique.)
		if self.stats.life > 0: #Vérifier s'il est en vie
			#Récupérer les inputs sur la frame
			events = self.game.events
			keys = self.game.keys

			#Update les compteurs

			#Compteur frame d'invincibilité
			if self.invincible > 0:
				self.invincible -= 1
			#Compteur frame avant re_dash
			if self.cd_dash > 0:
				self.cd_dash -= 1
			#Compteur frame avant re_résurrection
			if self.death_cd > 0:
				self.death_cd -= 1
			#Au sol, reset des compteurs
			if self.onground:
				#Compteur de saut
				self.cpt_saut = 0
				#Compteur frame planer
				self.gliding = self.stats.glide
			
			if self.dashing == 0: #Blocage des contrôles durant le dash.
				#Controles horizontaux
				if keys[K_q]:
					self.velocity[0] = -self.stats.speed*self.game.dt
					self.direction = -1
				elif keys[K_d]:
					self.velocity[0] = self.stats.speed*self.game.dt
					self.direction = 1
				else:
					self.velocity[0] = 0

				#Verticaux
				if keys[K_z]:
					if self.onground:
						self.jump(False)

				for event in events:
					if event.type == pygame.KEYDOWN:
						#Double saut
						if event.key == K_z and self.cpt_saut < self.stats.jump_max-1 and not self.onground and self.velocity[1] > 0:
							self.jump(True)
						#Dash
						if event.key == K_v and self.velocity[0] != 0 and self.cd_dash <= 0:
							self.dashing = self.stats.dash

						#Attaque
						if event.key == K_SPACE:
							#Projectile(self.game, self)
							self.weapon.use()
						#Interaction
						if event.key == K_e:
							self.interact = True
		
					if event.type == pygame.KEYUP:
						if event.key == K_e:
							self.interact = False


				#check damages
				if self.invincible == 0:
					for enemy in self.game.enemies:
						if self.game.player.rect.colliderect(enemy):
							self.stats.life -= 100
							self.invincible = 60
							if self.stats.life <= 0:
								self.velocity = pygame.math.Vector2([0,0])

				#Planer
				if keys[K_z] and self.gliding > 0 and self.velocity[1] >= 0:
					self.gliding -= self.game.dt
					self.velocity[1] = 3 #Gravité baisse de 3 pixels le poulet par frame
				else:
					super().update() #Application de la gravité normalement
			else:
				#Dash
				self.velocity[0] = self.direction * 1000*self.game.dt #Vitesse du dash
				self.velocity[1] = 0 #Insensible à la gravité (+ super().update() non appelé)
				self.dashing -= 1 #Décrémente le compteur du dash
				if self.dashing == 0:
					self.cd_dash = 60 #Lorsque le dash est fini, on met à jour son cooldown pour le réutiliser dans 30 frames

			if self.onground:
				self.last_onground_pos = [self.rect.x, self.rect.y]
			
			if self.rect.y >= self.game.tilemap.map_h: #Pour l'instant c'est 32000 parce que Joris il est con
				self.rect.x = self.last_onground_pos[0]
				self.rect.y = self.last_onground_pos[1]
				self.velocity[1] = 0
				self.stats.life -= 200

		else:
			for item in self.inventory:
				if self.game.item_collection.items.index(item) == 5 and self.death_cd == 0:					
					self.not_dead -= 1 #Décrémente le compteur de la mort
					if self.not_dead == 0:
						self.not_dead = 60
						self.death_cd = 300
						self.addBonus(item)
						self.inventory.remove(item) #Lorsque la mort est finie, on met à jour son cooldown pour le réutiliser dans minimum 60 frames, et on supprime l'item
			super().update()
		return self.velocity
		
	def updateSprite(self):
		self.cpt_frame += 1
		if self.cpt_frame == 16:
			self.cpt_frame = 0
		self.show_items = True
		if self.stats.life <= 0:
			self.sprite = self.imgs["dead"]
			self.show_items = False
		else:
			if not self.onground:
				self.sprite = self.imgs["glide"]
			else:
				if self.velocity[0] == 0:
					self.sprite = self.imgs["poulet0"]
				else:
					self.sprite = self.imgs["poulet"+str(self.cpt_frame//4)]

			if self.invincible != 0:
				if self.invincible % 6 in [0,5,4]: #3 premières frames + toutes les 3 frames
					self.sprite = self.imgs["blink"]
					self.show_items = False

	def addBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) + bonus["val"])
			else:
				setattr(self.stats, bonus["var"], bonus["val"])
			if bonus["var"] == "size":
				self.updateDim()

	def removeBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				setattr(self.stats, bonus["var"], getattr(self.stats, bonus["var"]) - bonus["val"])
			else:
				setattr(self.stats, bonus["var"], self.stats.base_stats()[bonus["var"]])

	def endCooldownDash(self):
		self.stats.can_dash = True

	def get_item_sprite(self, name):
		if name in self.imgs.keys():
			return self.imgs[name]
		else:
			return self.imgs["item_ph"] #Renvoie un placeholder (image transparente) si pas d'image.

	def draw(self, offset):
		self.updateSprite()
		super().draw(offset)
		if self.show_items:
			rect = [self.rect.x + offset[0], self.rect.y + offset[1]]
			for item in self.inventory:
				img = self.get_item_sprite(item["sprite"])
				if self.direction != 1:
					img = pygame.transform.flip(img, True, False)
				self.game.surf.blit(img, rect)

		#HUD
		pygame.draw.rect(self.game.surf, (70, 70, 70), [30, 30, 300, 30])
		pygame.draw.rect(self.game.surf, (0, 0, 0), [35, 35, 190, 20])
		pygame.draw.rect(self.game.surf, (255, 0, 0), [35, 35, 190*(self.stats.life/self.stats.lifemax), 20])
		font = pygame.font.SysFont("comic sans ms", 15)
		img = self.game.drawText(f"{max(0,self.stats.life)} / {self.stats.lifemax}", (255,255,255), 90, font, (70,70,70))
		img_rect = img.get_rect()
		img_rect.midleft = (235,45)
		self.game.surf.blit(img, img_rect)