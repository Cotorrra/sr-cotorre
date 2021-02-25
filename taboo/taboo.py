import json

from core.formating import format_text

current_taboo = "003"


def load_taboo():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('taboo/data/taboos.json') as taboo:
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


def calculate_xp(c, qty, taboo_ver=current_taboo):
    chain = 0
    if is_in_taboo(c['code'], taboo_ver):
        if 'xp' in get_tabooed_card(c['code'], taboo_ver):
            chain = get_tabooed_card(c['code'], taboo_ver)['xp']

    if "xp" in c:
        if c['myriad']:
            return c['xp'] + chain
        elif c['exceptional']:
            # Aunque debería haber 1 en el mazo...
            return (c['xp'] + chain) * 2 * qty
        else:
            return (c['xp'] + chain) * qty
    else:
        return chain * qty


def format_taboo_text(card_id, version=current_taboo):
    text = "Tabú más reciente: \n"
    if is_in_taboo(card_id, version):
        card = get_tabooed_card(card_id, version)
        if 'xp' in card:
            if card['xp'] >= 0:
                text += "> Encadenada: +%d de experiencia \n" % card['xp']
            else:
                text += "> Desencadenada: %d de experiencia \n" % card['xp']
        if 'text' in card:
            text += "> %s \n" % format_text(card['text'])
        return text
    else:
        return ""


taboo_info = load_taboo()

