import pygame
from pygame.locals import *
from game import Game

def game():
	clock = pygame.time.Clock()
	w,h = (1000,500)
	running = True
	window = pygame.display.set_mode((w,h))
	game = Game(window)
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				break
		game.update()
		clock.tick(30)




if __name__ == '__main__':
	game()
