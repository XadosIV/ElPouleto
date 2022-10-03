import pygame
from entity import Entity
from player import Player
from pygame.locals import *

class Item(Entity):
    def __init__(self, game, x, y, bonus):
        Entity.__init__(self, game)
        self.game = game
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0,0]
        self.taken = False
        self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
        self.type = "item"
        self.bonus = bonus

    def check(self, player):
        if player.rect.colliderect(self.rect) and not self.taken:
            self.taken = True
            player.inventory.append(self.bonus)
            player.addBonus(self.bonus)

    def draw(self, surf, offset):
        if not self.taken:
            self.game.surf.blit(self.sprite, self.rect)
