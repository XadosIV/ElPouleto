import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
import random

flying = True

class Firefly(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        self.rect.width = 32
        self.rect.height = 32
        #Vitesse
        self.stats.speed = 250
        #Chargement de l'image
        self.sprite = self.images.get("enemies/firefly0") #Sans paramètre, ça renvoie le placeholder (carré rouge)		
        self.stats.life = 1 #Vie de l'ennemi
        self.damage = 180
        self.flying = flying
        self.type = "firefly" #Le type de l'entité / son nom.
        self.game.enemies.append(self) #Ajout dans la liste d'ennemis		
        self.direction_hurt = 1
        #Compteurs
        self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
        self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre
        self.cpt_frame = 0 #Compteur de frames, pour les animations du firefly


    def update(self):
        if self.stats.life > 0: #S'il est en vie
            #comportement normal
            vecPlayer = pygame.math.Vector2([self.game.player.rect.x, self.game.player.rect.y])
            vecMoi = pygame.math.Vector2([self.rect.x, self.rect.y])
            vecDirection = vecPlayer - vecMoi
            if vecDirection.length_squared() != 0:
                vecDirection.normalize_ip()
                self.velocity = vecDirection * self.stats.speed * self.game.dt
            else:
                self.velocity = pygame.math.Vector2(0)
            if self.rect.colliderect(self.game.player.rect):
                self.game.player.numberOfTimesHurtByFire += 1
                self.hurt(self.stats.life, self)
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

    def updateSprite(self):
        self.cpt_frame += 1
        if self.cpt_frame == 16:
            self.cpt_frame = 0
        if self.stats.life <= 0: 
            self.sprite = self.images.get("enemies/firefly_dead") #S'il meurt, image de mort
            rect = self.sprite.get_rect()
            rect.move_ip(self.rect.x, self.rect.y)
            self.rect = rect 
        else:
            self.sprite = self.images.get("enemies/firefly"+str(self.cpt_frame//5)) #Animations de vol

    def hurt(self, damage, hitter):
        self.stats.life -= damage

    def draw(self, offset):
        self.updateSprite()
        super().draw(offset)