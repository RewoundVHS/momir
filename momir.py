#! /usr/bin/python3

from requests import get
from json import loads

# Query Scryfall for a random creature of the specified mana value
# Limit these creatures to only those that are legal in Vintage to avoid 
# stickers, attractions and culturally insensitive cards
def fetch_card_data(mana_value):
	card = loads(get(fr"https://api.scryfall.com/cards/random?q=t%3A%2F^[^\%2F]*Creature%2F%20legal%3Avintage%20mv%3A{mana_value}").text)

	remove_braces = str.maketrans('', '', '{}')

	if card['object'] == 'error':
		return 'Error'
    # Handle double faced cards
	elif 'card_faces' in card:
		card_data = {
			'name': card['card_faces'][0]['name'], 
			'mana_cost': card['card_faces'][0]['mana_cost'].translate(remove_braces), 
			'type_line': card['card_faces'][0]['type_line'], 
			'oracle_text': card['card_faces'][0]['oracle_text'], 
			'power_toughness': card['card_faces'][0]['power'] + '/' 
				+ card['card_faces'][0]['toughness'] 
				if 'Creature' in card['card_faces'][0]['type_line'] else '', 
			'art': card['card_faces'][0]['image_uris']['art_crop'], 
		}
	else:
		# Compile the list of relevant card data
		card_data = {
			'name': card['name'], 
			'mana_cost': card['mana_cost'].translate(remove_braces), 
			'type_line': card['type_line'], 
			'oracle_text': card['oracle_text'], 
			'power_toughness': card['power'] + '/' + card['toughness'] 
				if 'Creature' in card['type_line'] else '', 
			'art': card['image_uris']['art_crop']
		}
	return card_data
