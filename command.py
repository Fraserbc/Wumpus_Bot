#Import the database handler
import db_handler

"""prefixs = {
	"default":"w!",
	"592734071482744855":"w!",
	"571045813443362826":"w!"
}"""

commands = [
	"botstats",
	"stop",
	"help",
	"blacksmiths",
	"ping",
	"code"
]

#Initialize the prefixs from the sql database
prefixs = {}
def update_prefixs():
	global prefixs
	prefixs = db_handler.get_prefixs()
	prefixs["default"] = "w!"

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
		if command.startswith(prefixs["default"]):
			return check_matches(command, prefixs["default"])
		
		#The prefix doesn't match
		return {"status":4,"matches":None,"prefix":None,"args":[]}
	
	#It is a server so check if the prefix exists just to be sure
	elif server.id in prefixs:
		#Checks the command matches the prefix
		if command.startswith(prefixs[server.id]):
			prefix = prefixs[server.id]
			return check_matches(command, prefix)
		
		#It doesn't start with the prefix
		return {"status":4,"matches":None,"prefix":None,"args":[]}
	
	#No prefix was found, something broke help
	print(prefixs)
	return {"status":-1,"matches":None,"prefix":None,"args":[]}