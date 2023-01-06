from pygame.locals import *
import pygame

class Bindings():
	#Classe permettant de faire un lien entre une action en jeu et les touches appuyés par le joueur
	def __init__(self, game):
		self.game = game
		self.hold = ["left", "right", "lookUp", "lookDown", "glide"] #Touche pouvant être maintenu
		self.onHit = ["dash", "jump", "primary", "interact"] #Touche ne pouvant être maintenu
		#self.onHit = ["dash", "jump", "primary", "secondary", "worldPower", "pause", "inventory", "interact"] #Touche ne pouvant être maintenu
		self.keybind = {
			"left":K_LEFT,
			"right":K_RIGHT,
			"dash":K_d,
			"lookUp":K_UP,
			"lookDown":K_DOWN,
			"jump":K_SPACE,
			"primary":K_x,
			#"secondary":K_s,
			#"worldPower":K_q,
			#"pause":K_ESCAPE,
			#"inventory":K_e,
			"interact":K_c,
			"glide":K_SPACE
		}
		

	def getInputs(self):
		inputs = {
			"left":False,
			"right":False,
			"dash":False,
			"lookUp":False,
			"lookDown":False,
			"jump":False,
			"passBot":False,
			"glide":False,
			"primary":False,
			"secondary":False,
			"worldPower":False,
			"pause":False,
			"inventory":False,
			"interact":False
		}
		#Touches maintenus = True
		keys = self.game.keys
		for key in self.hold:
			inputs[key] = keys[self.keybind[key]]

		#Touche à l'appui = True
		events = self.game.events
		for event in events:
			if event.type == pygame.KEYDOWN:
				for key in self.onHit:
					inputs[key] = event.key == self.keybind[key]
		
		#Passer à travers les blocs passable
		if inputs["glide"] and inputs["lookDown"]:
			inputs["glide"] = False
			inputs["lookDown"] = False
			inputs["jump"] = False
			inputs["passBot"] = True

		if inputs["jump"]:
			inputs["glide"] = False

		return inputs