#Import the database handler
import db_handler

commands = [
	"botstats",
	"stop",
	"help",
	"blacksmiths",
	"ping",
	"code",
	"prefix",
	"profile"
]

#Initialize the prefixes from the sql database
def update_prefixes():
	global prefixes
	prefixes = db_handler.get_prefixes()

#Write the prefixes to the db
def write_prefixes():
	db_handler.set_prefixes(prefixes)

#Command autocompletion
def autocomplete(command):
	#Autocomplete command
	matches = []
	for cmd in commands:
		if cmd.startswith(command):
			matches.append(cmd)
	
	return matches

#Check the matches and return them as json
def check_matches(command, prefix):	
	#Remove the prefix and split args
	command = command.replace(prefix, "", 1).split(" ")
	args = command[1:]
	command = command[0]
	#Autocomplete the command if neccessary
	matches = autocomplete(command)
	
	#If there are no matches it is not a valid command
	if len(matches) == 0:
		return {"status":0,"matches":None,"prefix":prefix,"args":[]}
	
	#If there are more than one matches suggest then  to the user
	if len(matches) > 1:
		return {"status":2,"matches":matches,"prefix":prefix,"args":[]}
		
	#If there is only one match then that must be the answer
	return {"status":1,"matches":matches,"prefix":prefix,"args":args}

#Test and autocomplete the command
def test_command(command, server):
	#Test if it is actaully a server and not a dm
	if server == None:
		if command.startswith(prefixes["default"]):
			return check_matches(command, prefixes["default"])
		
		#The prefix doesn't match
		return {"status":4,"matches":None,"prefix":None,"args":[]}
	
	#It is a server so check if the prefix exists just to be sure
	elif server.id in prefixes:
		#Checks the command matches the prefix
		if command.startswith(prefixes[server.id]):
			prefix = prefixes[server.id]
			return check_matches(command, prefix)
		
		#It doesn't start with the prefix
		return {"status":4,"matches":None,"prefix":None,"args":[]}
	
	#No prefix was found, something broke help
	print(prefixes)
	return {"status":-1,"matches":None,"prefix":None,"args":[]}