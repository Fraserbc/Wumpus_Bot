#Import the db handler for the profiles
import db_handler

#we need json here
import json

#Function for proccessign the profiles
def get_profile(id):
	#Get the data from the db
	profile = db_handler.get_profile(id)

	#Proccess the profile picture
	profile["pfp"] = json.loads(profile["pfp"])

	image = profile["pfp"]["wumpus"] + profile["pfp"]["badge"] + profile["pfp"]["extra"]
	
	return "Images/{}.png".format(image)

#Turn the words into short abreviations for the db
abbr = {
	"bandana":"ban",
	"monocle":"mon",
	"headband":"head",
	"moustache":"mous",
	"pipe":"pipe",
	"hackweek":"hack",
	"lgbt":"lgbt",
	"black":"black",
	"white":"polar",
	"brown":"brown",
	"none":"none"
}

#Ask a question and get a response
async def ask_question(channel, title, question, error_message, answers, client, discord):
	#Ask the question
	embed = discord.Embed(title=title, description=question, color=0x972ed9)
	await client.send_message(channel, embed=embed)
	
	#Check the answer and tell bots no
	while True:
		#Wait for answer
		r = await client.wait_for_message(channel=channel)
		
		#No bad bot
		if r.author.bot:
			return
		
		#Lowercase becuase people do this BrOwN
		r = r.content.lower()
		
		answer = ""
		for x in answers:
			if r == x:
				answer = x
		
		if answer != "":
			break
		
		embed = discord.Embed(title=title, description=error_message, color=0x972ed9)
		await client.send_message(channel, embed=embed)
	
	return answer

#Build-a-Wumpus
async def build_a_wumpus(discord, client, channel, userid):
	#Show the usage for Build-a-Wumpus
	desc = """
	You will be prompted to answer questions that will build your wumpus!
	"""
	embed = discord.Embed(title="Build-a-Wumpus", description=desc, color=0x972ed9)
	await client.send_message(channel, embed=embed)

	#Ask for color
	color = await ask_question(channel, "Build-a-Wumpus", "What color do you want your Wumpus to be? White, Black, Brown", "That wasn't a valid color!\nPlease enter White, Black, Brown", ["white", "black", "brown"], client, discord)

	#If bot, stop
	if color == None:
		return

	#Ask what badge they want
	badge = await ask_question(channel, "Build-a-Wumpus", "What badge do you want you wumpus to have? LGBT, HackWeek or None", "That wasn't a valid badge!\nPlease enter LGBT, HackWeek or None", ["hackweek", "lgbt", "none"], client, discord)

	#If bot, stop
	if badge == None:
		return

	#Ask what badge they want
	extra = await ask_question(channel, "Build-a-Wumpus", "What extra do you want you wumpus to have? Bandana, Monocle, Headband, Moustache, Pipe or None", "That wasn't a valid extra!\nPlease enter Bandana, Monocle, Headband, Moustache, Pipe or None", ["bandana", "monocle", "headband", "moustache", "pipe", "none"], client, discord)
	
	#If bot, stop
	if extra == None:
		return

	#Tell them their wumpus is being proccessed
	embed = discord.Embed(title="Build-a-Wumpus", description="Your Wumpus is now being proccessed!", color=0x972ed9)
	await client.send_message(channel, embed=embed)

	#Proccess the badge and extras in a way the profile command can understand
	badge = abbr[badge]
	extra = abbr[extra]
	color = abbr[color]

	#Write to the db
	db_handler.set_profile(userid, color, badge, extra)

	#Show them their glorius wumpus
	image = get_profile(userid)
	await client.send_file(channel, image)

	return