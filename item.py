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
        self.pickable = False
        self.sprite = pygame.transform.scale(pygame.image.load(f"./assets/{data['sprite']}.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
        self.type = "item"
        self.data = data

    def delete(self):
        self.game.items.remove(self)
        self.game.entities.remove(self)
        del self

    def take(self):
        self.taken = True
        self.game.player.inventory.append(self.data)
        if self.data["hasButton"] == False:
            self.game.player.addBonus(self.data)
        self.delete()

    def check(self):
        if self.game.player.rect.colliderect(self.rect):
            if self.game.player.interact:
                self.take()
            else:
                self.infobulle()

    def infobulle(self):
        #créer et afficher une infobulle de l'item en question
        pass

    def draw(self, surf, offset):
        rect = [self.rect.x + offset[0], self.rect.y + offset[1]]
        self.game.surf.blit(self.sprite, rect)
