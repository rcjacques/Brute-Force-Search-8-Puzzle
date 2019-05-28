'''
@Author: Rene Jacques
February 25, 2019
'''

class Node:
	'''Node used as a storage object to keep track of specific data, node location in tree (ID), and node parent'''
	def __init__(self):
		self.data = None
		self.data_number = None
		self.parent = None
		self.children = []
		self.id = None
		self.cost = None

	def setCost(self,c):
		'''Set cost to reach for this node'''
		self.cost = c 

	def getCost(self):
		'''Return cost to reach'''
		return self.cost

	def setData(self,d):
		'''Set data for this node'''
		self.data = d 

	def getData(self):
		'''Return data'''
		return self.data

	def setID(self,i):
		'''Set node ID'''
		self.id = i

	def getID(self):
		'''Return node ID'''
		return self.id

	def setParent(self,p):
		'''Set node parent'''
		self.parent = p

	def getParent(self):
		'''Return node parent'''
		return self.parent