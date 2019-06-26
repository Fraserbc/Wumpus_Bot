from PIL import Image

wumpus = [
	"black",
	"brown",
	"polar"
]

extras = [
	"head",
	"pipe",
	"ban",
	"mon",
	"mous"
]

badges = [
	"hack",
	"lgbt",
	"dev"
]

for wump in wumpus:
	for badge in badges:
		for extra in extras:
			wump_im = Image.open(wump+".png").convert("RGBA")
			badge_im = Image.open(badge+".png").convert("RGBA")
			extra_im = Image.open(extra+".png").convert("RGBA")

			wump_im.paste(extra_im, (0, 0), extra_im)
			wump_im.paste(badge_im, (0, 0), badge_im)
			wump_im.save("../Images/{}{}{}.png".format(wump, badge, extra))

for wump in wumpus:
	wump_im = Image.open(wump+".png").convert("RGBA")
	wump_im.save("../Images/{}NoneNone.png".format(wump))