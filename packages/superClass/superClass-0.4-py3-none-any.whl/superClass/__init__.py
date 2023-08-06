class superList(list):
	def simplify(self):
		out = []
		for i in self:
			if not(i in out):
				out.append(i)
		return out
	def sp(self):
		out = self.simplify()
		out.sort()
		return out
	def __getitem__(self, ind):
		if isinstance(ind,slice):
			start = step = stop = None
			if ind.start != None:
				start = ind.start%len(self)
			if ind.step != None:
				step = ind.step%len(self)
			if ind.stop != None:
				stop = ind.stop%len(self)
			return super().__getitem__(slice(start,step,stop))
		else:
			index = ind%len(self)
			return super().__getitem__(index)

class superFile(object):
	"""docstring for superFile"""
	def __init__(self, name, default=""):
		super(superFile, self).__init__()
		self.file = name
		self.create()
		self.update()
		if self.content == "":
			self.append(default)

	def create(self):
		self.append("")

	def update(self):
		temp = open(self.file, "r")
		text = temp.read()
		self.__content = text
		temp.close()

	@property
	def content(self):
		self.update()
		return self.__content

	@content.setter
	def content(self, value):
		temp = open(self.file, "w+")
		temp.write(value)
		temp.close()
		self.update()

	def append(self, value):
		temp = open(self.file, "a+")
		temp.write(value)
		temp.close()
		self.update()

	def line(self, value, char="\n"):
		self.append(char + value)

	def log(self, value, symbol = " :: "):
		import datetime
		self.line(str(datetime.datetime.now()) + symbol + value)

	def __str__(self):
		return self.content

	def __add__(self, other):
		return self.content + str(other)

	def __iadd__(self, other):
		self.append(str(other))
		return self.content

class superRandom():
	"""docstring for superRandom"""
	def __init__(self):
		super(superRandom, self).__init__()
		import random as rd
		self.rd = rd
	@staticmethod
	def randomCircle(self,radius=1):
		from math import cos,sin
		angle = self.rd.random() * 360
		x = cos(angle)*radius
		y = sin(angle)*radius
		return (x,y)
	@staticmethod
	def randomDisk(self,radius=1):
		from math import cos,sin
		radius = self.rd.random() * radius
		angle = self.rd.random() * 360
		x = cos(angle)*radius
		y = sin(angle)*radius
		return (x,y)
	@staticmethod
	def randomPoint(self, x=1, y=1):
		x = self.rd.random() * x
		y = self.rd.random() * y
		return (x,y)

class superPoint2D(object):
	"""docstring for superPoint2D"""
	def __init__(self, x=0, y=0, system="cart"):
		super(superPoint2D, self).__init__()
		self.x = x
		self.y = y
		self.system = system

	def __sub__(self,other):
		pass

	def dist(self, other):
		import math
		x = self.x - other.x
		y = self.y - other.y
		return math.sqrt(x**2 + y**2)

# import numpy as np
# import matplotlib.pyplot as plt

# # Fixing random state for reproducibility
# np.random.seed(19680801)

# circle2 = plt.Circle((0, 0), 0.5, color='b', fill=False)
# ax = plt.gca()
# ax.cla()
# ax.add_artist(circle2)
# N = 500
# points = [tst.randomPoint(0.5,0.5) for i in range(N)]
# x = [i[0] for i in points]
# y = [i[1] for i in points]
# colors = np.random.rand(N)
# area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

# plt.scatter(x, y, s=10, c=colors, alpha=0.5)
# plt.axis("equal")
# plt.show()
#print(tst.randomCircle(5))
		