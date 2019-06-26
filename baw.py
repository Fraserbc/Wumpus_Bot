#Import the db handler for the profiles
import db_handler

#we need json here
import json

wumpus_to_image = {
    "brown":"Images/brownwumpus.png",
    "black":"Images/blackwumpus.png",
    "white":"Images/polarwumpus.png"
}

#Function for proccessign the profiles
def get_profile(id):
    #Get the data from the db
    profile = db_handler.get_profile(id)

    #Proccess the profile picture
    profile["pfp"] = json.loads(profile["pfp"])
    
    return wumpus_to_image[profile["pfp"]["wumpus"]]