import re
import unidecode


def card_search(query, cards, keyword_func):
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    f_cards = sorted(cards.copy(), key=lambda card: card['name'])

    if sub_text_mode:
        f_cards = [c for c in f_cards if filter_by_subtext(c, sub_query)]

    if keyword_mode:
        f_cards = keyword_func(f_cards, keyword_query)

    r_cards = search(query, f_cards)

    if len(r_cards) == 0 or len(r_cards) == len(f_cards):
        return []
    else:
        return r_cards


def search(query: str, cards: list):
    """
    Realiza una búsqueda según un grupo de palabras dentro del nombre (atributo 'name') de cada carta.
    :param query: Texto para buscar
    :param cards: Cartas
    :return:
    """
    r_cards = sorted(cards, key=lambda card: -hits_in_string(card['name'], query))

    # Sales en los resultados aparte si estas igual de hits con las palabras
    r_cards = [c for c in r_cards if hits_in_string(c['name'], query) == hits_in_string(r_cards[0]['name'], query)]
    return r_cards


def find_by_id(code: str, cards: list):
    """
    Retorna la carta que haga match con el id entregado, de otra forma devuelve False.
    :param code:
    :param cards:
    :return:
    """
    r_cards = [c for c in cards if c['code'] == code]
    try:
        return r_cards[0]
    except IndexError:
        return False


def use_pc_keywords(cards: list, key_list: str):
    """
    Filtra cartas de jugador según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c['exceptional']]
        if char == "b":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'seeker']
        if char == "g":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'guardian']
        if char == "r":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'rogue']
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'survivor']
        if char == "m":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'mystic']
        if char == "n":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'neutral']
        if char == "u":
            filtered_cards = [c for c in filtered_cards if c['unique']]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['permanent']]
        # TODO: c = carta característica. La mayoría de estas tiene "Solo para mazo de ..."
        if char == "c":
            filtered_cards = [c for c in filtered_cards if "Sólo para el mazo de" in c['text']]

    return filtered_cards


def use_ec_keywords(cards: list, key_list: str):
    """
    Filtra cartas de encuentro según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "enemy"]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "act"]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "agenda"]
        if char == "t":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "treachery"]
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "scenario"]
        if char == "l":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "location"]
        if char == "j":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'neutral']
    return filtered_cards


def is_lvl(card: dict, lvl: int):
    """
    Equipara el nivel de una carta con el numero dado, si no tiene nivel, se equipara con 0.
    :param card: carta
    :param lvl: nivel
    :return:
    """
    if 'xp' in card:
        return card['xp'] == lvl
    else:
        return 0 == lvl


def filter_by_subtext(card: dict, sub: str):
    """
    Retorna True si la carta contiene el subsombre dado, de otra forma False.
    :param card:
    :param sub:
    :return:
    """
    if "subname" in card:
        return hits_in_string(card['subname'], sub) > 0
    else:
        return False


def filter_by_subtext_ec(card: dict, sub: str):
    """
    Retorna True si la carta contiene el subnombre dado (incluído la parte de atras), de otra forma False.
    :param card:
    :param sub:
    :return:
    """
    if "subname" in card:
        return hits_in_string(card['subname'], sub) > 0
    else:
        return False


def find_and_extract(string: str, start_s: str, end_s: str):
    """
    Encuentra y extrae un substring delimitado por start_s y end_s, regresando una triada de valores:
    (string base, string extraido, si fue extraido algo)
    :param string:
    :param start_s:
    :param end_s:
    :return:
    """
    if start_s == end_s:
        enable = string.find(start_s) > 0
    else:
        enable = string.__contains__(start_s) and string.__contains__(end_s)
    fst_occ = string.find(start_s) + 1
    snd_occ = string[fst_occ:].find(end_s)
    extract = string[fst_occ: fst_occ + snd_occ]
    base = string.replace(" %s%s%s" % (start_s, extract, end_s), "", 1)
    return base, extract, enable


def hits_in_string(s1: str, s2: str):
    """
    Retorna la cantidad de veces únicas en las que un string contiene una palabra en el otro.
    :param s1:
    :param s2:
    :return:
    """
    hits = 0
    for w1 in list(set(s1.lower().split())):
        for w2 in list(set(s2.lower().split())):
            w1_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w1))
            w2_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w2))
            if w1_c == w2_c:
                hits += 1
    return hits


def get_qty(deck, card_id):
    for c_id, qty in deck['slots'].items():
        if c_id == card_id:
            return qty
    return 0


def has_trait(card, trait):
    try:
        traits = card['real_traits'].lower().split()
        return "%s." % trait in traits

    except KeyError:
        return False


def color_picker(c):
    colors = {
        "survivor": 0xcc3038,
        "rogue": 0x107116,
        "guardian": 0x2b80c5,
        "mystic": 0x4331b9,
        "seeker": 0xec8426,
        "neutral": 0x606060,
        "mythos": 0x000000,
    }
    return colors[c['faction_code']]


def get_color_by_investigator(deck, cards):
    inv_id = deck['investigator_code']
    inv_card = find_by_id(inv_id, cards)
    return color_picker(inv_card)
