#!/usr/bin/env python3
 
import momir
import subprocess
from requests import get
 
CARD_WIDTH = 744
CARD_HEIGHT = 1040
ART_WIDTH = 624
ART_HEIGHT = 468
TEXT_WIDTH = 624
ORACLE_HEIGHT = 315
NAME_MAX_WIDTH = 500
 
FONT_NAME = "Ubuntu-Sans-Regular"
FONT_TYPE = "Ubuntu-Sans-Regular"
FONT_RULES = "Ubuntu-Sans-Regular"
 
foundCard = momir.fetch_card_data(input("Mana Value: "))
 
if foundCard == 'Error':
	print('Error, card not found')
else:
	# Print the card data
	print("Name:", foundCard['name'])
	print("Mana Cost:", foundCard['mana_cost'])
	print("Type Line:", foundCard['type_line'])
	print("Oracle Text:", foundCard['oracle_text'])
	print("Power/Toughness:", foundCard['power_toughness'])
	print("Art URL:", foundCard['art'])
 
	print("Downloading art...")
	response = get(foundCard['art'])
	with open('art.png', 'wb') as f:
		f.write(response.content)
 
def run(cmd):
	return subprocess.check_output(cmd).decode().strip()

# Attempt to fit the text within the specified width
def fit_text_width(text, font, max_size, min_size, max_width):
	for size in range(max_size, min_size - 1, -1):
		w = run([
			"convert",
			"-font", font,
			"-pointsize", str(size),
			f"label:{text}",
			"-format", "%w",
			"info:"
		])
		if int(w) <= max_width:
			return size
	return min_size
 
# Attempt to fit the text within the specified height
def fit_text_height(text, font, max_size, min_size, width, height):
	for size in range(max_size, min_size - 1, -1):
		h = run([
			"convert",
			"-size", f"{width}x",
			"-font", font,
			"-pointsize", str(size),
			f"caption:{text}",
			"-format", "%h",
			"info:"
		])
		if int(h) <= height:
			return size
	return min_size
 
def main():
	# Fit text sizes 
	name_size = fit_text_width(foundCard["name"], FONT_NAME, 48, 28, NAME_MAX_WIDTH)
	type_size = fit_text_width(foundCard["type_line"], FONT_TYPE, 36, 20, TEXT_WIDTH)
	oracle_size = fit_text_height(foundCard["oracle_text"], FONT_RULES, 30, 12, TEXT_WIDTH, ORACLE_HEIGHT)
 
	# Create base 
	subprocess.run([
		"convert",
		"-size", f"{CARD_WIDTH}x{CARD_HEIGHT}",
		"xc:white",
		"card.png"
	], check=True)

	# Add name 
	subprocess.run([
		"convert", "card.png",
		"-font", FONT_NAME,
		"-pointsize", str(name_size),
		"-gravity", "NorthWest",
		"-annotate", "+60+10", foundCard["name"],
		"card.png"
	], check=True)

	# Add mana cost
	subprocess.run([
		"convert", "card.png",
		"-font", FONT_NAME,
		"-pointsize", "36",
		"-gravity", "NorthEast",
		"-annotate", "+60+10", foundCard["mana_cost"],
		"card.png"
	], check=True)
 
	# Crop art 
	subprocess.run([
		"convert", "art.png",
		"-resize", f"{ART_WIDTH}x{ART_HEIGHT}^",
		"-gravity", "center",
		"-extent", f"{ART_WIDTH}x{ART_HEIGHT}",
		"art_cropped.png"
	], check=True)

	# Add art 
	subprocess.run([
		"convert", "card.png",
		"art_cropped.png",
		"-geometry", "+60+80",
		"-composite",
		"card.png"
	], check=True)
 
	# Add type line 
	subprocess.run([
		"convert", "card.png",
		"-font", FONT_TYPE,
		"-pointsize", str(type_size),
		"-gravity", "NorthWest",
		"-annotate", "+60+560", foundCard["type_line"],
		"card.png"
	], check=True)

	# Render oracle text
	subprocess.run([
		"convert",
		"-size", f"{TEXT_WIDTH}x",
		"-font", FONT_RULES,
		"-pointsize", str(oracle_size),
		"-background", "white",
		f"caption:{foundCard['oracle_text']}",
		"-gravity", "NorthWest",
		"-extent", f"{TEXT_WIDTH}x{ORACLE_HEIGHT}",
		"oracle.png"
	], check=True)

	# Add oracle text 
	subprocess.run([
		"convert", "card.png",
		"oracle.png",
		"-geometry", "+60+610",
		"-composite",
		"card.png"
	], check=True)
 
	# Add power/toughness 
	subprocess.run([
		"convert", "card.png",
		"-font", FONT_NAME,
		"-pointsize", "36",
		"-gravity", "SouthEast",
		"-annotate", "+60+80", foundCard["power_toughness"],
		"output.png"
	], check=True)
 
	print("Generated: output.png")
 
if __name__ == "__main__":
	main()
