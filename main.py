
"""
Known bugs ---
	duplicate monsters
	duplicate rooms?
	hardcode XP

"""
from conn import *
from receive import *
from send import *
from player import *
import tkinter
import time
import re

characterList = []
connectionList = []

temp = ""
killThread = False
promptIndex = 0

def receive(): #the complications with closing are this
	while True:
		try:
			type = ord(s.recv(1))
			print("Type: " + str(type))
			msg = checkType(type, msg_list)
			if(type == 7 or type == 8 or type == 11):
				msg_list.insert(tkinter.END, msg)
			elif(type == 1): #Message
				if(msg[1] == play.getName() and msg[2] != play.getName()):
					msg_list.insert(tkinter.END, "\n" + re.sub('\0', '', msg[2]) + ": "
						+ re.sub('\0', '', msg[3]))
			elif(type == 9): #Room Description
				play.setRoom(msg)
				msg_list.insert(tkinter.END, "\nYou are in the " + re.sub('\0', '', msg[1]) +  ".")
				msg_list.insert(tkinter.END, "\n" + str(msg[2]))
				updateCharacterScreen()
			elif(type == 10): #character
				print(msg[1])
				print(play.getName())
				if(msg[0] != play.getName() and msg not in characterList):
					characterList.append(msg)
				elif(msg[0] == play.getName()):
					play.updateCharacter(msg)
					updateCharacterScreen()
					
				monsterDisplay.delete(1.0, 'end')
				print(characterList)
				for c in characterList:
					monsterDisplay.insert(tkinter.END, re.sub('\0', '', c[0]) + ": " 
						+ str(c[5]) + "\n")

			elif(type == 13): #Connections
				connectionList.append(msg)
				connectionDisplay.delete(1.0, 'end')
				for c in connectionList:
					if(c[0] != play.getRoom()[0]):
						connectionDisplay.insert(tkinter.END, str(c[0]) + ": "
							+ re.sub('\0', '', c[1]) + "\n")	
		except OSError:
			pass
		msg_list.see(tkinter.END)
	
def exit(event=None): 
	sender.leaveGame()
	#killThread = True
	#s.close()
	gui.quit()
	
def switchFight(event=None):
	flags = play.getFlags()
	stringFlag = str(bin(flags))[2:]
	if(stringFlag[1] == '1'):
		stringFlag = stringFlag[0] + '0' + stringFlag[2:] 
		msg_list.insert(tkinter.END, ("\nAuto fight has been turned off.\n"))
		msg_list.see(tkinter.END)
	else:
		stringFlag = stringFlag[0] + '1' + stringFlag[2:]
		msg_list.insert(tkinter.END, ("\nAuto fight has been turned on.\n"))
		msg_list.see(tkinter.END)
	play.setFlags(stringFlag)
	updateCharacterScreen()

def updateCharacterScreen():
	playerDisplay.delete(1.0, 'end')
	playerDisplay.insert(tkinter.END, ("Name: " + re.sub('\0', '', play.getName())) + "\n")
	playerDisplay.insert(tkinter.END, ("Health: " + str(play.getHealth())) + "\n")
	playerDisplay.insert(tkinter.END, ("Attack: " + str(play.getAttack())) + "\n")
	playerDisplay.insert(tkinter.END, ("Defense: " + str(play.getDefense())) + "\n")
	playerDisplay.insert(tkinter.END, ("Regeneration: " + str(play.getRegeneration())) + "\n")
	playerDisplay.insert(tkinter.END, ("Gold: " + str(play.getGold())) + "\n")
	playerDisplay.insert(tkinter.END, ("Room Num: " + str(play.getRoom()[0])) + "\n")
	playerDisplay.insert(tkinter.END, ("Room Name: " + re.sub('\0', '', play.getRoom()[1])) + "\n")

	
def createCharacter():
	global promptIndex
	prompts = ["\n\tDescription: ","\n\tAttack: ", "\n\tDefense: ", "\n\tRegeneration: ","\nCharacter Created :D"]
	setters = [play.setName, play.setDescription, play.setAttack, play.setDefense, play.setRegeneration]
	response = my_msg.get()
	setters[promptIndex](response)
	msg_list.insert(tkinter.END, response)
	msg_list.see(tkinter.END)
	promptIndex += 1
	
	#Error checking to make sure stats equal 100
	if(promptIndex > 4 and ((play.getAttack() + play.getDefense() + play.getRegeneration()) != 100)):
		promptIndex -= 3
		msg_list.insert(tkinter.END, "\nAttack + Defense + Regeneration MUST equal 100 points. - \n")
		msg_list.insert(tkinter.END, prompts[promptIndex-1])
	elif(promptIndex > 4 and  ((play.getAttack() + play.getDefense() + play.getRegeneration()) == 100)):
		#this is what you want to happpen, if the conditions are met it sends new Charater
		#to the server
		msg_list.insert(tkinter.END, prompts[promptIndex-1])
		promptIndex -= 4
		send_button.configure(text="Send", command=send)
		
		#call function to send character to server
		sender.sendCharacter()
		sender.startGame()
		updateCharacterScreen()
	else:
		msg_list.insert(tkinter.END, prompts[promptIndex-1])
	msg_list.see(tkinter.END)
	my_msg.set("") 
		
def start(event=None):
	send_button.configure(text="Submit", command=createCharacter)
	msg_list.insert(tkinter.END,"Create character -\n\tName: ")
	my_msg.set("") 
	msg_list.see(tkinter.END)
	

def send(event=None): 
	msg_list.insert(tkinter.END,"\nTo who? -\n\tName: ")	
	msg = my_msg.get()
	sender.holdMessage(msg)
	my_msg.set("") 
	send_button.configure(text="Send", command= commenceSend)
	msg_list.see(tkinter.END)
	
def commenceSend(event=None):
	msg = my_msg.get()
	msg_list.insert(tkinter.END, msg)
	my_msg.set("") 
	sender.sendMessage(msg)
	send_button.configure(text="Send", command = send)
	
def loot(event=None):
	msg_list.insert(tkinter.END,"\nYou can only loot dead players- \n\tName: ")
	send_button.configure(text="Send", command= commenceLoot)
	msg_list.see(tkinter.END)

def commenceLoot(event=None):
	sender.lootPlayer(my_msg)
	send_button.configure(text="Submit", command=send)
	my_msg.set("") 
	
def fight(event=None):
	msg_list.insert(tkinter.END,"\nChoose player - \n\tPlayer Name: ")
	send_button.configure(text="Submit", command= commenceFight)
	msg_list.see(tkinter.END)
	
def commenceFight(event=None):
	global characterList
	characterList = []
	global connectionList
	connectionList = []
	monsterDisplay.delete(1.0, 'end')
	sender.fightPlayer(my_msg)
	send_button.configure(text="Send", command=send)
	my_msg.set("") 

	
def updateMonsterScreen():
	monsterDisplay.delete(1.0, 'end')
	for c in characterList:
		if(c[7] == (play.getRoom())[0]): #need to make sure in same room
			monsterDisplay.insert(tkinter.END, re.sub('0', '', c[0]) + ": " 
				+ str(c[5]) + "\n")
			msg_list.see(tkinter.END)
	
def changeRoom(event=None):
	msg_list.insert(tkinter.END,"\nChange room enter value from list - \n\tRoom Number: ")
	send_button.configure(text="Submit", command= commenceChangeRoom)
	msg_list.see(tkinter.END)

def commenceChangeRoom(event=None):
	global connectionList
	global characterList
	connectionList = []
	characterList = []
	sender.sendChangeRoom(my_msg)
	send_button.configure(text="Send", command=send)
	my_msg.set("") 
	updateMonsterScreen()

	




'''
	THIS IS MY GUI
'''

gui = tkinter.Tk()	
gui.title("Lurk Interface")

'''
	THIS IS MY MENU
'''
menu = tkinter.Frame(gui)

exit_button = tkinter.Button(menu, text="Quit", compound="top", command=exit)
exit_button.pack(side="left", pady = 5, padx = 10)

start_button = tkinter.Button(menu, text="Start", compound="bottom",command=start)
start_button.pack(side="left", pady = 5, padx = 10)

room_button = tkinter.Button(menu, text="Change Room", compound="bottom",command=changeRoom)
room_button.pack(side="left", pady = 5, padx = 10)

fight_button = tkinter.Button(menu, text="Fight Monster", compound="bottom",command=sender.fightMonster)
fight_button.pack(side="left", pady = 5, padx = 10)

pvp_button = tkinter.Button(menu, text="Fight Player", compound="bottom",command=fight)
pvp_button.pack(side="left", pady = 5, padx = 10)

auto_button = tkinter.Button(menu, text="AutoFight", compound="bottom",command=switchFight)
auto_button.pack(side="left", pady = 5, padx = 10)

loot_button = tkinter.Button(menu, text="Loot", compound="bottom",command=loot)
loot_button.pack(side="left", pady = 5, padx = 10)

menu.pack(side="top")


'''
                    Right Frame                    
'''
messages_frame = tkinter.Frame(gui)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
''' Main Terminal '''
msg_list = tkinter.Text(messages_frame, height=30, width=50, wrap ='word')
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack(side="top")
''' Button and Text Box '''
entry_field = tkinter.Entry(messages_frame, width=50,textvariable=my_msg)
#entry_field.bind("<Return>", send)
entry_field.pack(side="left")
send_button = tkinter.Button(messages_frame, text="Send", command=send)
send_button.pack(side="right")
messages_frame.pack(side="right", padx = 5)
'''
                    Left Frame                   
'''
stat_frame = tkinter.Frame(gui)
''' Player Stats '''
playerLabel = tkinter.Label(stat_frame, text="Player Stats: ")
playerLabel.pack(side="top")
playerDisplay = tkinter.Text(stat_frame, height=10, width=30, wrap ='word')
playerDisplay.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
playerDisplay.pack(side="top")
''' Display Players/Monsters '''
monsterDisplay = tkinter.Text(stat_frame, height=10, width=30, wrap ='word')
monsterDisplay.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
monsterDisplay.pack(side="bottom")
monsterLabel = tkinter.Label(stat_frame, text="Players & Monster: ")
monsterLabel.pack(side="bottom", pady = 5)
''' Display Connections '''
connectionLabel = tkinter.Label(stat_frame, text="Room Connections: ")
connectionLabel.pack(side="top")
connectionDisplay = tkinter.Text(stat_frame, height=7, width=30, wrap ='word')
connectionDisplay.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
connectionDisplay.pack(side="top")

stat_frame.pack(side="left", padx = 5)


gui.protocol("WM_DELETE_WINDOW", exit)



receive_thread = Thread(target=receive)
receive_thread.start()


tkinter.mainloop()  # Starts GUI execution.

