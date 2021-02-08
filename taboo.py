import json
from formating.formating import *

current_taboo = "003"


def load_taboo():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('data/taboos.json') as taboo:
        info = list(json.load(taboo))

    for t in info:
        t['cards'] = json.dumps(t['cards'])
        t['cards'] = json.loads(t['cards'])

    return info


def get_taboo_info(version=current_taboo):
    """
    Obtiene la version de taboo, si no se da argumento, devuelve la mas reciente.
    :param version:
    :return:
    """
    for info in taboo_info:
        if info['code'] == version:
            return info['cards']
    return []


def is_in_taboo(card_id, version=current_taboo):
    """
    Devuelve True si la carta esta en la lista de tabues dada (o en la actual si solo se dio la carta)
    :param card_id:
    :param version:
    :return:
    """
    tabooed_cards = get_taboo_info(version)
    for card in tabooed_cards:
        if card['code'] == card_id:
            return True
    return False


def get_tabooed_card(card_id, version=current_taboo):
    """
    Devuelve la informacion de la carta dada en la informacion de tabú actual o dada.
    :param card_id:
    :param version:
    :return:
    """
    tabooed_cards = get_taboo_info(version)
    for card in tabooed_cards:
        if card['code'] == card_id:
            return card
    return {}


taboo_info = load_taboo()
