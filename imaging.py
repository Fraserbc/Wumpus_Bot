from PIL import Image

def wumpus_pfp():
	background = Image.open("wumpus.png")
	foreground = Image.open("test2.png")

	Image.alpha_composite(background, foreground).save("test3.png")