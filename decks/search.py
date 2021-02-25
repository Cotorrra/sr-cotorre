import requests

from decks.deck import check_upgrade_rules
from decks.formating import format_upgraded_deck


def find_deck(code: str):
    link = 'https://es.arkhamdb.com/api/public/deck/%s' % code
    req = requests.get(link)
    if req.url != link:
        link = 'https://es.arkhamdb.com/api/public/decklist/%s' % code
        req = requests.get(link)
        if req.url != link:
            req = False
    return req.json()


def find_former_deck(code: str):
    curr_deck = find_deck(code)
    if curr_deck:
        former_code = str(curr_deck["previous_deck"])
        former_deck = find_deck(former_code)
        if former_deck:
            return former_deck
        else:
            return False
    return False


def search_for_upgrades(query, cards):
    if len(query) >= 2:
        deck1 = find_deck(query[0])
        deck2 = find_deck(query[1])
        if not deck1 or deck2:
            response = "No encontre uno de los mazos."
            embed = False
        else:
            info = check_upgrade_rules(deck1, deck2, cards)
            response = "¡Encontré una Mejora!"
            embed = format_upgraded_deck(deck1, info)

    elif len(query) == 1:
        deck1 = find_deck(query[0])
        deck2 = find_former_deck(query[0])
        if not deck1:
            response = "No encontré el mazo."
            embed = False
        elif not deck2:
            response = "El Mazo dado no contiene una mejora."
            embed = False
        else:
            info = check_upgrade_rules(deck2, deck1, cards)
            response = "¡Encontré una Mejora!"
            embed = format_upgraded_deck(deck1, info)

    else:
        response = "Uso de !ahu [numero] [numero] o bien !ahu [numero]"
        embed = False

    return response, embed
