class Stats():
	def __init__(self, opt={}):
		self.speed = 300
		self.jumpforce = 600
		self.jump_max = 1
		self.glide = 0 #en secondes
		self.dash = 0 #en frame
		self.cd_dash = 60 #en frame
		self.size = 1
		self.life = 500
		self.lifemax = 500

		self.dict = self.__dict__.copy()

		for (k,v) in opt:
			if getattr(self, k) != None:
				setattr(self, k, v)

	def base_stats(self):
		return self.dict