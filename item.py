import pygame
from entity import Entity
from player import Player
from pygame.locals import *

class Item(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        self.game = game
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0,0]
        self.taken = False
        self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
        self.type = "item"

    def updateTaken(self):
        self.taken = True

    def draw(self, surf):
        if not self.taken:
            self.game.surf.blit(self.sprite, self.rect)
