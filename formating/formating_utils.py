from taboo import *
from utils import *


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


def format_inv_card_f_short(c):
    formater = {"class": format_text("[%s]" % c['faction_code']),
                "name": "%s" % c['name'],
                "skills": format_inv_skills(c),
                "health_sanity": format_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                }
    text = "%(class)s %(name)s [%(skills)s] [%(health_sanity)s]" % formater
    return text


def format_player_card_short(c, qty=0):
    formater = {"name": "%s" % c['name'],
                "level": "%s" % format_xp(c),
                "class": faction_order[c['faction_code']] + format_faction(c),
                "quantity": "x%s" % str(qty) if qty > 1 else "",
                "subname": ": _%s_" % c['subname'] if ("subname" in c and not c["is_unique"]) else ""
                }
    text = "%(class)s %(name)s%(level)s%(subname)s %(quantity)s" % formater
    return text


def format_text(text):
    text_format = {"[free]": "<:Libre:789610643262799913>",
                   "[fast]": "<:Libre:789610643262799913>",
                   "[elder_sign]": "<:arcano:799004602183843851>",
                   "[willpower]": "<:Voluntad:789619119704113173>",
                   "[combat]": "<:Combate:789619139403972639>",
                   "[intellect]": "<:Intelecto:789619129082576966>",
                   "[agility]": "<:Agilidad:789619149730218044>",
                   "[action]": "<:Accion:789610653912399891>",
                   "[reaction]": "<:Reaccion:789610628339073075>",
                   "[bless]": "<:bendicion:799051903816171550>",
                   "[curse]": "<:maldicion:799050838928654347>",
                   "[wild]": "<:Comodin:789619157657583636>",
                   "[skull]": "<:calavera:799059800276336721>",
                   "[cultist]": "<:sectario:799004435762249729>",
                   "[tablet]": "<:tablilla:799004747687526410>",
                   "[elder_thing]": "<:primigenio:799059800230461441>",
                   "[auto_fail]": "<:fallo:799004322796797953>",
                   "[mystic]": "<:Mistico:786679149196476467>",
                   "[seeker]": "<:Buscador:786679131768225823>",
                   "[guardian]": "<:Guardian:786679100273852457>",
                   "[rogue]": "<:Rebelde:786679171257991199>",
                   "[survivor]": "<:Superviviente:786679182284947517>",
                   "[neutral]": "<:Neutral:786679389303603221>",
                   "[mythos]": "<:encuentro:808047457971470388>",
                   "[health]": "<:Salud:808821841413668904>",
                   "[sanity]": "<:Cordura:808821830608617493>",
                   "[per_investigator]": "<:Porinvestigador:789610613650489434>",
                   "[doom]": "<:perdicion:801160341886468138>",
                   "[clues]": "<:pista:801161173864808548>",
                   "</b>": "**",
                   "<b>": "**",
                   "<em>": "_",
                   "</em>": "_",
                   "<i>": "_",
                   "</i>": "_",
                   "<u>": "__",
                   "</u>": "__",
                   "[[": "***",
                   "]]": "***",
                   "<cite>": "\n— ",
                   "</cite>": "",
                   }

    for key, value in text_format.items():
        text = text.replace(key, value)
    return text


def format_xp(c):
    if "xp" in c:
        if c['xp'] == 0:
            text = ""
        elif c['exceptional']:
            text = " (%sE)" % c['xp']
        else:
            text = " (%s)" % c['xp']
    else:
        text = ""
    return text


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


def format_health_sanity(c):
    return format_text("%s%s" % ("[health] %s " % format_number(c['health']) if "health" in c else "",
                                 "[sanity] %s" % format_number(c['sanity']) if "sanity" in c else ""))


def format_skill_icons(c):
    formater = {
        "will": "[willpower]" * c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect]" * c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat]" * c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility]" * c['skill_agility'] if "skill_agility" in c else "",
        "wild": "[wild]" * c['skill_wild'] if "skill_wild" in c else "",
    }
    return format_text("%(will)s%(int)s%(com)s%(agi)s%(wild)s" % formater)


def format_inv_skills(c):
    formater = {
        "will": "[willpower] %s " % c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect] %s " % c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat] %s " % c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility] %s" % c['skill_agility'] if "skill_agility" in c else "",
    }
    return format_text("%(will)s%(int)s%(com)s%(agi)s" % formater)


def format_number(n):
    if int(n) == -2:
        return "X"
    else:
        return str(n)


def format_enemy_stats(c):
    formater = {"health": "[health] %s%s " % (format_number(c['health']) if "health" in c else "-",
                                              "[per_investigator]" if c[
                                                  "health_per_investigator"] else ""),
                "combat": "[combat] %s " % (format_number(c['enemy_fight']) if "enemy_fight" in c else "-"),
                "agility": "[agility] %s" % (format_number(c['enemy_evade']) if "enemy_evade" in c else "-")
                }

    return format_text("%(combat)s | %(health)s | %(agility)s\n" % formater)


def format_clues(c):
    if "clues" in c:
        clues = str(c['clues'])
        if c['clues_fixed'] or c['clues'] == 0:
            return format_text("[clues] %s" % clues)
        else:
            return format_text("[clues] %s [per_investigator]" % clues)
    else:
        return format_text("[clues] -")


def format_set(c):
    text = "%s #%s" % (c['pack_name'], str(c['position']))
    if "encounter_code" in c:
        text += ": %s #%s" % (c['encounter_name'], str(c['encounter_position']))
        if c['quantity'] > 1:
            text += "-%s" % str(c['encounter_position'] + c['quantity'] - 1)
    text += "."
    return text


def format_attack(c):
    formater = {
        "damage": "[health]" * c['enemy_damage'] if "enemy_damage" in c else "",
        "horror": "[sanity]" * c['enemy_horror'] if "enemy_horror" in c else "",
    }
    return format_text("%(damage)s%(horror)s" % formater)


def format_faction(c):
    if 'faction2_code' in c:
        return format_text("[%s]/[%s]" % (c['faction_code'], c['faction2_code']))
    else:
        return format_text("[%s]" % c['faction_code'])


def format_card_text(c):
    formating = {"\n": "\n> "}
    text = format_text(c['text'])
    for key, value in formating.items():
        text = text.replace(key, value)
    return text


faction_order = {
    "guardian": "0",
    "seeker": "1",
    "rogue": "2",
    "mystic": "3",
    "survivor": "4",
    "neutral": "5",
    "mythos": "6",
}


def in_out_len(info, prefix):
    return max(len(info[prefix + "_in"]), len(info[prefix + "_out"]))


def format_remove_upgr_duplicates(arr):
    array = []
    while len(arr) > 0:
        q = 0
        card = arr[0]
        while card in arr:
            q += 1
            arr.remove(card)

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


def set_thumbnail_image(c, embed):
    if "imagesrc" in c:
        embed.set_thumbnail(url="https://arkhamdb.com%s" % c["imagesrc"])


def format_illustrator(c):
    return "🖌 %s" % c['illustrator']


def format_name(c):
    return "*%s" % c['name'] if c['is_unique'] else "%s" % c['name']


def format_subtext(c):
    return ": _%s_" % c['subname'] if 'subname' in c else ""


