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

        if y + fontHeight > 180:
            break

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
        self.padding = 20
        self.width = 320
        self.background_color = (50,50,50)
        self.item = item
        self.game = self.item.game
        pygame.font.init()
        self.create_infobulle(item)
        

    def create_infobulle(self, item):
        padding = self.padding
        width = self.width
        font = pygame.font.SysFont("comic sans ms", 18)
        font_desc = pygame.font.SysFont("comic sans ms", 15)


        img_sprite = self.create_padding(pygame.transform.scale(item.sprite, (40,40)), padding, ellipse=True)
        rect_sprite = img_sprite.get_rect()

        img_title = self.create_padding(drawText(item.data["name"], (255,255,255), width-(rect_sprite.width+padding*3)-padding*2, font), padding)
        rect_title = img_title.get_rect()

        rect_sprite.x = padding
        rect_title.x = padding*2+rect_sprite.width

        if rect_title.height > rect_sprite.height:
            #centrer rect_sprite
            rect_title.y = padding
            rect_sprite.centery = rect_title.centery
        else:
            #centrer rect_title
            rect_sprite.y = padding
            rect_title.centery = rect_sprite.centery

        img_desc = self.create_padding(drawText(item.data["description"], (255,255,255), width-(padding*2)-padding*2, font_desc), padding)
        rect_desc = img_desc.get_rect()
        rect_desc = rect_desc.move((padding, padding*2+max(rect_sprite.height, rect_title.height)))

        img_infobulle = pygame.Surface((width,padding*3+max(rect_sprite.height, rect_title.height)+rect_desc.height))
        img_infobulle.fill(self.background_color)

        img_infobulle.blit(img_sprite, rect_sprite)
        img_infobulle.blit(img_title, rect_title)
        img_infobulle.blit(img_desc, rect_desc)

        self.img = img_infobulle
        self.rect = self.img.get_rect()

    def create_padding(self, img, padding, color=(0,0,0), ellipse=False):
        rect = img.get_rect()
        img_padding = pygame.Surface((padding*2+rect.width, padding*2+rect.height))
        if ellipse:
            img_padding.fill(self.background_color)
            rect_padding = img_padding.get_rect()
            pygame.draw.circle(img_padding, color, rect_padding.center, rect_padding.width//2)
        else:
            img_padding.fill(color)
        img_padding.blit(img, (padding,padding))
        return img_padding


    def draw(self, offset):
        self.rect.midbottom = [self.item.rect.x + offset[0], self.item.rect.y + offset[1]]
        self.rect.y -= self.padding
        self.game.surf.blit(self.img, self.rect)

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

    def draw(self, offset):
        coor = [self.rect.x + offset[0], self.rect.y + offset[1]]
        self.game.surf.blit(self.sprite, coor)