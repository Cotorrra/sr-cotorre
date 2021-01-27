
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


def format_player_card(c):
    formater = {"name": "*%s" % c['name'] if c['is_unique'] else "%s" % c['name'],
                "level": ("" if c['xp'] == 0 else "(%s)" % c['xp']) if "xp" in c else "",
                "subtext": "_-%s-_" % c['subtext'] if 'subtext' in c else "",
                "faction": format_card_text("[%s]" % c['faction_code']),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*" % c['traits'],
                "icons": "Íconos de Habilidad: %s \n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % c['cost'] if "cost" in c else "",
                "text": "> %s" % format_card_text(c['text']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "health_sanity": "%s%s \n" % (":Salud: %s " % c['health'] if "health" in c else "",
                                              ":Cordura: %s" % c['sanity'] if "sanity" in c else "")}

    text = "¡Carta de Jugador Encontrada!: \n" \
           "%(name)s %(level)s %(subtext)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(costs)s" \
           "%(icons)s" \
           "%(text)s" \
           "%(flavour)s" \
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
                "artist": ":paintbrush: %s\n" % c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position'])),
                "traits": "***%s***" % c['traits'],
                }
    text = "¡Carta de investigador Encontrada!: \n"\
           "%(class)s %(name)s %(subname)s \n" \
           "%(traits)s \n" \
           "%(skills)s \n" \
           "%(ability)s \n" \
           "%(health_sanity)s \n" \
           "%(artist)s" \
           "%(pack)s" % formater
    return text


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

