# /!\ Pas notre code ! Trouvé sur stackoverflow : https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

import pygame as pg

pg.init()

COLOR_INACTIVE = pg.Color('white')
COLOR_ACTIVE = pg.Color((255,255,0))
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text, mainMenu):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.baseText = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.mainMenu = mainMenu

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    if (self.text != self.baseText):
                        self.text = self.text[:-1]
                elif event.key != pg.K_RETURN:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                self.mainMenu.seedRaw = self.text
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)