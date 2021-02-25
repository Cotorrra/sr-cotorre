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
