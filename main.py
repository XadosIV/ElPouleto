import pygame
from pygame.locals import *
from game import Game

def game():
	framerate = 30
	clock = pygame.time.Clock()
	w,h = (1440,720)
	running = True
	window = pygame.display.set_mode((w,h))
	pygame.font.init()
	game = Game(window)
	while running:
		dt = clock.tick(framerate)
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == QUIT:
				running = False
		game.update(events, keys, dt)


if __name__ == '__main__':
	game()