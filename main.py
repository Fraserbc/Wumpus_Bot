#Needed imports
import discord, sys, json
from asyncio import sleep

#import the command auto complete and test
import command

#Build-a-Wumpus/profiles library
import baw

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
	print("Started custom status!")

	#get the prefixes from the db
	command.update_prefixes()

	#Update the sql db with all the prefixes from the json
	client.loop.create_task(update_db())
	print("Started DB updater!")

#Dealign with commands
@client.event
async def on_message(message):
	#Ingore any messages from bots
	if (message.author.bot):
		return

	#Test and autocomplete the command
	cmd = command.test_command(message.content, message.server)

	#It doesn't start with the prefix ignore it
	if cmd["status"] == 4:
		return

	#If the status was 0 (not a valid command or it doesn't start with the prefix)
	if cmd["status"] == 0:
		desc = "That wasn't a valid command! Use {}help for a list of commands!".format(cmd["prefix"])
		embed = discord.Embed(title="Invalid Command", description=desc, color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
		return
	
	#If there are multiple matches suggest them to the user
	if cmd["status"] == 2:
		desc = '\n    {}'.format( cmd["prefix"] ).join( [""] + cmd["matches"] )
		embed = discord.Embed(title="Did you mean", description=desc, color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
		return
	
	#If something broken
	if cmd["status"] == -1:
		desc = "Well... this is awkward. Something broke and will be fixed soon. Try again in a few minutes."
		embed = discord.Embed(title="Wumpus tripped over a wire", description=desc, color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
		return
	
	#If all the checks passed then get the command and arguments
	args = cmd["args"]
	prefix = cmd["prefix"]
	cmd = cmd["matches"][0]

	#Stop the bot
	if cmd == "stop":
		#Write the prefixes so the prefix is saved
		command.write_prefixes()
		sys.exit()
	
	#Show the help/usage message
	if cmd == "help":
		desc =  """
			{p}botstats - Shows statistics about the bot
			{p}help - Shows this help message
			{p}blacksmiths - Lists the development team
			{p}ping - Pong!
			{p}code - Link to the github (Yay! Open Source!)
			{p}prefix [New Prefix] - Set the prefix for the server

		Other features
			-Command auto-completion for when you're too lazy to type out the whole command
			-Build-a-Wumpus
		""".format(p=prefix)

		#Embeds look nice
		embed = discord.Embed(title="Wumpus Bot Help", description=desc, color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
		return

	#Pong!    
	if cmd == "ping":
		await client.send_message(message.channel, "Pong! {}".format(' '.join(args)))
		return

	#Displays the developers names
	if cmd == "blacksmiths":
		desc = "This is a bot that was written for Discord Hack Week.\nThe development team is <@388777079455612929>, <@140611354317815808> and, of course, Wumpus"
		embed = discord.Embed(title="Blacksmiths", description=desc, color=0x972ed9)
		await client.send_message(message.channel, embed=embed)
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

	#Show the users profile
	if cmd == "profile":
		return
	
	#Share a link to the github
	if cmd == "code":
		await client.send_message(message.channel, "https://github.com/Fraserbc/Wumpus_Bot")
		return
	
	#Set the prefix command
	if cmd == "prefix":
		#Check they have the correct permissions
		if message.server == None or not message.author.server_permissions.administrator:
			embed = discord.Embed(title="Permission Denied", description="You need to have administrator permissions in this server to change the prefix!", color=0x972ed9)
			await client.send_message(message.channel, embed=embed)
			return
		
		#They have permission so set the prefix so check if they supplied an argument
		if len(args) == 0:
			embed = discord.Embed(title="No Arguments Supplied", description="You need to supply an argument!\nCheck {}help for the syntax".format(prefix), color=0x972ed9)
			await client.send_message(message.channel, embed=embed)
			return
		
		#Set the prefix
		command.prefixes[message.server.id] = args[0]
		embed = discord.Embed(title="Prefix Changed", description="You have successfully changed the prefix to {}".format(args[0]), color=0x972ed9)
		await client.send_message(message.channel, embed=embed)

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

#Update the db every 5 mins
async def update_db():
	while True:
		#Update the prefixes
		command.write_prefixes()

		#Wait for 5 mins
		await sleep(60*5)		

#Start the bot
client.run(token)