#Needed imports
import discord, sys, json

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
    
    client.logout()

#Dealign with commands
@client.event
async def on_message(message):
    #Test and autocomplete the command
    cmd = command.test_command(message.content, message.server.id)

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
    
    #If all the checks passed then get the command
    cmd = cmd["matches"][0]

    #Stop the bot
    if cmd == "stop":
        sys.exit()
    
    """channel = client.get_channel("592734071982129153")
    
    await client.send_file(channel, "wumpus_heart.png")

    e = discord.Embed()
    e.title = "Abcd"

    await client.send_message(channel, embed=e)"""
    return

#Start the bot
client.run(token)