class Stats():
	def __init__(self, opt={}):
		self.glide = 0
		self.speed = 300
		self.jumpforce = 600
		self.jump_max = 1
		self.fallspeed = 0
		self.size = 1
		self.can_dash = True
		self.can_glide = True
		self.life = 500
		self.lifemax = 500
		for (k,v) in opt:
			if getattr(self, k) != None:
				setattr(self, k, v)

	def base_stats(self):
		return {"glide":0, "speed":300, "jumpforce":600, "jump_max":1, "fallspeed": 0, "size":1, "can_dash":True, "life":500, "lifemax":500}