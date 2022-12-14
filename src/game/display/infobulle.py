import pygame

class Infobulle():
    def __init__(self, item):
        self.padding = 20
        self.width = 320
        self.background_color = (50,50,50)
        self.item = item
        self.game = self.item.game
        self.create_infobulle(item)
        
    def create_infobulle(self, item):
        padding = self.padding
        width = self.width
        font = pygame.font.SysFont("comic sans ms", 18)
        font_desc = pygame.font.SysFont("comic sans ms", 15)


        img_sprite = self.create_padding(pygame.transform.scale(item.sprite, (40,40)), padding, ellipse=True)
        rect_sprite = img_sprite.get_rect()

        img_title = self.create_padding(self.game.drawText(item.data["name"], (255,255,255), width-(rect_sprite.width+padding*3)-padding*2, font), padding)
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

        img_desc = self.create_padding(self.game.drawText(item.data["description"], (255,255,255), width-(padding*2)-padding*2, font_desc), padding)
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
        self.rect.midbottom = self.item.rect.move(offset).midtop
        self.rect.y -= self.padding
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1440:
            self.rect.right = 1440
        self.game.surf.blit(self.img, self.rect)