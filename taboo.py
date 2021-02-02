import json
from formating import *

current_taboo = "003"

def load_taboo():
    with open('data/taboos.json') as taboo:
        info = list(json.load(taboo))

    for t in info:
        t['cards'] = json.loads(t['cards'])

    return info


def get_taboo_info(version=current_taboo):
    for info in taboo_info:
        if info['code'] == version:
            return info['cards']
    return []


def is_in_taboo(card_id, version=current_taboo):
    tabooed_cards = get_taboo_info(version)
    for card in tabooed_cards:
        if card['code'] == card_id:
            return True
    return False


def get_tabooed_card(card_id, version=current_taboo):
    tabooed_cards = get_taboo_info(version)
    for card in tabooed_cards:
        if card['code'] == card_id:
            return card
    return {}


taboo_info = load_taboo()
