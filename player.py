import tkinter

class Player:
	flags = int('10011000', 2)
	def __init__(self, name, attack, defense, regeneration, health, description):
		self.name = name
		self.attack = attack
		self.defense = defense
		self.regeneration = regeneration
		self.health = health
		self.gold = 0
		self.room = [10, "Unknown Location"]
		self.description = description
		
	def updateCharacter(self, newDescription):
		self.name = newDescription[0]
		flags = newDescription[1]
		self.attack = newDescription[2]
		self.defense = newDescription[3]
		self.regeneration = newDescription[4]
		self.health = newDescription[5]
		self.gold = newDescription[6]
		self.description = newDescription[9]

	def getName(self):
		return self.name

	def setName(self, n):
		while(len(n) < 32):
			n += "\0"
		self.name = n

	def getFlags(self):
		return self.flags

	def setFlags(self, f):
		self.flags = int(f, 2)

	def getAttack(self):
		return self.attack

	def setAttack(self, a):
		self.attack = int(a)

	def getDefense(self):
		return self.defense

	def setDefense(self, d):
		self.defense = int(d)

	def getRegeneration(self):
		return self.regeneration

	def setRegeneration(self, r):
		self.regeneration = int(r)

	def getHealth(self):
		return self.health	

	def setHealth(self, h):
		self.health = int(h)

	def getGold(self):
		return self.gold

	def setGold(self, g):
		self.gold = int(g)
		
	def getRoom(self):
		return self.room

	def setRoom(self, r):
		self.room = r

	def getDescriptionLen(self):
		return len(self.description)

	def getDescription(self):
		return self.description

	def setDescription(self, d):
		self.description = d


play = Player("name", 0, 0, 0, 100, "X") 
