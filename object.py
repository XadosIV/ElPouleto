from operator import truediv
import pygame
from entity import Entity
from player import Player
from pygame.locals import *

class Object(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        self.game = game
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0,0]
        self.taken = False
        self.sprite = pygame.transform.scale(pygame.image.load("./assets/poulet.png"), (self.game.tilemap.tile_size,self.game.tilemap.tile_size))
        
    def update(self):
        self.velocity[1] += self.game.gravity
        if self.velocity[1] > self.rect.height:
            self.velocity[1] = self.rect.height - 1 #Cap de vitesse de chute = hauteur de l'entité -1
													#Permet d'éviter que l'entité ne touche aucun bord d'un mur
													#Empêchant de détecter de quel côté a eu lieu la collision
        return self.velocity

    def updateTaken(self):
        self.taken = True

    def draw(self, surf):
        if not self.taken:
            self.game.surf.blit(self.sprite, self.rect)
