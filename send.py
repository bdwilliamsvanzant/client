from player import *
from conn import *
import tkinter
import struct
#from main import msg_list


class Send():
	message = ""
	def sendCharacter(self):
		packet = bytearray()
		characterFunctions = [(10).to_bytes(1, "little"), 	#message type
			(play.getName()).encode('utf-8'), 				#playername
			(play.getFlags()).to_bytes(1, "little"),		#flag
			(play.getAttack()).to_bytes(2, "little")] 		#desc	
		for i in characterFunctions:
			packet += i
		s.send(packet)
		return 
	
	def startGame(self):
		s.send((6).to_bytes(1, "little"))
		
	def leaveGame(self):
		s.send((12).to_bytes(1, "little"))
		
	def holdMessage(self, m):
		global message
		message = m
		

	def sendMessage(self, recipient):
		global message
		packet = bytearray()
		packet += (1).to_bytes(1, "little")				#type
		packet += len(message).to_bytes(2, "little")	#message length
		while(len(recipient) < 32):
			recipient += '\0'
		packet += (recipient).encode('utf-8')			#recipient
		packet += (play.getName()).encode('utf-8')		#sender
		packet += (message).encode('utf-8')				#message
		s.send(packet)		
		
	def sendChangeRoom(self, ml):
		room = int(ml.get())
		packet = bytearray()
		packet += (2).to_bytes(1, "little")
		packet += (room).to_bytes(2, "little")
		s.send(packet)
		
	def fightMonster(self):
		packet = bytearray()
		packet += (3).to_bytes(1, "little")
		s.send(packet)
		
	def fightPlayer(self, ml):
		player = ml.get()
		while(len(player) < 32):
			player += "\0"
		packet = bytearray()
		packet += (4).to_bytes(1, "little")
		packet += (player).encode('utf-8')
		s.send(packet)

	def lootPlayer(self, ml):
		victim = ml.get()
		while(len(victim) < 32):
			victim += "\0"
		packet = bytearray()
		packet += (4).to_bytes(1, "little")
		packet += (victim).encode('utf-8')
		s.send(packet)
sender = Send()

