import pygame
from pygame.locals import *
from src.game.gameplay.entity import Entity
from src.game.gameplay.utilities import Timer
from src.game.gameplay.projectile import Projectile

class FireShooter(Entity): #Initialisé comme une entité
    def __init__(self, game, x, y):
        Entity.__init__(self, game)
        self.score = 300
        #Point de spawn de l'ennemi
        self.rect.x = x 
        self.rect.y = y
        #Vitesse
        self.stats.speed = 150
        #Chargement de l'image
        self.sprite = self.images.get("enemies/fireshooter") #Sans paramètre, ça renvoie le placeholder (carré rouge)        
        self.stats.life = 200 #Vie de l'ennemi
        self.damage = 100
        self.type = "fireshooter" #Le type de l'entité / son nom.
        self.game.enemies.append(self) #Ajout dans la liste d'ennemis
        #Compteurs
        self.cd_hurt = 0 #Temps pendant lequel l'ennemi est intouchable + knockback
        self.timer_disappear = Timer(90, self.game) #Temps pendant lequel l'ennemi est mort avant de disparaitre
       
    def update(self):
         if self.stats.life > 0: #S'il est en vie
            if self.cd_hurt == 0: #Si pas touché par le joueur
                vecRect = pygame.math.Vector2(self.rect.center) #Vecteur du fireshooter
                vecPlayer = pygame.math.Vector2(self.game.player.rect.center) #Vecteur du joueur
                distPlayer = vecPlayer.distance_to(vecRect) #Distance des deux vecteurs
                vecPlayer = vecRect - vecPlayer
                if self.rect.x < self.game.player.rect.x: #Direction vers le joueur
                    self.direction = 1
                else:
                    self.direction = -1
                if distPlayer < 400:
                    if self.cd.ended:
                        Projectile(self, self.damage, angle=pygame.math.Vector2([0,0]).angle_to(vecPlayer))
                        self.cd.start(reset=True)
                    
         else: #Supprime si plus de vie
            if not self.timer_disappear.running:
                self.game.score += self.score
                self.sprite = pygame.transform.rotate(self.sprite, -45)
                self.game.enemies.remove(self)
                self.timer_disappear.start()    
                self.velocity[0] = 0
            if self.timer_disappear.ended:
                self.game.entities.remove(self)

         return Entity.update(self)

    