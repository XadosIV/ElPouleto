

class Stats():
	def __init__(self, opt={}):
		self.glide = 0
		self.speed = 300
		self.jumpforce = 600
		self.jump_max = 1
		for (k,v) in opt:
			if getattr(self, k) != None:
				setattr(self, k, v)