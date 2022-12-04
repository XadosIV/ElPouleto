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
		framerate = 60
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
    #pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
	return window