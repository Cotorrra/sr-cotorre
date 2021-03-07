import re
import unidecode


def card_search(query, cards, keyword_func):
    """
    Busca una carta en un conjunto de cartas usando keywords (ej (4E))
    :param query: Nombre de la carta a buscar
    :param cards: Conjunto de cartas
    :param keyword_func: Función para utilizar keywords
    :return:
    """
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    f_cards = cards.copy()

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
    r_cards = sorted(cards, key=lambda card: -hits_in_string(query, card['name']))

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


def hits_in_string(query: str, find: str):
    """
    Retorna la cantidad de veces únicas en las que un string contiene una palabra en el otro.
    Va por palabras.6,mnbvcxz<
    :param s1:
    :param s2:
    :return:
    """
    hits = 0
    set1 = query.lower().split()
    set2 = find.lower().split()
    hit_list = []
    for w1 in set1:
        for w2 in set2:
            w1_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w1))
            w2_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w2))
            if w1_c == w2_c and w1_c not in hit_list:
                hits += 1
                hit_list.append(w1_c)
                if set1.index(w1) == set2.index(w2):
                    hits += 1
    return hits


