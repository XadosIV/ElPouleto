import pygame
from src.game.gameplay.entity import Entity
from src.game.display.infobulle import Infobulle
from pygame.locals import *
import json
import random

class Collection():
    def __init__(self, game):
        self.items = self.loadJson("src/game/gameplay/data/items.json", addItemType=True)
        self.weapons = self.loadJson("src/game/gameplay/data/weapons.json", addWeaponType=True)
        self.all = self.items + self.weapons
        self.game = game

    def loadJson(self, path, addItemType=False, addWeaponType=False):
        with open(path, "r", encoding="utf-8") as f:
            rawjson = f.read().encode("utf-8")
        data=json.loads(rawjson)
        if addItemType:
            for item in data:
                item["type"]="item"
        if addWeaponType:
            for item in data:
                item["type"]="weapon"
        return data

    def spawnItem(self,index,x,y):
        item = self.items[index]
        self.game.items.append(Item(self.game, item, x, y))

    def spawnWeapon(self, index, x, y):
        item = self.weapons[index]
        self.game.items.append(Item(self.game, item, x, y))

    def spawnRandomItem(self, x, y):
        item = self.all[random.randint(0, len(self.all)-1)]
        self.game.items.append(Item(self.game, item, x, y))

class Item(Entity):
    def __init__(self, game, data, x, y):
        Entity.__init__(self, game)
        self.game = game
        self.rect.x = x
        self.rect.y = y
        self.pickable = False
        self.sprite = self.images.get(f"items/{data['sprite']}")
        self.type = "item"
        self.data = data
        self.infobulle = Infobulle(self)
        self.show_info = False

    def delete(self):
        self.game.items.remove(self)
        self.game.entities.remove(self)
        del self

    def take(self):
        self.game.player.inventory.append(self.data)
        if self.data["type"] == "item":
            self.game.player.addBonus(self.data)
        else:
            if self.game.player.weaponManager.script != "Peck":
                self.game.item_collection.spawnWeapon(self.game.item_collection.weapons.index(self.game.player.weaponManager.data), self.game.player.rect.x, self.game.player.rect.y)
            self.game.player.weaponManager.set(self.data)
        self.delete()

    def check(self):
        if self.game.player.rect.colliderect(self.rect) and self.game.player.stats.life > 0:
            self.show_info = True
            if self.game.player.interact:
                self.take()
        else:
            self.show_info = False

    def draw(self, offset):
        self.game.surf.blit(self.sprite, self.rect.move(offset))