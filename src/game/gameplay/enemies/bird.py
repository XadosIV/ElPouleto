import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

flying = True

class Bird(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        #Vitesse
        self.area = [x-200, x+200, y-200, y+200] #Taille de l'endroit pù peut se déplacer l'oiseau
        self.stats.speed = 150
        #Chargement de l'image
        self.sprite = self.images.get("enemies/bird0") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
        self.flying = flying
        self.stats.life = 100 #Vie de l'ennemi
        self.damage = 80
        self.type = "bird" #Le type de l'entité / son nom.
        self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
        self.direction_hurt = 1
        self.flying = flying
        #Compteurs
        self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
        self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre
        self.cpt_frame = 0 #Compteur de frames, pour les animations du bird.

    def update(self):
        if self.stats.life > 0: #S'il est en vie
            if self.cd_hurt != 0: #Si touché par le joueur
                self.cd_hurt -= 1 
                self.velocity[0] = (self.cd_hurt*4 + 1) * self.direction_hurt * self.game.dt #Knockback de l'ennemi
            else:
                if self.rect.x < self.area[0] or self.rect.x > self.area[1]: #S'il sort de l'area à gauche ou à droite
                    self.direction *= -1 #Changement de direction
                if self.rect.y < self.area[2]: #S'il sort de l'area en haut
                    self.velocity[1] += 5
                elif self.rect.y > self.area[3]: #S'il sort de l'area en bas
                    self.velocity[1] -= 5
                else: #Sinon déplacement aléatoires de temps en temps
                    if random.randint(1,10) == 1:
                        self.velocity[1] += 1
                    elif random.randint(1,10) == 2:
                        self.velocity[1] -= 1
                    if random.randint(1,50) == 1:
                        self.direction *= -1

                self.velocity[0] = self.stats.speed * self.direction * self.game.dt #Vitesse        

        else: #Supprime si plus de vie			
            if not self.timer_disappear.running: #Temps pendant lequel son corps est toujours visible
                self.game.enemies.remove(self)
                self.timer_disappear.start()	
                self.velocity[0] = 0
                self.flying = False
            if self.timer_disappear.ended:
                self.game.entities.remove(self)

        return Entity.update(self)

    def updateSprite(self):
        self.cpt_frame += 1
        if self.cpt_frame == 16:
            self.cpt_frame = 0
        if self.stats.life <= 0: #S'il est mort il prend le sprite mort
            self.sprite = self.images.get("enemies/bird_dead")
        else:
            if self.velocity[0] == 0: #Sinon animations de vol
                self.sprite = self.images.get("enemies/bird0")
            else:
                self.sprite = self.images.get("enemies/bird"+str(self.cpt_frame//5))

    def hurt(self, damage, hitter):
        self.stats.life -= damage
        if hitter.rect.x > self.rect.x:
            self.direction_hurt = -1
        else:
            self.direction_hurt = 1
            self.cd_hurt = 30
    
    def draw(self, offset):
        self.updateSprite()
        super().draw(offset)