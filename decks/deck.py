import requests
from utils import *
from taboo import *


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


def find_deck(code: str):
    link = 'https://es.arkhamdb.com/api/public/deck/%s' % code
    req = requests.get(link)
    if req.url != link:
        link = 'https://es.arkhamdb.com/api/public/decklist/%s' % code
        req = requests.get(link)
        if req.url != link:
            req = False
    return req.json()


def diff_decks(a_deck1, a_deck2):
    """
    Regresa una tupla con las diferencias entre dos mazos: La primera contiene las id de cartas que salieron y el otro
    contiene el id con las cartas que entraron.
    :param a_deck1:
    :param a_deck2:
    :return:
    """
    diff_deck = []
    d1 = a_deck1.copy()
    d2 = a_deck2.copy()
    for c in d1:
        if c not in d2:
            diff_deck.append(c)
        else:
            d2.remove(c)
    return diff_deck, d2


def deck_to_array(deck):
    arr_deck = []
    for c_id, qty in deck['slots'].items():
        for i in range(qty):
            arr_deck.append(c_id)
    return arr_deck


def check_upgrade_rules(deck1, deck2, cards):
    info = {"upgrades_out": [], "upgrades_in": [],
            "buys_in": [], "buys_out": [],
            "parallel_buy": [],
            "arcane_upg_in": [], "arcane_upg_out": [],
            "adaptable_in": [], "adaptable_out": [],
            "xp_diff": 0}
    taboo = "00" + str(deck1['taboo_id'])
    a_deck1 = deck_to_array(deck1)
    a_deck2 = deck_to_array(deck2)
    diffs = diff_decks(a_deck1, a_deck2)
    arcane_inv_used = False
    adaptable_uses = 0
    inv_meta = json.loads(deck1['meta'])
    parallel_upg = False
    if "alternative_back" in inv_meta:
        parallel_upg = True

    for c2 in diffs[1]:
        done_with_c2 = False
        real_c2 = find_by_id(c2, cards)
        if real_c2:
            name2 = real_c2['real_name']
            for c1 in diffs[0]:
                real_c1 = find_by_id(c1, cards)
                name1 = real_c1['real_name']
                if name1 == name2:
                    done_with_c2 = True
                    xp_diff = max(calculate_xp(real_c2, 1, taboo) - calculate_xp(real_c1, 1, taboo),
                                  calculate_xp(real_c1, 1, taboo))
                    if has_trait(real_c1, "spell") and get_qty(deck1, "04109") > 0 and not arcane_inv_used:
                        # 04109 es Investigación Arcana
                        xp_diff = max(xp_diff - get_qty(deck1, "04109"), 0)
                        arcane_inv_used = True
                        info["arcane_upg_in"].append(real_c2)
                        info["arcane_upg_out"].append(real_c1)
                        diffs[0].remove(c1)
                    else:
                        info["buys_in"].append(real_c2)
                        info["buys_out"].append(real_c1)
                        diffs[0].remove(c1)

                    info["xp_diff"] += xp_diff
                    break

            # "Parallel" upgrade
            if not done_with_c2:
                c2_lvl = real_c2['xp'] if "xp" in real_c2 else 0
                p_upgrade = find_lower_lvl_copy_in_deck(real_c2['real_name'], deck1, cards, c2_lvl)
                if parallel_upg and p_upgrade:
                    # TODO: Aqui se agregan los que vengan a futuro
                    lower_card = find_by_id(p_upgrade, cards)
                    p_upg_traits = []
                    if deck1['investigator_name'] == "\"Skids\" O'Toole":
                        p_upg_traits = ["fortune", "gambit"]
                    if deck1['investigator_name'] == "Agnes Baker":
                        p_upg_traits = ["spell"]
                    for t in p_upg_traits:
                        if has_trait(lower_card, t):
                            info["parallel_buy"].append(real_c2)
                            info["xp_diff"] += calculate_xp(real_c2, 1, taboo)
                            break
                # return "Error"
                else:
                    # Ver las compras normales
                    if c2_lvl > 0:
                        info["buys_in"].append(real_c2)
                        info["xp_diff"] += calculate_xp(real_c2, 1, taboo)
                    else:
                        # Ver adaptable / Compras de lvl0
                        if get_qty(deck1, "02110") * 2 > adaptable_uses:
                            for c1 in diffs[0]:
                                real_c1 = find_by_id(c1, cards)
                                if "xp" in real_c1:
                                    if real_c1["xp"] == 0:
                                        name1 = real_c1['real_name']
                                        if find_greater_lvl_copy_in_array(name1, diffs[1], cards, 0) == "":
                                            info["adaptable_in"].append(real_c2)
                                            info["adaptable_out"].append(real_c1)
                                            diffs[0].remove(c1)
                                            adaptable_uses += 1
                                            break
                        else:
                            info["buys_in"].append(real_c2)
                            info["xp_diff"] += 1 if "xp" in real_c2 else 0

    for c1 in diffs[0]:
        real_c1 = find_by_id(c1, cards)
        info["buys_out"].append(real_c1)

    return info


def deck_to_text(deck, cards):
    arr = []
    for c_id, qty in deck['slots'].items():
        c = find_by_id(c_id, cards)
        if c:
            title = c['name']
            level = c['xp'] if "xp" in c else 0
            arr.append((title, level, c_id))

    return arr


def find_greater_lvl_copy_in_array(title, arr, cards, lvl):
    for c_id in arr:
        c = find_by_id(c_id, cards)
        xp = c['xp'] if "xp" in c else 0
        if c['name'] == title and xp > lvl:
            return c_id
    return ""


def find_lower_lvl_copy_in_deck(title, deck, cards, lvl):
    d_array = deck_to_text(deck, cards)
    for c_t, c_lvl, c_id in d_array:
        if c_t == title and c_lvl < lvl:
            return c_id
    return ""
