import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

class Bird(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        #Vitesse aléatoire de l'ennemi
        self.area = [x-200, x+200, y-200, y+200] #Taille de l'endroit pù peut se déplacer l'oiseau
        self.stats.speed = 150
        #Chargement de l'image
        self.sprite = self.images.get("enemies/bird0") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
        self.life = 100 #Vie de l'ennemi
        self.damage = 80
        self.type = "bird" #Le type de l'entité / son nom.
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
                if self.rect.x < self.area[0] or self.rect.x > self.area[1]: #S'il sort de l'area
                    self.direction *= -1
                if self.rect.y < self.area[2]:
                    self.velocity[1] = self.stats.speed * self.direction * self.game.dt
                elif self.rect.y > self.area[3]:
                    self.velocity[1] = - self.stats.speed * self.direction * self.game.dt

                if random.randint(1,2) == 2:
                    self.velocity[1] = self.stats.speed * self.direction * self.game.dt
                if random.randint(1,50) == 1:
                    self.direction *= -1

                self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse        

        else: #Supprime si plus de vie			
            if not self.timer_disappear.running:
                self.game.enemies.remove(self)
                self.timer_disappear.start()	
                self.velocity[0] = 0
                self.velocity[1] = 0
            if self.timer_disappear.ended:
                self.game.entities.remove(self)

        Entity.update(self)
        return self.velocity

    def updateSprite(self):
        self.cpt_frame += 1
        if self.cpt_frame == 16:
            self.cpt_frame = 0
        if self.stats.life <= 0:
            self.sprite = self.images.get("enemies/bird_dead")
        else:
            if self.velocity[0] == 0:
                self.sprite = self.images.get("enemies/bird0")
            else:
                self.sprite = self.images.get("enemies/bird"+str(self.cpt_frame//5))

    def hurt(self, damage, hitter):
        self.life -= damage
        if hitter.rect.x > self.rect.x:
            self.direction_hurt = -1
        else:
            self.direction_hurt = 1
            self.cd_hurt = 30
    
    def draw(self, offset):
        self.updateSprite()
        super().draw(offset)