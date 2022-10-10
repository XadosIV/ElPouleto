

class Stats():
	def __init__(self, opt={}):
		self.glide = 0
		self.speed = 300
		self.jumpforce = 600
		self.jump_max = 1
		self.fallspeed = 32
		self.size = 1
		for (k,v) in opt:
			if getattr(self, k) != None:
				setattr(self, k, v)

	def base_stats(self):
		return {"glide":0, "speed":300, "jumpforce":600, "jump_max":1, "fallspeed":32, "size":1}