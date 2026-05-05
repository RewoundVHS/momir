#! /usr/bin/python3

from requests import get
from json import loads

# Query Scryfall for a random creature of the specified mana value
# Limit these creatures to only those that are legal in Vintage to avoid 
# stickers, attractions and culturally insensitive cards
# This query also excludes double-faced creatures
def fetch_card_data(mana_value):
    card = loads(get(f"https://api.scryfall.com/cards/random?q=t%3Acreature%20-is%3A:double-faced%20legal%3Avintage%20mv%3A{mana_value}").text)

    remove_braces = str.maketrans('', '', '{}')

    if card['object'] == 'error':
        return 'Error'
    else:
        # Compile the list of relevant card data
        card_data = {
            'name': card['name'], 
            'mana_cost': card['mana_cost'].translate(remove_braces), 
            'type_line': card['type_line'], 
            'oracle_text': card['oracle_text'], 
            'power_toughness': card['power'] + '/' + card['toughness'], 
            'art': card['image_uris']['art_crop']
        }
    return card_data
