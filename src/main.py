import pygame
from pygame.locals import *
from src.game.game import Game
from src.constants import CREDITS
from src.inputbox import InputBox

class Main():
	def __init__(self):
		self.scene = 1 # 1 = menu / 2 = game / 3 = end
		self.w, self.h = (1440,720)
		self.window = self.create_window()
		self.clock = pygame.time.Clock()
		self.framerate = 30
		self.posMouse = (0,0)
		
		self.seedInput = InputBox(0,0, self.w//4, self.h//10, "Seed: ", self)
		self.seedRaw = ""
		self.loop()

	def setGame(self): #Appelé au passage de scene 1 à scene 2
		self.game = Game(self.window, self, self.seedRaw)

	def loop(self):
		running = True
		while running:
			self.click = False
			events = pygame.event.get()
			keys = pygame.key.get_pressed()
			for event in events:
				if event.type == QUIT:
					running = False
				if event.type == MOUSEBUTTONDOWN:
					self.click = True

				if self.scene == 1:
					self.seedInput.handle_event(event)
	
			dt = self.clock.tick(self.framerate)
			self.posMouse = pygame.mouse.get_pos()

			if self.scene == 1:
				self.main_menu()
			elif self.scene == 2:
				self.game.update(events, keys, dt)
			elif self.scene == 3:
				self.credits()

	def switchScene(self):
		if (self.scene == 1):
			self.setGame() #On définie self.game (pas avant car besoin de la seed)
		elif (self.scene == 2):
			#On récupère le score du joueur:
			self.score = self.game.score
			self.timescore = self.game.timeToString()

			self.credits_y = 0 #On définie les variables de l'algo de crédits
			self.loadCredits()

		self.scene += 1
		if (self.scene > 3):
			self.scene = 1

	def loadCredits(self):
		margin = 10 #Espace entre chaque ligne
		creditsLines = CREDITS.split("\n") #Lignes récupérés du fichier constants.py
		font = pygame.font.SysFont(None, 48) #Taille d'écriture

		textSurfaces = [] #Stockage des surfaces de chaque texte
		heightSurfaces = 0 #Compte taille totale nécessaire
		for line in creditsLines: #Remplissage des deux variables précédentes
			if (line == "[score]"):
				surface = font.render("Score : "+str(self.score), True, "white") # <= Génération de la surface
			elif (line == "[temps]"):
				surface = font.render("Temps :"+self.timescore, True, "white") # <= Génération de la surface
			else:
				surface = font.render(line, True, "white") # <= Génération de la surface
			heightSurfaces += surface.get_rect().height + margin
			textSurfaces.append(surface)

		self.creditsSurface = pygame.Surface((self.w, heightSurfaces)) # Surface unique, image contenant tout les crédits
		y = 0
		for surface in textSurfaces: #Placement de tout les textes, alignés correctement dans l'image
			rect = surface.get_rect()
			rect.midtop = (self.creditsSurface.get_rect().centerx, y)
			self.creditsSurface.blit(surface, rect)
			y += rect.height + margin

	def credits(self):
		#Simplement, appelé à chaque frame, fait monter un rectangle de 2 pixels par frame.
		#Concrètement : fait défilé les crédits.
		self.window.fill((0,0,0))

		rect = self.creditsSurface.get_rect()
		rect.midtop = (self.w//2, self.credits_y)

		self.window.blit(self.creditsSurface, rect)

		self.credits_y -= 2
		pygame.display.flip()

	def main_menu(self):
		self.window.fill((0,0,0))
	
		font = pygame.font.SysFont(None, 100)
		#Title
		surfTitle = font.render("El Pouleto !", True, "white")
		rectTitle = surfTitle.get_rect()
		rectTitle.center = (self.w//2,self.h//3)
		#PlayButton
		font = pygame.font.SysFont(None, 50)
		playButton = font.render("JOUER", True, "black")
		rectPlayButton = playButton.get_rect()
	
		padding = 20
		bgPlayButton = pygame.Surface((rectPlayButton.width+padding*2, rectPlayButton.height+padding*2))
		rectBgPlayButton = bgPlayButton.get_rect()
		rectPlayButton.center = rectBgPlayButton.center
		rectBgPlayButton.center = (self.w//2, (self.h//3)*2)
	
		#PlayButtonDetection
		if (rectBgPlayButton.collidepoint(self.posMouse)):
			bgPlayButton.fill((255,255,0))
			if (self.click):
				self.switchScene()
				
		else:
			bgPlayButton.fill((255,255,255))
		bgPlayButton.blit(playButton, rectPlayButton)

		#SeedInput position
		self.seedInput.rect.center = (self.w//2, (self.h//3)*3 - self.seedInput.rect.height)

		#Draw
		self.window.blit(surfTitle, rectTitle)
		self.window.blit(bgPlayButton, rectBgPlayButton)

		self.seedInput.update()
		self.seedInput.draw(self.window)

		pygame.display.flip()

	def create_window(self):
		pygame.init()

		window = pygame.display.set_mode((self.w,self.h))
		pygame.display.set_icon(pygame.image.load("./resources/icon.png"))
		pygame.display.set_caption("El Pouleto !")
		pygame.mouse.set_visible(True)
		return window