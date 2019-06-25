prefixs = {
	"default":"w!",
	"592734071482744855":"w!"
}

commands = [
	"abcd",
	"stop",
	"help",
	"blacksmiths"
]

def test_command(command, server):
	#Test if it is actaully a server and not a dm
	if server == None:
		command = command.replace(prefixs["default"], "", 1)
		return {"status":1,"matches":[command],"prefix":None,"args":[]}
	#It is a server so check if the prefix exists just to be sure
	elif server in prefixs:
		#Checks the command matches the prefix
		if command.startswith(prefixs[server]):
			#Store the prefix for later use
			prefix = prefixs[server]
			
			#Remove the prefix and split args
			command = command.replace(prefix, "", 1).split(" ")
			args = command[1:]
			command = command[0]

			#Autocomplete command
			matches = []
			for cmd in commands:
				if cmd.startswith(command):
					matches.append(cmd)
			
			#If there are no matches it is not a valid command
			if len(matches) == 0:
				return {"status":0,"matches":None,"prefix":prefix,"args":[]}
			
			#If there are more than one matches suggest then  to the user
			if len(matches) > 1:
				return {"status":2,"matches":matches,"prefix":prefix,"args":[]}
			
			#If there is only one match then that must be the answer
			return {"status":1,"matches":matches,"prefix":prefix,"args":args}
		
		#It doesn't start with the prefix
		return {"status":4,"matches":None,"prefix":None,"args":[]}
	
	#No prefix was found, something broke help
	return {"status":-1,"matches":None,"prefix":None,"args":[]}