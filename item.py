import pygame
from entity import Entity
from player import Player
from pygame.locals import *
import json
import random

class Collection():
    def __init__(self, game, itemfile="items.json"):
        with open("items.json", "r") as f:
            rawjson = f.read().encode("utf-8")
        self.items = json.loads(rawjson)
        self.game = game

    def spawnItem(self,index,x,y):
        item = self.items[index]
        self.game.items.append(Item(self.game, item, x, y))


    def spawnRandomItem(self, x, y):
        item = self.items[random.randint(0, len(self.items)-1)]
        self.game.items.append(Item(self.game, item, x, y))


class Item(Entity):
    def __init__(self, game, data, x, y):
        Entity.__init__(self, game)
        self.game = game
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0,0]
        self.taken = False
        self.sprite = pygame.transform.scale(pygame.image.load(f"./assets/{data['sprite']}.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
        self.type = "item"
        self.data = data

    def check(self, player):
        if player.rect.colliderect(self.rect) and not self.taken:
            self.taken = True
            player.inventory.append(self.data)
            player.addBonus(self.data)

    def draw(self, surf, offset):
        if not self.taken:
            rect = [self.rect.x + offset[0], self.rect.y + offset[1]]
            self.game.surf.blit(self.sprite, rect)
