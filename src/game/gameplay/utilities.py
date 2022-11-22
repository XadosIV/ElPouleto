import os, pygame

class Timer():
	def __init__(self, maximum, game):
		self.max = maximum
		self.game = game
		self.game.timers.append(self)
		self.reset()

	def setMax(self, maximum):
		self.max = maximum
		if self.running:
			if self.current > self.max:
				self.current = self.max
		else:
			self.reset()

	def update(self):
		if self.running:
			if self.current != 0:
				self.current -= 1
				if self.current == 0:
					self.ended = True
					self.running = True

	def reset(self):
		self.current = self.max
		self.ended = True
		self.running = False

	def start(self, reset=False):
		if reset:
			self.reset()
		if not self.running:
			self.running = True
			self.ended = False

	def pause(self):
		self.running = False

	def resume(self):
		self.running = True

	def __str__(self):
		return f"TIMER : Current : {self.current} / Running : {self.running} / Ended : {self.ended} / Max : {self.max}"

class Galery():
	def __init__(self, path="./resources"):
		self.imgs = {}
		self.assetsDir = path
		self.load(path)

	def load(self, path):
		for file in os.listdir(path):
			relativePath = path+"/"+file
			if os.path.isdir(relativePath):
				self.load(relativePath)
			else:
				self.imgs[relativePath[12:-4]] = pygame.image.load(relativePath)

	def get(self, name="placeholder"):
		return self.imgs[name]

	def startsWith(self, start=""):
		dico = {}
		for k,v in self.imgs.items():
			if k.startswith(start):
				dico[k.split("/")[1]] = v
		return dico