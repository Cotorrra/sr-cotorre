import discord

from core.formating import format_text
from p_cards.formating import format_inv_card_f_short, format_player_card_short
from p_cards.utils import get_color_by_investigator
from taboo.taboo import calculate_xp


def format_deck(deck, info):
    formater = {"name": "%s" % deck['name'],
                "investigator": "_Mazo para %s_" % deck['investigator_name'],
                "xp": "Experiencia Necesaria: %s" % str(info['xp']),
                "assets": "Apoyos: (%s)" % make_string(info, 'assets')[0] if len(info['assets']) > 0 else "",
                "permanents": "Permanentes: (%s)" % make_string(info, 'permanents')[0] if len(
                    info['permanents']) > 0 else "",
                "events": "Eventos: (%s)" % make_string(info, 'events')[0] if len(info['events']) > 0 else "",
                "skills": "Habilidades: (%s)" % make_string(info, 'skills')[0] if len(
                    info['skills']) > 0 else "",
                "treachery": "Traiciones/Enemigos: (%s)" % make_string(info, 'treachery')[0] if len(
                    info['treachery']) > 0 else "",
                }

    m_title = "%(name)s" % formater
    m_description = "%(investigator)s \n" \
                    "%(xp)s" % formater

    inline = False

    embed = discord.Embed(title=m_title, description=m_description, color=info['color'])
    if len(info['assets']) > 0:
        embed.add_field(name="%(assets)s" % formater, value=make_string(info, 'assets')[1], inline=inline)

    if len(info['permanents']) > 0:
        embed.add_field(name="%(permanents)s" % formater, value=make_string(info, 'permanents')[1], inline=inline)

    if len(info['events']) > 0:
        embed.add_field(name="%(events)s" % formater, value=make_string(info, 'events')[1], inline=inline)

    if len(info['skills']) > 0:
        embed.add_field(name="%(skills)s" % formater, value=make_string(info, 'skills')[1], inline=inline)

    if len(info['skills']) > 0:
        embed.add_field(name="%(treachery)s" % formater, value=make_string(info, 'treachery')[1], inline=inline)

    return embed


def format_upgraded_deck(deck1, info):
    formater = {"name": "%s" % deck1['name'],
                "investigator": "_Mazo para %s_" % deck1['investigator_name'],
                "xp": "Experiencia Utilizada: %s" % str(info['xp_diff']),
                }

    m_title = "%(name)s" % formater
    m_description = "%(investigator)s \n" \
                    "%(xp)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=info['color'])

    if len(info['buys_out']) > 0:
        embed.add_field(name="Cambios (-):",
                        value=format_list_of_cards(format_in_out_upgr(info, "buys")[0]), inline=True)

    if len(info['buys_in']) > 0:
        embed.add_field(name="Cambios (+):",
                        value=format_list_of_cards(format_in_out_upgr(info, "buys")[1]), inline=True)

    # if in_out_len(info, 'arcane_upg') > 0:
    #   embed.add_field(name="Mejora de Investigación Arcana", value=format_upgrades(info, 'arcane_upg'), inline=False)

    # if len(info['parallel_buy']) > 0:
    #    embed.add_field(name="Mejora Especial (Agnes/Skids)", value=format_special_upgr(info), inline=False)

    # if in_out_len(info, 'adaptable') > 0:
    #    embed.add_field(name="Cambios por Adaptable (-):",
    #                    value=format_list_of_cards(format_in_out_upgr(info, "adaptable")[0]), inline=True)

    #    embed.add_field(name="Cambios por Adaptable (+)",
    #                    value=format_list_of_cards(format_in_out_upgr(info, "adaptable")[1]), inline=True)

    return embed

def format_deck_cards(deck, cards):
    info = {"assets": [], "events": [], "skills": [], "treachery": [], "permanents": [], "assets_q": 0, "events_q": 0,
            "skills_q": 0, "treachery_q": 0, "permanents_q": 0,
            "xp": 0, "color": get_color_by_investigator(deck, cards)}
    taboo_version = "00" + str(deck['taboo_id'])
    for c_id, qty in deck['slots'].items():
        card = [c for c in cards if c['code'] == c_id][0]
        text = format_player_card_short(card, qty)
        info["xp"] += calculate_xp(card, qty, taboo_version)

        # if card['permanent']:
        #    info['permanents'].append(text)
        #    info['permanents_q'] += qty
        # el
        if card['type_code'] == "asset":
            info['assets'].append(text)
            info['assets_q'] += qty
        elif card['type_code'] == "event":
            info['events'].append(text)
            info['events_q'] += qty
        elif card['type_code'] == "skill":
            info['skills'].append(text)
            info['skills_q'] += qty
        else:
            info['treachery'].append(text)
            info['treachery_q'] += qty

    info['assets'] = sorted(info['assets'])
    info['events'] = sorted(info['events'])
    info['skills'] = sorted(info['skills'])
    info['treachery'] = sorted(info['treachery'])
    info['permanents'] = sorted(info['permanents'])
    return info


def in_out_len(info, prefix):
    return max(len(info[prefix + "_in"]), len(info[prefix + "_out"]))


def format_remove_upgr_duplicates(arr):
    copy_arr = arr.copy()
    array = []

    while len(copy_arr) > 0:
        q = 0
        card = copy_arr[0]
        while card in copy_arr:
            q += 1
            copy_arr.remove(card)

        text = format_player_card_short(card, q)
        array.append(text)
    array = sorted(array)
    arr2 = []
    for c in array:
        text = c[1:]
        arr2.append(text)

    return arr2


def format_in_out_upgr(info, prefix):
    array_out = format_remove_upgr_duplicates(info[prefix + "_out"])
    array_in = format_remove_upgr_duplicates(info[prefix + "_in"])
    return array_out, array_in


def format_list_of_cards(cards):
    text = ""
    for c in cards:
        text += "%s \n" % c
    return text


def format_upgrades(info, prefix):
    pf_out, pf_in = format_in_out_upgr(info, prefix)
    m_length = max(len(pf_out), len(pf_out))
    text = ""
    for i in range(m_length):
        left = pf_out[i] if i < len(pf_out) else ""
        right = pf_in[i] if i < len(pf_in) else ""
        text += "\n %s <:Accion:789610653912399891> %s" % (left, right)

    return text


def format_special_upgr(info):
    text = ""
    buys = format_remove_upgr_duplicates(info['parallel_buy'])
    for card in buys:
        text += "%s \n" % buys
    return text


def make_string(info, tag, prefix=""):
    array = info[tag]
    text = ""
    for c in array:
        text += "%s%s \n" % (prefix, format_text(c)[1:])
    return info["%s_q" % tag], text


def list_rest(array):
    text = ""
    for c in array:
        if c['type_code'] == "investigator":
            text += "%s \n" % format_inv_card_f_short(c)
        else:
            text += "%s \n" % format_player_card_short(c, 1)[1:]
    return text

