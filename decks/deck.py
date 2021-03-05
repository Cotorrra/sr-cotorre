from core.search import find_by_id
from core.utils import has_trait, get_qty
from p_cards.utils import get_color_by_investigator
from taboo.taboo import *


def diff_decks(a_deck1, a_deck2):
    """
    Regresa una tupla con las diferencias entre dos mazos: La primera contiene las id de cartas que salieron y el otro
    contiene el id con las cartas que entraron.
    :param a_deck1:
    :param a_deck2:
    :return:
    """

    d_out = a_deck1.copy()
    d_in = a_deck2.copy()
    for c in a_deck1:
        if c in d_in:
            d_out.remove(c)
            d_in.remove(c)
    return d_out, d_in


def deck_to_array(deck, cards):
    arr_deck = []
    for c_id, qty in deck['slots'].items():
        for i in range(qty):
            arr_deck.append(find_by_id(c_id, cards))
    return arr_deck


def check_upgrade_rules(deck1, deck2, cards):
    # Getting versatile reduces the cost of the cards of lvl 0
    info = {"buys_in": [], "buys_out": [],
            "xp_diff": 0, "color": get_color_by_investigator(deck1, cards)}
    taboo = "00" + str(deck1['taboo_id'])
    a_deck1 = deck_to_array(deck1, cards)
    a_deck2 = deck_to_array(deck2, cards)
    [diff_out, diff_in] = diff_decks(a_deck1, a_deck2)

    arcane_inv_used = False
    adaptable_uses = 0
    inv_meta = json.loads(deck1['meta'])
    parallel_upg = False
    if "alternative_back" in inv_meta:
        parallel_upg = True

    while diff_in:
        # Mejora
        c_in = pick_card(diff_in, diff_out)
        if find_lower_lvl_card(c_in, diff_out):
            c_out = find_lower_lvl_card(c_in, diff_out)
            xp_diff = max(calculate_xp(c_in, 1, taboo) - calculate_xp(c_out, 1, taboo),
                          calculate_xp(c_out, 1, taboo))
            if has_trait(c_out, "spell") and get_qty(deck1, "04109") > 0 and not arcane_inv_used:
                # 04109 es Investigación Arcana
                xp_diff = max(xp_diff - get_qty(deck1, "04109"), 0)
                arcane_inv_used = True

            move_card_in_array(info["buys_in"], diff_in, c_in)
            move_card_in_array(info["buys_out"], diff_out, c_out)
            info['xp_diff'] += xp_diff

        # Adaptable
        elif (c_in["xp"] if "xp" in c_in else -1) == 0:
            if get_qty(deck1, "02110") * 2 > adaptable_uses:
                c_out = get_lvl_zero_card(diff_out)
                move_card_in_array(info["buys_in"], diff_in, c_in)
                move_card_in_array(info["buys_out"], diff_out, c_out)
                adaptable_uses += 1
            else:
                move_card_in_array(info["buys_in"], diff_in, c_in)
                info['xp_diff'] += max(calculate_xp(c_in, 1, taboo), 1)

        # Mejora Paralela
        elif parallel_upg and find_lower_lvl_card(c_in, deck1):
            lower_card = find_lower_lvl_card(c_in, deck1)
            p_upg_traits = []
            if deck1['investigator_name'] == "\"Skids\" O'Toole":
                p_upg_traits = ["fortune", "gambit"]
            if deck1['investigator_name'] == "Agnes Baker":
                p_upg_traits = ["spell"]
            for t in p_upg_traits:
                if has_trait(lower_card, t):
                    move_card_in_array(info["buys_in"], diff_in, c_in)
                    info["xp_diff"] += calculate_xp(c_in, 1, taboo)
        # Compras
        else:
            move_card_in_array(info["buys_in"], diff_in, c_in)
            info['xp_diff'] += calculate_xp(c_in, 1, taboo)

    while diff_out:
        c_out = diff_out[0]
        move_card_in_array(info["buys_out"], diff_out, c_out)

    return info


def find_lower_lvl_card(card, a_deck):
    for c in a_deck:
        if c['real_name'] == card['real_name'] and 'xp' in c and 'xp' in card:
            if c['xp'] < card['xp']:
                return c
    return {}


def get_lvl_zero_card(a_deck):
    for c in a_deck:
        if (c["xp"] if "xp" in c else -1) == 0:
            return c
    return {}


def move_card_in_array(a_in, a_out, c_in):
    if c_in['myriad']:
        while c_in in a_out:
            a_out.remove(c_in)
            a_in.append(c_in)
    else:
        a_out.remove(c_in)
        a_in.append(c_in)


def pick_card(pool, pool2):
    for c in pool:
        if find_lower_lvl_card(c, pool2):
            return c
    return pool[0]

