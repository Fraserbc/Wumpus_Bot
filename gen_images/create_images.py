from PIL import Image

wumpus = [
	"blackwumpus.png",
	"brownwumpus.png",
	"polarwumpus.png"
]

extras = [
	"discordheadband.png",
	"pipewumpus.png",
	"wumpusbandana.png",
	"wumpusmonocole.png",
	"wumpusmoustache.png"
]

badges = [
	"wumphackweek.png",
	"wumplgbt.png",
	"wumpdev.png"
]

i = 0
for wump in wumpus:
	for badge in badges:
		for extra in extras:
			wump_im = Image.open(wump).convert("RGBA")
			badge_im = Image.open(badge).convert("RGBA")
			extra_im = Image.open(extra).convert("RGBA")

			wump_im.paste(extra_im, (0, 0), extra_im)
			wump_im.paste(badge_im, (0, 0), badge_im)
			wump_im.save("../Images/{}.png".format(i))
			i += 1