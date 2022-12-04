import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

flying = True

class Moskito(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        self.rect.width = 16
        self.rect.height = 16
        #Vitesse
        self.stats.speed = 220
        #Chargement de l'image
        self.sprite = self.images.get("enemies/moskito") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
        self.stats.life = 50 #Vie de l'ennemi
        self.damage = 120
        self.flying = flying
        self.type = "moskito" #Le type de l'entité / son nom.
        self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
        self.direction_hurt = 1
        #Compteurs
        self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
        self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre

    def update(self):
        if self.stats.life > 0: #Si en vie
            if self.cd_hurt != 0: #Si pas touché par le joueur
                self.cd_hurt -= 1
                self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt #Knockback
            else:
                #comportement normal
                vecPlayer = pygame.math.Vector2([self.game.player.rect.x, self.game.player.rect.y]) #Vecteur du player
                vecMoi = pygame.math.Vector2([self.rect.x, self.rect.y]) #Vecteur du moskito
                vecDirection = vecPlayer - vecMoi #Vecteur entre les 2
                if vecDirection.length_squared() != 0: 
                    vecDirection.normalize_ip()
                    self.velocity = vecDirection * self.stats.speed * self.game.dt #Se dirige vers le joueur
                else:
                    self.velocity = pygame.math.Vector2(0)
        else: #Supprime si plus de vie			
            if not self.timer_disappear.running: #Timer pendant lequel il reste "mort" sur l'écran
                self.game.enemies.remove(self)
                self.timer_disappear.start()	
                self.velocity[0] = 0
                self.flying = False
            if self.timer_disappear.ended:
                self.delete()

        if self.velocity[0] > 0: #Ajustement de la direction
            self.direction = 1
        else:
            self.direction = -1

        return Entity.update(self)

    def hurt(self, damage, hitter):
        self.stats.life -= damage
        if hitter.rect.x > self.rect.x:
            self.direction_hurt = -1
        else:
            self.direction_hurt = 1
            self.cd_hurt = 30