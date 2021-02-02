""""
Casos borde locos que tienes que ver siempre:
    Cartas multi-clase
    Cartas miriada
    Cartas excepcionales
    Cartas características
    Cartas con más de un espacio
    Traiciones cartas de jugador
"""

# Esto es para que se vea bonito en el server de ¡Tengo un Plan!

from taboo import *


def format_deck(deck, info):
    formater = {"name": "**%s**" % deck['name'],
                "investigator": "_Mazo para %s_" % deck['investigator_name'],
                "xp": "Experiencia Necesaria: %s" % str(info['xp']),
                "assets": "__Apoyos:__ (%s) %s \n" % make_string(info['assets']) if len(info['assets']) > 0 else "",
                "permanents": "__Permanentes:__ (%s) %s \n" % make_string(info['permanents']) if len(
                    info['permanents']) > 0 else "",
                "events": "__Eventos:__ (%s) %s \n" % make_string(info['events']) if len(info['events']) > 0 else "",
                "skills": "__Habilidades:__ (%s) %s \n" % make_string(info['skills']) if len(
                    info['skills']) > 0 else "",
                "treachery": "__Traiciones/Enemigos__: (%s) %s \n" % make_string(info['treachery']) if len(
                    info['treachery']) > 0 else "",
                }
    text = "¡Mazo Encontrado!: \n\n" \
           "%(name)s \n" \
           "%(investigator)s \n" \
           "%(xp)s \n" \
           "%(assets)s" \
           "%(permanents)s" \
           "%(events)s " \
           "%(skills)s " \
           "%(treachery)s" % formater
    return text


def make_string(array):
    text = ""
    qty = 0
    for c in array:
        text += "\n\t %s" % format_card_text(c)[1:]
        qty += 1
    return qty, text


def list_rest(array):
    text = ""
    for c in array:
        if c['type_code'] == "investigator":
            text += " %s \n" % format_inv_card_f_short(c)
        else:
            text += " %s \n" % format_player_card_short(c, 1)[1:]
    return text


def format_deck_cards(deck, cards):
    info = {"assets": [], "events": [], "skills": [], "treachery": [], "permanents": [], "xp": 0}
    for c_id, qty in deck['slots'].items():
        card = [c for c in cards if c['code'] == c_id][0]
        text = format_player_card_short(card, qty)
        taboo_version = "00" + str(deck['taboo_id'])
        info["xp"] += calculate_xp(card, qty, taboo_version)

        if card['permanent']:
            info['permanents'].append(text)
        elif card['type_code'] == "asset":
            info['assets'].append(text)
        elif card['type_code'] == "event":
            info['events'].append(text)
        elif card['type_code'] == "skill":
            info['skills'].append(text)
        else:
            info['treachery'].append(text)

    info['assets'] = sorted(info['assets'])
    info['events'] = sorted(info['events'])
    info['skills'] = sorted(info['skills'])
    info['treachery'] = sorted(info['treachery'])
    info['permanents'] = sorted(info['permanents'])
    return info


def format_player_card_short(c, qty):
    formater = {"name": "%s" % c['name'],
                "level": "%s" % format_xp(c),
                "class": faction_order[c['faction_code']] + format_faction(c),
                "quantity": "x%s" % str(qty) if qty > 1 else "",
                "subname": ": _%s_" % c['subname'] if "subname" in c else ""
                }
    text = "%(class)s %(name)s%(level)s%(subname)s %(quantity)s" % formater
    return text


def format_health_sanity(c):
    return format_card_text("%s%s" % ("[health] %s " % format_number(c['health']) if "health" in c else "",
                                      "[sanity] %s" % format_number(c['sanity']) if "sanity" in c else ""))


def format_number(n):
    if int(n) == -2:
        return "X"
    else:
        return str(n)


def format_player_card(c):
    formater = {"name": "***%s**" % c['name'] if c['is_unique'] else "**%s**" % c['name'],
                "level": format_xp(c),
                "subtext": " _-%s-_" % c['subname'] if 'subname' in c else "",
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s* " % c['traits'],
                "icons": "Iconos de Habilidad: %s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % format_number(c['cost']) if "cost" in c else "",
                "text": "> %s \n" % format_card_text(c['text']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "health_sanity": "%s \n" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
                "taboo_text": format_taboo_text(c['code'])
                }

    text = "¡Carta de Jugador Encontrada!: \n\n" \
           "%(name)s%(subtext)s%(level)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(costs)s" \
           "%(icons)s" \
           "%(text)s" \
           "%(flavour)s " \
           "%(health_sanity)s \n" \
           "%(taboo_text)s" \
           "%(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_enemy_stats(c):
    formater = {"health": "[health] %s%s " % (format_number(c['health']) if "health" in c else "-",
                                              "[per_investigator]" if c[
                                                  "health_per_investigator"] else ""),
                "combat": "[combat] %s " % (format_number(c['enemy_fight']) if "enemy_fight" in c else "-"),
                "agility": "[agility] %s" % (format_number(c['enemy_evade']) if "enemy_evade" in c else "-")
                }

    return format_card_text("%(health)s%(combat)s%(agility)s\n" % formater)


def format_enemy_card(c):
    formater = {"name": "*%s" % c['name'] if c['is_unique'] else "%s" % c['name'],
                "subtext": " _-%s-_" % c['subname'] if 'subname' in c else "",
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s* " % c['traits'],
                "text": "> %s \n" % format_card_text(c['text']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "stats": format_enemy_stats(c),
                "attack": "Ataque: %s\n" % format_attack(c) if format_attack(c) != "" else ""}

    text = "¡Carta de Enemigo Encontrada!: \n\n" \
           "%(name)s%(subtext)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(stats)s" \
           "%(text)s" \
           "%(flavour)s " \
           "%(attack)s" \
           "%(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_treachery_card(c):
    formater = {"name": "*%s" % c['name'] if c['is_unique'] else "%s" % c['name'],
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*" % c['traits'],
                "text": "> %s \n" % format_card_text(c['text']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position']))}

    text = "¡Carta de Traición Encontrada!: \n\n" \
           "%(name)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(text)s" \
           "%(flavour)s " \
           "%(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_attack(c):
    formater = {
        "damage": "[health]" * c['enemy_damage'] if "enemy_damage" in c else "",
        "horror": "[sanity]" * c['enemy_horror'] if "enemy_horror" in c else "",
    }
    return format_card_text("%(damage)s%(horror)s" % formater)


def format_inv_card_f_short(c):
    formater = {"class": format_card_text("[%s]" % c['faction_code']),
                "name": "%s" % c['name'],
                "skills": format_skill_icons_2(c),
                "health_sanity": format_card_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                }
    text = "%(class)s %(name)s [%(skills)s] [%(health_sanity)s]" % formater
    return text


def format_inv_card_f(c):
    formater = {"class": format_card_text("[%s]" % c['faction_code']),
                "name": "**%s**" % c['name'],
                "subname": "_-%s-_" % c['subname'],
                "skills": format_skill_icons_2(c),
                "health_sanity": format_card_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                "ability": format_card_text("> %s" % c['text']),
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "traits": "*%s*" % c['traits'],
                "taboo_text": format_taboo_text(c['code'])
                }
    text = "¡Carta de investigador Encontrada!: \n\n" \
           "%(class)s %(name)s %(subname)s \n" \
           "%(traits)s \n" \
           "%(skills)s \n" \
           "%(ability)s \n" \
           "%(health_sanity)s \n\n" \
           "%(taboo_text)s" \
           "%(artist)s \n" \
           "%(pack)s" % formater
    return text


def format_faction(c):
    if 'faction2_code' in c:
        return format_card_text("[%s]/[%s]" % (c['faction_code'], c['faction2_code']))
    else:
        return format_card_text("[%s]" % c['faction_code'])


def format_skill_icons(c):
    formater = {
        "will": "[willpower]" * c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect]" * c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat]" * c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility]" * c['skill_agility'] if "skill_agility" in c else "",
        "wild": "[wild]" * c['skill_wild'] if "skill_wild" in c else "",
    }
    return format_card_text("%(will)s%(int)s%(com)s%(agi)s%(wild)s" % formater)


def format_skill_icons_2(c):
    formater = {
        "will": "[willpower] %s " % c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect] %s " % c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat] %s " % c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility] %s" % c['skill_agility'] if "skill_agility" in c else "",
    }
    return format_card_text("%(will)s%(int)s%(com)s%(agi)s" % formater)


def format_card_text(text):
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


text_format = {"[free]": "<:Libre:789610643262799913>",
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
               "[mythos]": "<:plan:789646429043425300>",
               "[health]": "<:Salud:789610448604758066>",
               "[sanity]": "<:Cordura:789610438748012594>",
               "[per_investigator]": "<:Porinvestigador:789610613650489434>",
               "</b>": "**",
               "<b>": "**",
               "<em>": "__",
               "</em>": "__",
               "[[": "***",
               "]]": "***",
               "\n": "\n> ",
               }

faction_order = {
    "guardian": "0",
    "seeker": "1",
    "rogue": "2",
    "mystic": "3",
    "survivor": "4",
    "neutral": "5",
    "mythos": "6",
}


def format_taboo_text(card_id, version=current_taboo):
    text = "Tabú más reciente: \n"
    if is_in_taboo(card_id, version):
        card = get_tabooed_card(card_id, version)
        if 'xp' in card:
            if card['xp'] >= 0:
                text += "> Encadenada: +%d de experiencia \n" % card['xp']
            else:
                text += "> Desencadenada: -%d de experiencia \n" % card['xp']
        if 'text' in card:
            text += "> %s \n" % format_card_text(card['text'])
        return text
    else:
        return ""
