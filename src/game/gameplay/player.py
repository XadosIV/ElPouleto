import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.stats import Stats
import os
from src.game.gameplay.projectile import Projectile
from src.game.gameplay.weaponManager import WeaponManager
from src.game.gameplay.utilities import Timer

from src.constants import TILE_SIZE


class Player(Entity): #Initialisé comme une entité
	def __init__(self, game):
		super().__init__(game, player=True)
		self.type = "player" #Le type de l'entité / son nom.
		#Point de spawn du joueur
		self.rect.x = 0
		self.rect.y = 0
		#Inventaire, stockant les données des objets obtenus par le joueur
		self.inventory = []
		self.weaponManager = WeaponManager(self)
		self.secondary_weapon = None
		self.world_power = None
		#Chargement des images
		self.imgs = self.images.startsWith("player/") #Contient toutes les images contenues dans img_path
		self.updateDim(force=True) #Redimensionne toutes les images de self.imgs
		#Variables locales
		self.interact = False #True si touche appuyé <=> Permet au joueur d'interagir avec le jeu (item, parler, etc...)
		self.last_onground_pos = [0,0] #Position où  faire respawn le joueur en cas de chute dans le vide
		#Compteurs et timers
		self.timer_invincible = Timer(60, self.game) #Timer de frames d'invincibilité, décrémente de deltaTime à chaque frame si != 0
		self.timer_dashing = Timer(0, self.game) #Timer de frames de dash
		self.timer_gliding = Timer(0, self.game) #Timer de secondes de vol, décrémente de deltaTime à chaque frame si != 0
		self.timer_cd_dash = Timer(30, self.game) #Timer de frames avant réutilisation du dash
		self.cpt_frame = 0 #Compteur de frames, pour les animations du poulet.
		self.timer_respawn = Timer(60, self.game) #Timer de frames, pour la résurrection du joueur.
		#Affichage
		self.show_items = True #True = objets affichés sur le joueur

	def teleport(self, x, y):
		self.rect.x = x
		self.rect.y = y
		self.velocity = pygame.math.Vector2([0,0])

	def updateDim(self, force=False):
		# Redimensionne si nécessaire le joueur (tout ses sprites)
		if force or self.width != TILE_SIZE*self.stats.size:
			#Calcul de la taille selon les stats du poulet
			self.width = TILE_SIZE*self.stats.size
			self.height = TILE_SIZE*self.stats.size
			#Redimensionner les images
			"""for img in self.imgs:
				self.imgs[img] = pygame.transform.scale(self.imgs[img], (self.width, self.height))"""
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
		inputs = self.game.inputs

		if self.stats.life > 0: #Vérifier s'il est en vie
			#Sauvegarde de la dernière position correcte en cas de chute dans le vide
			#Une position correcte = deux tuiles pleines en dessous du joueur
			if self.game.tilemap.getTileByCoor(self.rect.bottomleft) and self.game.tilemap.getTileByCoor(self.rect.bottomright):
				tile1 = self.game.tilemap.getTileByCoor(self.rect.bottomleft)
				tile2 = self.game.tilemap.getTileByCoor(self.rect.bottomright)
				if (not tile1.noBottom) and (not tile2.noBottom):
					self.last_onground_pos = [self.rect.x, self.rect.y]


			#Récupérer les s sur la frame
			events = self.game.events
			keys = self.game.keys

			#Update les compteurs
			#Au sol, reset des compteurs
			if self.onground:
				#Compteur de saut
				self.cpt_saut = 0

				#Reset timer glide
				self.timer_gliding.setMax(self.stats.glide)
				self.timer_gliding.reset()
			
			if self.timer_dashing.ended: #Blocage des contrôles durant le dash.
				if not self.timer_cd_dash.running: #Si le dash est fini, on lance le cd et on reset le timer du dash
					self.timer_cd_dash.start(reset=True)
					self.timer_dashing.reset()

				#Controles horizontaux
				self.velocity[0] = 0
				if inputs["left"]:
					self.velocity[0] -= self.stats.speed*self.game.dt
				if inputs["right"]:
					self.velocity[0] += self.stats.speed*self.game.dt
				#Direction du joueur
				if self.velocity[0] > 0:
					self.direction = 1
				elif self.velocity[0] < 0:
					self.direction = -1

				#Contrôles verticaux
				if inputs["jump"]:
					if self.onground:
						self.jump(False)
					elif self.cpt_saut < self.stats.jumpMax-1 and self.velocity[1] > 0:
						self.jump(True)
				#Reset de l'interaction avec les items afind e ne pas récupérer tous les items en même temps 
				self.interact = False

				#Dash
				if inputs["dash"] and self.velocity[0] != 0 and self.timer_cd_dash.ended:
					self.timer_dashing.setMax(self.stats.dash)
					self.timer_dashing.start()

				#Utilisation de l'arme équipée
				if inputs["primary"] and inputs["lookUp"]:
					self.weapon.use(direction=-1)
				elif inputs["primary"] and inputs["lookDown"]:
					self.weapon.use(direction=1)
				elif inputs["primary"]:
					self.weapon.use()

				#Utiulisation de l'arme secondaire
				if inputs["secondary"]:
					self.secondary_weapon.use()

				#Interaction avec les items
				if inputs["interact"]:
					self.interact = True


				#check damages
				if self.timer_invincible.ended:
					for enemy in self.game.enemies:
						if self.game.player.rect.colliderect(enemy):
							self.hurt(enemy.damage)
							break #On peut pas se faire toucher deux fois dans la même frame

				#Planer
				#Uniquement en chute, avec l'appui sur la touche, si le timer est à son état initial (!= 0) ou si il n'est pas fini.
				if inputs["glide"] and self.velocity[1] >= 0 and (self.timer_gliding.max == self.timer_gliding.current != 0 or not self.timer_gliding.ended):
					self.timer_gliding.start()
					self.velocity[1] = 3 #Gravité baisse de 3 pixels le poulet par frame
				else:
					self.timer_gliding.pause()
					super().update() #Application de la gravité normalement
			else:
				#Dash
				self.timer_cd_dash.reset() # On reset le compteur du cd
				self.velocity[0] = self.direction * 1000*self.game.dt #Vitesse du dash
				self.velocity[1] = 0 #Insensible à la gravité (+ super().update() non appelé)

			if self.rect.y >= self.game.tilemap.map_h: 
				self.rect.x = self.last_onground_pos[0]
				self.rect.y = self.last_onground_pos[1]
				self.hurt(200)

		else:
			if self.stats.extraLife <= 0:
				#Perdu
				pass
			else:
				self.removeFromInventory("Tome de résurrection")
				self.timer_respawn.start()
				if self.timer_respawn.ended:
					self.timer_respawn.reset() #On réinitialise le compteur
					self.stats.extraLife -= 1 #On retire une vie
					self.stats.life = round(self.stats.lifeMax * 0.2) #On lui rend 20% de sa vie
					self.timer_invincible.start(reset=True) #On le met invincible le temps de respawn

			super().update() #Application de la gravité

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

			if not self.timer_invincible.ended:
				if self.timer_invincible.current % 6 in [0,5,4]: #3 premières frames + toutes les 3 frames
					self.sprite = self.imgs["blink"]
					self.show_items = False

	def addBonus(self,item):
		for bonus in item["bonus"]:
			if bonus["add"]:
				if bonus["var"] == "life" and self.stats.life + bonus["val"] > self.stats.lifeMax:
					self.game.item_collection.spawnItem(self.game.item_collection.items.index(self.inventory[-1]), self.game.player.rect.x, self.game.player.rect.y)
					self.removeFromInventory(self.weapon.data['name'])
					break
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
	
	def removeFromInventory(self, name):
		for i in range(len(self.inventory)):
			if self.inventory[i]['name'] == name:
				self.inventory.pop(self.inventory.index(self.inventory[i]))
				break

	def get_item_sprite(self, name):
		if name in self.imgs.keys():
			return self.imgs[name]
		else:
			return self.imgs["item_ph"] #Renvoie un placeholder (image transparente) si pas d'image.

	def draw(self, offset):
		self.updateSprite()
		super().draw(offset)
		if self.show_items:
			for item in self.inventory:
				img = self.get_item_sprite(item["sprite"]) #Récupération du sprite à appliquer sur le poulet
				if self.direction != 1: #Change le sens si dans l'autre direction
					img = pygame.transform.flip(img, True, False)
				self.game.surf.blit(img, self.rect.move([offset[0] - (img.get_size()[0]-TILE_SIZE)/2, offset[1] - (img.get_size()[1]-TILE_SIZE)/2])) #Fixe l'image au centre du poulet

		#HUD
		#Lifebar
		pygame.draw.rect(self.game.surf, (70, 70, 70), [30, 30, 300, 30])
		pygame.draw.rect(self.game.surf, (0, 0, 0), [35, 35, 190, 20])
		pygame.draw.rect(self.game.surf, (255, 0, 0), [35, 35, 190*(self.stats.life/self.stats.lifeMax), 20])
		font = pygame.font.SysFont("comic sans ms", 15)
		img = self.game.drawText(f"{max(0,self.stats.life)} / {self.stats.lifeMax}", (255,255,255), 90, font, (70,70,70))
		img_rect = img.get_rect()
		img_rect.midleft = (235,45)
		self.game.surf.blit(img, img_rect)

		#Items
		#Weapon Primary
		out_rect = pygame.Rect([self.game.width-120, self.game.height-120, 100,100])
		in_rect = pygame.Rect([0,0,85,85])
		in_rect.center = out_rect.center
		pygame.draw.rect(self.game.surf, (70,70,70), out_rect)
		pygame.draw.rect(self.game.surf, (30,30,30), in_rect)
		if (self.weapon.data != None):
			img = self.images.get("items/"+self.weapon.data["sprite"])
			img = pygame.transform.scale(img, (85,85))

			self.game.surf.blit(img, in_rect)

	def hurt(self, dmg):
		if self.stats.shield == 0:
			self.stats.life -= dmg
			self.timer_invincible.start(reset=True)
			if self.stats.life <= 0:
				self.velocity = pygame.math.Vector2([0,0])
		else:
			self.stats.shield -= 1
			self.removeFromInventory("Bulle de protection")
			self.timer_invincible.start(reset=True)