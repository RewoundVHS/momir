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
 
random_card = momir.random_card_by_mana_value(input("Mana Value: "))
found_card = momir.fetch_card_data(random_card)
 
if found_card == 'Error':
    print('Error, card not found')
    quit()
else:
    for i, face in enumerate(found_card):
        # Print the card data
        print("Name:", face['name'])
        print("Mana Cost:", face['mana_cost'])
        print("Type Line:", face['type_line'])
        print("Oracle Text:", face['oracle_text'])
        print("Power/Toughness:", face['power_toughness'])
        print("Art URL:", face['art'])
     
        print("Downloading art...")
        response = get(face['art'])
        with open(f"art_{i}.png", 'wb') as f:
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
    for i, face in enumerate(found_card):
        # Fit text sizes 
        name_size = fit_text_width(face["name"], FONT_NAME, 48, 28, NAME_MAX_WIDTH)
        type_size = fit_text_width(face["type_line"], FONT_TYPE, 36, 20, TEXT_WIDTH)
        oracle_size = fit_text_height(face["oracle_text"], FONT_RULES, 30, 12, TEXT_WIDTH, ORACLE_HEIGHT)
     
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
            "-annotate", "+60+10", face["name"],
            "card.png"
        ], check=True)

        # Add mana cost
        subprocess.run([
            "convert", "card.png",
            "-font", FONT_NAME,
            "-pointsize", "36",
            "-gravity", "NorthEast",
            "-annotate", "+60+10", face["mana_cost"],
            "card.png"
        ], check=True)
     
        # Crop art 
        subprocess.run([
            "convert", f"art_{i}.png",
            "-resize", f"{ART_WIDTH}x{ART_HEIGHT}^",
            "-gravity", "center",
            "-extent", f"{ART_WIDTH}x{ART_HEIGHT}",
            f"art_cropped_{i}.png"
        ], check=True)

        # Add art 
        subprocess.run([
            "convert", "card.png",
            f"art_cropped_{i}.png",
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
            "-annotate", "+60+560", face["type_line"],
            "card.png"
        ], check=True)

        # Render oracle text
        subprocess.run([
            "convert",
            "-size", f"{TEXT_WIDTH}x",
            "-font", FONT_RULES,
            "-pointsize", str(oracle_size),
            "-background", "white",
            f"caption:{face['oracle_text']}",
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
            "-annotate", "+60+80", face["power_toughness"],
            f"output_{i}.png"
        ], check=True)
     
        print(f"Generated: output_{i}.png")
 
if __name__ == "__main__":
    main()
