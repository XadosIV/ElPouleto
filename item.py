import pygame
from entity import Entity
from player import Player
from pygame.locals import *
import json
import random

class Collection():
    def __init__(self, game, itemfile="items.json"):
        with open("items.json", "r", encoding="utf-8") as f:
            rawjson = f.read().encode("utf-8")
        self.items = json.loads(rawjson)
        self.game = game

    def spawnItem(self,index,x,y):
        item = self.items[index]
        self.game.items.append(Item(self.game, item, x, y))


    def spawnRandomItem(self, x, y):
        item = self.items[random.randint(0, len(self.items)-1)]
        self.game.items.append(Item(self.game, item, x, y))

def drawText(text, color, width, font, bg=(0,0,0)):
    #Trouvé ici: https://www.pygame.org/wiki/TextWrap
    #Réarrangé à nos besoins
    y = 0
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    imgs_y = []

    while text:
        i = 1

        # determine maximum width of line
        while font.size(text[:i])[0] < width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        image = font.render(text[:i], True, color)
        imgs_y.append((image, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    render_img = pygame.Surface((width, y))
    render_img.fill(bg)

    for im in imgs_y:
        render_img.blit(im[0], (0, im[1]))

    return render_img

class Infobulle():
    def __init__(self, item):
        self.item = item
        self.game = self.item.game
        self.sprite = pygame.transform.scale(self.item.sprite, (50,50))
        self.sprite_rect = self.sprite.get_rect()
        pygame.font.init()
        self.create_infobulle()
        

    def create_infobulle(self):
        font = pygame.font.SysFont("comic sans ms", 18)
        font_desc = pygame.font.SysFont("comic sans ms", 15)

        img_title = drawText(self.item.data["name"], (255,255,255), 165, font)
        rect_title = img_title.get_rect()
        img_desc = drawText(self.item.data["description"], (255,255,255), 230, font_desc)
        rect_desc = img_desc.get_rect()

        img_infobulle = pygame.Surface((250,35+max(50, rect_title.height)+rect_desc.height))
        img_infobulle.fill((255,0,0))

        img_infobulle.blit(self.sprite,(10, max(10+rect_title.centery-25,10)))
        img_infobulle.blit(img_title, (75,15))
        img_infobulle.blit(img_desc, (10, 25+max(50, rect_title.height)))

        self.img = img_infobulle


    def draw(self):
        self.game.surf.blit(self.img, (0,0))

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
        self.infobulle = Infobulle(self)
        self.show_info = False

    def delete(self):
        self.game.items.remove(self)
        self.game.entities.remove(self)
        del self

    def take(self):
        self.game.player.inventory.append(self.data)
        if self.data["hasButton"] == False:
            self.game.player.addBonus(self.data)
        self.delete()

    def check(self):
        if self.game.player.rect.colliderect(self.rect):
            self.show_info = True
            if self.game.player.interact:
                self.take()
        else:
            self.show_info = False

    def draw(self, surf, offset):
        rect = [self.rect.x + offset[0], self.rect.y + offset[1]]
        if self.show_info:
            self.infobulle.draw()
        self.game.surf.blit(self.sprite, rect)
