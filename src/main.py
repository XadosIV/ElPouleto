import pygame
from pygame.locals import *
from src.game.game import Game

def main():
	window = _create_window()
	game = Game(window)
	running = True
	clock = pygame.time.Clock()
	while running:
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		framerate = 30
		dt = clock.tick(framerate)
		for event in events:
			if event.type == QUIT:
				running = False
		game.update(events, keys, dt)


def _create_window():
	pygame.init()

	w,h = (1440,720)
	window = pygame.display.set_mode((w,h))
	pygame.display.set_icon(pygame.image.load("./resources/icon.png"))
	pygame.display.set_caption("El Pouleto !")
    #pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
	pygame.mouse.set_visible(True)
	window.fill((0,0,0))
	font = pygame.font.SysFont(None, 24)
	startText = font.render("Bienvenue sur notre jeu, El Pouleto !", True, "white")
	startTextTwo = font.render("Vous êtes ici en tant que petit poulet, afin de vivre votre vie paisible dans la ferme", True, "white")
	window.blit(startText, (550, window.get_size()[1]/2 -12)) #Centrer le texte
	window.blit(startTextTwo, (400, window.get_size()[1]/2 +30))
	pygame.display.flip()
    #pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
	return window