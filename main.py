import pygame
from pygame.locals import *
from game import Game

def game():
	framerate = 30 
	clock = pygame.time.Clock()
	w,h = (1440,720)
	running = True
	window = pygame.display.set_mode((w,h))
	game = Game(window)
	while running:
		dt = clock.tick(framerate)
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				running = False
				break
		game.update(events, dt)

if __name__ == '__main__':
	game()


     