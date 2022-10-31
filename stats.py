class Stats():
	def __init__(self, opt={}):
		self.speed = 300 #Vitesse
		self.jumpforce = 600 #Hauteur de saut
		self.jump_max = 1 #Nombre max de sauts
		self.glide = 0 #Planer
		self.size = 1 #Taille du joueur
		self.can_dash = True #Possibilité de dash
		self.life = 500 #Vie actuelle
		self.lifemax = 500 #Vie maximale

		self.dict = self.__dict__.copy() #Pour avoir toutes les stats de base

		for (k,v) in opt: #On ajoute les stats données dans l'initialisation
			if getattr(self, k) != None:
				setattr(self, k, v)

	def base_stats(self):
		return self.dict