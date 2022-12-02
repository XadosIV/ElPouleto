import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

class Moskito(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        self.rect.width = 16
        self.rect.height = 16
        #Vitesse aléatoire de l'ennemi
        self.stats.speed = 300
        #Chargement de l'image
        self.sprite = self.images.get("enemies/moskito") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
        self.life = 50 #Vie de l'ennemi
        self.damage = 120
        self.flying = True
        self.type = "moskito" #Le type de l'entité / son nom.
        self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
        self.direction_hurt = 1
        #Compteurs
        self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
        self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre
        self.cpt_frame = 0 #Compteur de frames, pour les animations du bird.

    def update(self):
        if self.life > 0:
            if self.cd_hurt != 0:
                self.cd_hurt -= 1
                self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt
            else:
                #comportement normal
                vecPlayer = pygame.math.Vector2([self.game.player.rect.x, self.game.player.rect.y])
                vecMoi = pygame.math.Vector2([self.rect.x, self.rect.y])
                vecDirection = vecPlayer - vecMoi
                if vecDirection.length_squared() != 0:
                    vecDirection.normalize_ip()
                    self.velocity = vecDirection * self.stats.speed * self.game.dt
                else:
                    self.velocity = pygame.math.Vector2(0)
        else: #Supprime si plus de vie			
            if not self.timer_disappear.running:
                self.game.enemies.remove(self)
                self.timer_disappear.start()	
                self.velocity[0] = 0
                self.flying = False
            if self.timer_disappear.ended:
                self.delete()

        if self.velocity[0] > 0:
            self.direction = 1
        else:
            self.direction = -1

        return Entity.update(self)

    def hurt(self, damage, hitter):
        self.life -= damage
        if hitter.rect.x > self.rect.x:
            self.direction_hurt = -1
        else:
            self.direction_hurt = 1
            self.cd_hurt = 30