class Stats():
	def __init__(self, opt={}):
		self.speed = 300
		self.jumpForce = 17
		self.jumpMax = 1
		self.glide = 0 #en secondes
		self.dash = 0 #en frame
		self.cd_dash = 60 #en frame
		self.size = 1 #En pourcentage (1 = 100%)
		self.lifeMax = 500
		self.life = self.lifeMax
		self.extraLife = 0

		self.dict = self.__dict__.copy() #Pour avoir toutes les stats de base

		for (k,v) in opt: #On ajoute les stats données dans l'initialisation
			if getattr(self, k) != None:
				setattr(self, k, v)

	def base_stats(self):
		return self.dict