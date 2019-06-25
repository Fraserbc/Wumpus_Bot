#Needed imports
import discord, sys, json
from asyncio import sleep

#import the command auto complete and test
import command

#Set the client instance
client = discord.Client()

#Load the token
with open("config.json", "r") as conf_file:
	config = json.load(conf_file)

token = config["token"]

#Runs when they bot starts
@client.event
async def on_ready():
	print("The Wumpus is ready!")
	
	#Automatically update the status to show usercount
	client.loop.create_task(update_status())
	print("Started update_status()")

#Dealign with commands
@client.event
async def on_message(message):
	#Ingore any messages from bots
	if (message.author.bot):
		return

	#Test and autocomplete the command
	cmd = command.test_command(message.content, message.server.id)

	#It doesn't start with the prefix ignore it
	if cmd["status"] == 4:
		return

	#If the status was 0 (not a valid command or it doesn't start with the prefix)
	if cmd["status"] == 0:
		await client.send_message(message.channel, "That wasn't a valid command! Use {}help for a list of commands!".format(cmd["prefix"]))
		return
	
	#If there are multiple matches suggest them to the user
	if cmd["status"] == 2:
		text = '\n    {}'.format( cmd["prefix"] ).join( [""] + cmd["matches"] )
		await client.send_message(message.channel, "Did you mean:{}".format(text))
		return
	
	#If something broken
	if cmd["status"] == -1:
		await client.send_message(message.channel, "Well... this is awkward. Something broke and will be fixed soon")
		return
	
	#If all the checks passed then get the command and arguments
	args = cmd["args"]
	prefix = cmd["prefix"]
	cmd = cmd["matches"][0]

	#Stop the bot
	if cmd == "stop":
		sys.exit()
	
	#Show the help/usage message
	if cmd == "help":
		await client.send_message(message.channel, """
Wumpus Bot Help
		{p}botstats - Shows statistics about the bot
		{p}help - Shows this help message
		{p}blacksmiths - Lists the development team
		{p}ping - Pong!
		{p}code - Link to the github (Yay! Open Source!)

Other features
		-Command auto-completion for when you're too lazy to type out the whole command
		-Build-a-Wumpus
		""".format(p=prefix))
		return

	#Pong!    
	if cmd == "ping":
		await client.send_message(message.channel, "Pong!")
		return

	#Displays the developers names
	if cmd == "blacksmiths":
		await client.send_message(message.channel, "This is a bot that was written for Discord Hack Week.\nThe development team is <@388777079455612929>, <@140611354317815808> and Wumpus")
		return
	
	#Shows the bot statistics
	if cmd == "botstats":
		#Get the statistics
		users = len([x for x in list(dict.fromkeys(list(client.get_all_members()))) if str(x.status) != "offline"])
		servers = len(client.servers)

		#Send them in an embed so it looks cool
		embed = discord.Embed(title="Bot Statistics", description="Bot Version - Alpha\nGaming with {} discordians in {} servers".format(users,servers), color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
		return
	
	#Share a link to the github
	if cmd == "code":
		await client.send_message(message.channel, "https://github.com/Fraserbc/Wumpus_Bot")
		return

	"""channel = client.get_channel("592734071982129153")
	
	await client.send_file(channel, "wumpus_heart.png")

	e = discord.Embed()
	e.title = "Abcd"

	await client.send_message(channel, embed=e)"""
	return

#Update status every 10 seconds
async def update_status():
	while True:
		#How many users are online (removes duplicates)
		users = len([x for x in list(dict.fromkeys(list(client.get_all_members()))) if str(x.status) != "offline"])

		#Change the status
		await client.change_presence(game=discord.Game(name='Games with {} discordians'.format(users)))
		
		#Sleep so I don't DOS the API
		await sleep(10)

#Start the bot
client.run(token)