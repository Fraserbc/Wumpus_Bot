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
	"lgbt":"lgbt"
}

#Build-a-Wumpus
async def build_a_wumpus(discord, client, channel, userid):
	#Show the usage for Build-a-Wumpus
	desc = """
	You will be prompted to answer questions that will build your wumpus!
	"""
	embed = discord.Embed(title="Build-a-Wumpus", description=desc, color=0x972ed9)
	await client.send_message(channel, embed=embed)

	#Ask for color
	embed = discord.Embed(title="Build-a-Wumpus", description="What color do you want your Wumpus to be? White, Black or Brown", color=0x972ed9)
	await client.send_message(channel, embed=embed)
	
	while True:
		r = await client.wait_for_message(channel=channel).lower()
		
		color = ""
		for x in ["white", "black", "brown"]:
			if r == x:
				color = x
		
		if color != "":
			break
		
		embed = discord.Embed(title="Build-a-Wumpus", description="That wasn't a valid color!\nPlease enter White, Black or Brown", color=0x972ed9)
		await client.send_message(channel, embed=embed)

	#Ask what badge they want
	embed = discord.Embed(title="Build-a-Wumpus", description="What badge do you want you wumpus to have? LGBT or HackWeek", color=0x972ed9)
	await client.send_message(channel, embed=embed)
	
	while True:
		r = await client.wait_for_message(channel=channel).lower()
		
		badge = ""
		for x in ["hackweek", "lgbt"]:
			if r == x:
				badge = x
		
		if badge != "":
			break
		
		embed = discord.Embed(title="Build-a-Wumpus", description="That wasn't a valid badge!\nPlease enter LGBT or HackWeek", color=0x972ed9)
		await client.send_message(channel, embed=embed)
	
	#Ask what badge they want
	embed = discord.Embed(title="Build-a-Wumpus", description="What extra do you want you wumpus to have? Bandana, Monocle, Headband, Moustache or Pipe", color=0x972ed9)
	await client.send_message(channel, embed=embed)
	
	while True:
		r = await client.wait_for_message(channel=channel).lower()
		
		extra = ""
		for x in ["bandana", "monocle", "headband", "moustache", "pipe"]:
			if r == x:
				extra = x
		
		if extra != "":
			break
		
		embed = discord.Embed(title="Build-a-Wumpus", description="That wasn't a valid extra!\nPlease enter Bandana, Monocle, Headband, Moustache or Pipe", color=0x972ed9)
		await client.send_message(channel, embed=embed)

	#Tell them their wumpus is being proccessed
	embed = discord.Embed(title="Build-a-Wumpus", description="Your Wumpus is now being proccessed!", color=0x972ed9)
	await client.send_message(channel, embed=embed)

	#Proccess the badge and extras in a way the profile command can understand
	badge = abbr[badge]
	extra = abbr[extra]

	#Write to the db
	db_handler.set_profile(id, color, badge, extra)

	return