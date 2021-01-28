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
from functools import reduce


def format_deck(deck, info):
    formater = {"name": "**%s**" % deck['name'],
                "investigator": "_Mazo para %s_" % deck['investigator_name'],
                "xp": "Experiencia Necesaria: %s" % str(info['xp']),
                "assets": "__Apoyos:__ (%s) %s \n" % make_string(info['assets']) if len(info['assets']) > 0 else "",
                "permanents": "__Permanentes:__ (%s) %s \n" % make_string(info['permanents']) if len(
                    info['permanents']) > 0 else "",
                "events": "__Eventos:__ (%s) %s \n" % make_string(info['events']) if len(info['events']) > 0 else "",
                "skills": "__Habilidades:__ (%s) %s \n" % make_string(info['skills']) if len(info['skills']) > 0 else "",
                "treachery": "__Traiciones/Enemigos__: (%s) %s \n" % make_string(info['treachery']) if len(
                    info['treachery']) > 0 else "",
                }
    text = "¡Mazo Encontrado!: \n" \
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
        text += "\n\t%s" % format_card_text(c)[1:]
        qty += 1
    return qty, text


def format_deck_cards(deck, cards):
    info = {"assets": [], "events": [], "skills": [], "treachery": [], "permanents": [], "xp": 0}
    for c_id, qty in deck['slots'].items():
        card = [c for c in cards if c['code'] == c_id][0]
        text = format_player_card_short(card, qty)
        info["xp"] += calculate_xp(card, qty)

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
                "quantity": str(qty),
                "subname": ": __%s__" % c['subname'] if "subname" in c else ""
                }
    text = "%(class)s %(name)s%(level)s x%(quantity)s" % formater
    return text


def format_player_card(c):
    formater = {"name": "*%s" % c['name'] if c['is_unique'] else "%s" % c['name'],
                "level": format_xp(c),
                "subtext": "_-%s-_" % c['subtext'] if 'subtext' in c else "",
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s* " % c['traits'],
                "icons": "Íconos de Habilidad: %s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % c['cost'] if "cost" in c else "",
                "text": "> %s " % format_card_text(c['text']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "health_sanity": "%s%s\n" % (":Salud: %s " % c['health'] if "health" in c else "",
                                              ":Cordura: %s" % c['sanity'] if "sanity" in c else "")}

    text = "¡Carta de Jugador Encontrada!: \n" \
           "%(name)s %(level)s %(subtext)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(costs)s" \
           "%(icons)s" \
           "%(text)s" \
           "%(flavour)s " \
           "%(health_sanity)s" \
           "%(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_inv_card_f(c):
    formater = {"class": format_card_text("[%s]" % c['faction_code']),
                "name": "**%s**" % c['name'],
                "subname": "_-%s-_" % c['subname'],
                "skills": format_skill_icons_2(c),
                "health_sanity": "%s%s" % (":Salud: %s " % c['health'], ":Cordura: %s" % c['sanity']),
                "ability": format_card_text("> %s" % c['text']),
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "traits": "***%s***" % c['traits'],
                }
    text = "¡Carta de investigador Encontrada!: \n" \
           "%(class)s %(name)s %(subname)s \n" \
           "%(traits)s \n" \
           "%(skills)s \n" \
           "%(ability)s \n" \
           "%(health_sanity)s \n" \
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
        "will": ":Voluntad:" * c['skill_willpower'] if "skill_willpower" in c else "",
        "int": ":Intelecto:" * c['skill_intellect'] if "skill_intellect" in c else "",
        "com": ":Combate:" * c['skill_combat'] if "skill_combat" in c else "",
        "agi": ":Agilidad:" * c['skill_agility'] if "skill_agility" in c else "",
        "wild": ":Comodin:" * c['skill_wild'] if "skill_wild" in c else "",
    }
    return "%(will)s%(int)s%(com)s%(agi)s%(wild)s" % formater


def format_skill_icons_2(c):
    formater = {
        "will": ":Voluntad:: %s " % c['skill_willpower'] if "skill_willpower" in c else "",
        "int": ":Intelecto:: %s " % c['skill_intellect'] if "skill_intellect" in c else "",
        "com": ":Combate:: %s " % c['skill_combat'] if "skill_combat" in c else "",
        "agi": ":Agilidad:: %s" % c['skill_agility'] if "skill_agility" in c else "",
    }
    return "%(will)s%(int)s%(com)s%(agi)s" % formater


def format_card_text(text):
    for key, value in text_format.items():
        text = text.replace(key, value)
    return text


def format_xp(c):
    if "xp" in c:
        if c['xp'] == 0:
            text = ""
        elif c['exceptional']:
            text = " [%s]" % c['xp'] * 2
        else:
            text = " [%s]" % c['xp']
    else:
        text = ""
    return text


def calculate_xp(c, qty):
    if "xp" in c:
        if c['myriad']:
            return c['xp']
        elif c['exceptional']:
            # Aunque debería haber 1 en el mazo...
            return c['xp'] * 2 * qty
        else:
            return c['xp'] * qty
    else:
        return 0

text_format = {"[free]": ":Libre:",
               "[elder_sign]": ":arcano:",
               "[willpower]": ":Voluntad:",
               "[combat]": ":Combate:",
               "[intellect]": ":Intelecto:",
               "[agility]": ":Agilidad:",
               "[action]": ":Accion:",
               "[reaction]": ":Reaccion:",
               "[bless]": ":Bendicion:",
               "[curse]": ":Maldicion:",
               "[wild]": ":Comodin:",
               "[skull]": ":calavera:",
               "[cultist]": ":sectario:",
               "[tablet]": ":tablilla:",
               "[elder_thing]": ":primigenio:",
               "[auto_fail]": ":fallo:",
               "[mystic]": ":Mistico:",
               "[seeker]": ":Buscador:",
               "[guardian]": ":Guardian:",
               "[rogue]": ":Rebelde:",
               "[survivor]": ":Superviviente:",
               "[neutral]": ":Neutral:",
               "</b>": "**",
               "<b>": "**",
               "[[": "***",
               "]]": "***",
               "\n": "\n > ",
               }

faction_order = {
    "guardian": "0",
    "seeker": "1",
    "rogue": "2",
    "mystic": "3",
    "survivor": "4",
    "neutral": "5",
}