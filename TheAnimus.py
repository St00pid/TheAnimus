#The Animus - Version 1.6
#Version Changes:
#1.0 initial game - each turn player's mood changes. each turn each player rolls two d6 dices which equals to their luck.
#luck + mood defines actions. 
#mood states = Fight, Search , Ponder 
#2 x 6 roll special action per mood.
#1.1 added legendary item limit. one char can never get the same item twice.
#if for any reason he gets all the items in the list everybody in The Animus universe will instantly die and the game will end.
#-----------------------------------
#1.2 added kill count to characters
#1.3 when a player gets a legendary item it's removed from the list
#1.4 when a player dies if he had an item in his inventory it will automatically go to the new winner
#1.5 added dragonballs. when a player dies dragonball will be transfered to the winner
#1.6 every 7 days game will print stats



import random
from random import randint
from random import randrange
from mainlist import legendary_items, mood, ponder, powerup, ways_to_die, playerdir, nofight, fight, enter
import time
import sys

class Player(object):
	def __init__(self, name, avatar):
		self.name = name
		self.avatar = avatar
		self.lifecondition = True
		self.items = []
		self.mood = ""
		self.luck = 0 
		self.kills = 0
		self.dragonballs = 0
		
	def death(self):
		self.lifecondition = False
	
	def roll_luck(self, luck):
		self.luck = luck
	
	def add_ball(self, dragonballs):
		self.dragonballs += dragonballs
	def erase_ball(self):
		self.dragonballs = 0

	def kill_count(self, kills):
		self.kills += kills
		
	def  add_items(self, item):
			self.items.append(item)
	
	def remove_items(self, item):
			self.items.remove(item)

	def change_mood(self, mood):
		self.mood = mood
	
	def __repr__(self):
		return repr(self.name)
		return repr(self.avatar)
		return repr(self.dragonballs)
	
	
		
# add players function


def addplayers(adictionary):
	players = []
	for key, value in adictionary.iteritems():
		key = Player("%s" % key, "[img]%s[/img]" % value)
		players.append(key)
	for player in players:
		print "%s" % player.avatar
		print "%s " % player.name + ''.join(random.choice(enter))
	return players

#randomly set mood each turn
def player_mood(playerlist, moodlist):
	for item in playerlist:
		mood = random.choice(moodlist)
		item.change_mood(mood)

#Give legendary items if summary of luck is 12 and if mood is "Search"

def gods_favor(player):
	if player.mood is 'Search' and player.luck == 12:
		item = random.choice(legendary_items)
		if player.items.count("%s" % item) == 1:
			item = random.choice(legendary_items)
			return item
		player.add_items(item)
		index_item = legendary_items.index(item)
		legendary_items.pop(index_item)
		print "%s" % player.avatar
		print "The Animus has bestowed its godly favor upon %s. " % player.name + \
		"%s has found a legendary item. %s's inventory now contains: %s." % (player.name, player.name, ','.join(player.items)),  \
		"%s's damage has increased tenfold" % player.name
	if player.mood is 'Ponder' and player.luck == 12:
		print "%s" % player.avatar
		print "%s has found a dragonball!" % player.name
		player.add_ball(1)
	if len(player.items) == len(legendary_items):
		print player.avatar
		print "%s has gathered all the legendary items that exist in the universe. Everybody else instantly dies." % player.name
		stats()
		sys.exit(0)
	if player.dragonballs == 7:
		print player.avatar
		print "%s has gathered all the dragonballs and summoned Shenron! He is now the most powerful being in the universe. Everybody else dies." % player.name
		stats()
		sys.exit(0)
	else:
		pass


#gods favor through the list
def favorcheck(players):
	for player in players:
		gods_favor(player)



#change luck each round function

def roll_dice():
	roll = random.randint(1,6), random.randint(1,6)
	roll = sum(roll)
	return roll

def roll(playerlist):
	for player in playerlist:
		roll = roll_dice()
		item_luck = len(player.items)
		roll = roll + item_luck
		player.roll_luck(roll)
		
		

#do something according to mood
def combat_mood(playerlist):
	fighters = []
	for player in playerlist:
		if player.mood is 'Fight':
			fighters.append(player)
	#for fighter in fighters:
		#print "%s is looking for a fight!" % fighter.name
	return fighters	

def ponder_mood(playerlist):
	for player in playerlist:
		if player.mood is 'Ponder':
			print "%s" % player.avatar
			print "%s " % player.name + ''.join(random.choice(ponder))


def search_mood(playerlist):
	for player in playerlist:
		if player.mood is 'Search':
			print "%s" % player.avatar
			print "%s " % player.name + "is aimlessly wandering around"
		
#function random death
def  random_death():
	n = len(fighters)
	roll = random.randint(1,2)
	if roll == 1:
		fighters.pop(n-1)
	else:
		print "%s" % fighters[n-1].avatar
		print "As %s was tactically avoiding battle he fell inside a hole and died a coward's death." % fighters[n-1].name
		fighters[n-1].death()
		players.remove(fighters[n-1])
		deadbeats.append(fighters[n-1])
		fighters.pop(n-1)
		
#fighter functions
#group them , remove odd participant 1/2 dies, sort by luck
def group_fight():
	if len(fighters) == 0:
		pass
	elif len(fighters) == 1:
		print "%s" % fighters[0].avatar
		print "%s " % fighters[0].name + ''.join(random.choice(nofight))
		fighters.pop(0)
	elif len(fighters) > 2 and len(fighters) % 2 != 0:
		n = len(fighters)
		print "%s" % fighters[n-1].avatar
		print "%s " % fighters[n-1].name + ''.join(random.choice(nofight))
		random_death()
		print "%s" % "".join(str(fighter.avatar) for fighter in fighters)
		print "%s are starting to fight!" % " and ".join(str(fighter.name) for fighter in fighters)
		fighters.sort(key=lambda fighter: fighter.luck, reverse=True)  
	elif len(fighters) % 2 == 0:
		print "%s," % "".join(str(fighter.avatar) for fighter in fighters)
		print "%s are starting to fight!" % " and ".join(str(fighter.name) for fighter in fighters)
		fighters.sort(key=lambda fighter: fighter.luck, reverse=True)

#win,  remove dead


def win_fight():
	n = len(fighters)
	x = len(players) 
	if n == 0:
		pass
	if n == 1:
		pass	
	elif n == 2 and x == 2:
		print ''.join(random.choice(fight))
		print "%s" % fighters[0].avatar
		print "%s " % fighters[0].name + ''.join(random.choice(powerup))
		fighters[0].kill_count(1)
		fighters[n-1].death()
		print "%s" % fighters[n-1].avatar
		print "%s " % fighters[n-1].name + ''.join(random.choice(ways_to_die))
		players.remove(fighters[n-1])
		deadbeats.append(fighters[n-1])
		del fighters[:]
	elif n > 2 or n == 2:
		print ''.join(random.choice(fight))
		fighters[n-1].death()
		print "%s" % fighters[n-1].avatar 
		print "%s " % fighters[n-1].name + ''.join(random.choice(ways_to_die))
		print "%s" % fighters[0].avatar
		print "%s has emerged victorious" % fighters[0].name
		if len(fighters[n-1].items) > 0:
			for item in fighters[n-1].items:
				fighters[n-1].remove_items(item)
				fighters[0].add_items(item)
			print fighters[0].avatar, fighters[n-1].avatar
			print "%s is salvaging %s's dead corpse and finds: %s" % (fighters[0].name, fighters[n-1].name, item)
		if fighters[n-1].dragonballs > 0:
			n = fighters[1].dragonballs
			fighters[0].add_ball(n)
			fighters[1].erase_ball()
			print fighters[0].avatar, fighters[1].avatar
			print "%s is salvaging %s's dead corpse and finds:%d dragonball" % (fighters[0].name, fighters[1].name, n)
		fighters[0].kill_count(1)
		print "The rest cowardly ran away to different directions..."
		players.remove(fighters[n-1])
		deadbeats.append(fighters[n-1])
		del fighters[:]
	





#remove the dead
#def alivecheck(players):
#	for player in players:
#		if player.lifecondition == False:
#			index = players.index(player)
#			players.pop(index)
#		else:
#			pass

def live_stats(alist):
	for player in alist:
		print player.avatar 
		print '\n' and player.name 
		print '\n' and "kills: %d" % player.kills
		print '\n' and "Backpack: %s" % player.items
		print '\n' and "Dragonballs: %d" % player.dragonballs
		

def dead_stats(alist):
	for player in alist:
		print player.name
		print '\n' and "kills: %d" % player.kills
		print '\n' and "Inventory: %s" % player.items
		print '\n' and "Dragonballs: %d" % player.dragonballs
		print "------------------"


#Game sum of functions

def game():
	player_mood(players, mood)
	ponder_mood(players)
	search_mood(players)
	if len(players) == 2:
		players[0].change_mood("Fight")
		players[1].change_mood("Fight")
	roll(players)
	favorcheck(players)

def stats():
	print "[center]"
	print "Day %d game stats:" % day
	live_stats(players)
	print ""
	print "Gone but not forgotten:"
	dead_stats(deadbeats)
	print "[/center]"

print '[center]'
print "Welcome to the Animus mortal."
print "[img]http://i.imgur.com/XjYW7NO.jpg[/img]"
deadbeats = []
players = addplayers(playerdir)
print ''
print ''
print ''
print "%s players have entered The Animus" %  len(players)
print "[img]http://static3.spilcdn.com/fa/200X120/2/2/156822/20140305043003_Anime-Star-Fighting.jpg[/img]"
print ''
print ''
print "The Animus - NF Games has Begun!!!"
print '[/center]'


day = 1
while len(players) > 1:
	print "[center]"
	print ''
	print "Day %d" % day
	game()
	fighters = combat_mood(players)	
	group_fight()
	win_fight()
	print ""
	day += 1
	print ''
	print "[/center]"
	if day & 7 == 0:
		stats()
	raw_input("Press Enter to continue...")
	if len(players) == 1:
		print "[center]"
		print "%s" % players[0].avatar
		print "%s is standing on a mountain of corpses, invincible under the sun." % players[0].name
		print "[/center]"
		stats()
		break
