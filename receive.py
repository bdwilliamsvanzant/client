'''
This file will analyzes incoming packages from server
and will adjust do the nescessary operations
'''
from conn import *
from player import *

		
'''
	AFTER THE FIRST BIT IS READ IN IT GOES TO THIS FUNCTION TO DETERMINE THE MESSAGE TYPE
	AND PASS IT TO THE CORRECT FUNCTION TO HANDLE IT
'''

def checkType(x, ml):
	if(x == 1):
		return messageMessage()
	elif (x == 7):
		return errorMessage()
	elif (x == 8):
		return acceptMessage(ml)
	elif (x == 9):
		return roomMessage()
	elif (x == 10):
		return characterMessage()
	elif (x == 11):
		return gameMessage()
	elif (x == 13):
		return connectionMessage()
	else:
		return "somethings a miss"
		
'''
	ALL THE DIFFERENT MESSAGE HANDLING FUNCTIONS, IN ORDER BY THEIR NUMBER
'''

def messageMessage():
	messageLen = ord(s.recv(1)) + ord(s.recv(1))
	recipient = (s.recv(32)).decode('utf-8')
	sender = (s.recv(32)).decode('utf-8')
	message = (s.recv(messageLen)).decode('utf-8')
	messageArray = [messageLen, recipient, sender, message]
	return messageArray

def errorMessage():
	code = ord(s.recv(1)) 
	messageLen = ord(s.recv(1))  + ord(s.recv(1)) 
	message = s.recv(messageLen) 

	#from server to client
	#stat violations, inappropriate room connections, etc
	return message

def acceptMessage(ml):
	acceptanceType = ord(s.recv(1))
	if(acceptanceType == 1):
		returnMessage = "\nMessage sent."
	elif (acceptanceType == 2):
		returnMessage = "\nYou have changed rooms."
	elif (acceptanceType == 3):
		returnMessage = "\nFighting monster..."
	elif (acceptanceType == 4):
		returnMessage = "\nFighting player..."
	elif (acceptanceType == 5):
		returnMessage = "\nCommence the loot..."
	elif (acceptanceType == 6):
		returnMessage = "\nGame has started."
	elif (acceptanceType == 10):
		returnMessage = "\n...Player has entered the game."
	elif (acceptanceType == 12):
		returnMessage = "\nYou have successfully left the game."
	else: 
		returnMessage = "\nPROBLEM IN THE FORCE (ACCEPT MESSAGE)"
	#server to player
	#response to change room or start
	return returnMessage

def roomMessage():
	roomNum = ord(s.recv(1)) + ord(s.recv(1)) 
	roomName = (s.recv(32)).decode('utf-8')
	roomDescriptionLen = ord(s.recv(1)) + ord(s.recv(1)) 
	roomDescription = (s.recv(roomDescriptionLen)).decode('utf-8')
	roomArray = [roomNum, roomName, roomDescription, roomDescriptionLen]
	#sent be server to describe roomm
	#player is in
	return roomArray

def characterMessage():
	name = (s.recv(32)).decode('utf-8')
	flag = ord(s.recv(1))
	attack = ord(s.recv(1)) + ord(s.recv(1)) 
	defense = ord(s.recv(1)) + ord(s.recv(1)) 
	regeneration = ord(s.recv(1)) + ord(s.recv(1)) 
	health = ord(s.recv(1)) + ord(s.recv(1)) 
	gold = ord(s.recv(1)) + ord(s.recv(1)) 
	room = ord(s.recv(1)) + ord(s.recv(1)) 
	descriptionLen = ord(s.recv(1)) + ord(s.recv(1)) 
	description = (s.recv(descriptionLen)).decode('utf-8')
	characterStatArray = [name, flag, attack, defense, regeneration,
	health, gold, room, descriptionLen, description]
	#both client and server shows changes to player status
	#let you know about other players
	#used when creating new character, or reviving dead one
	return characterStatArray

def gameMessage(): 
	#server uses it to describe the game this is the first one we recieve only ever sent once
	#pulling final data from packet
	points = ord(s.recv(1)) + ord(s.recv(1)) 
	statlimit = ord(s.recv(1)) + ord(s.recv(1)) 
	descriptionLen = ord(s.recv(1)) + ord(s.recv(1))  
	description = s.recv(descriptionLen * 8)
	return description

def connectionMessage():
	roomNum = ord(s.recv(1)) + ord(s.recv(1)) 
	roomName = (s.recv(32)).decode('utf-8')	
	roomDescriptionLen = ord(s.recv(1)) + ord(s.recv(1)) 
	roomDescription = (s.recv(roomDescriptionLen)).decode('utf-8')
	connectionArray = [roomNum, roomName, roomDescriptionLen, roomDescription]
	#server uses to describe
	#room connections to the user
	return connectionArray
	
