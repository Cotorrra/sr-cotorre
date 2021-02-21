from formating.formating_utils import *


def format_deck(deck, info):
    formater = {"name": "**%s**" % deck['name'],
                "investigator": "_Mazo para %s_" % deck['investigator_name'],
                "xp": "Experiencia Necesaria: %s" % str(info['xp']),
                "assets": "__Apoyos:__ (%s) %s \n" % make_string(info, 'assets') if len(info['assets']) > 0 else "",
                "permanents": "__Permanentes:__ (%s) %s \n" % make_string(info, 'permanents') if len(
                    info['permanents']) > 0 else "",
                "events": "__Eventos:__ (%s) %s \n" % make_string(info, 'events') if len(info['events']) > 0 else "",
                "skills": "__Habilidades:__ (%s) %s \n" % make_string(info, 'skills') if len(
                    info['skills']) > 0 else "",
                "treachery": "__Traiciones/Enemigos__: (%s) %s \n" % make_string(info, 'treachery') if len(
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


def format_upgraded_deck(deck1, info):
    formater = {"name": "**%s**" % deck1['name'],
                "investigator": "_Mazo para %s_" % deck1['investigator_name'],
                "xp": "Experiencia Utilizada: %s" % str(info['xp_diff']),
                "purchases": "__Mejoras:__ %s \n" % format_upgrades(info, 'buys') if in_out_len(info,
                                                                                                'buys') > 0 else "",
                "adaptable": "__Adaptable:__  %s \n" % format_upgrades(info, 'adaptable') if in_out_len(info,
                                                                                                        'adaptable') > 0 else "",
                "arcane": "__Investigación Arcana:__ %s \n" % format_upgrades(info, 'arcane_upg')
                if in_out_len(info, 'arcane_upg') > 0 else "",
                "special": "__Especial (Agnes/Skids)__: %s \n" % format_special_upgr(info) if len(
                    info['parallel_buy']) > 0 else "",
                }
    text = "¡Mejora Calculada!: \n\n" \
           "%(name)s \n" \
           "%(investigator)s \n" \
           "%(xp)s \n" \
           "%(upgrades)s" \
           "%(purchases)s" \
           "%(adaptable)s " \
           "%(arcane)s " \
           "%(special)s" % formater
    return text


def format_player_card(c):
    formater = {"name": "***%s**" % c['name'] if c['is_unique'] else "**%s**" % c['name'],
                "level": format_xp(c),
                "subtext": " _-%s-_" % c['subname'] if 'subname' in c else "",
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "icons": "Iconos de Habilidad: %s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % format_number(c['cost']) if "cost" in c else "",
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": format_set(c),
                "health_sanity": "%s \n" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
                "taboo_text": format_taboo_text(c['code'])
                }

    text = "¡Carta de Jugador Encontrada!: \n\n" \
           "%(name)s%(subtext)s%(level)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s" \
           "%(costs)s" \
           "%(icons)s" \
           "%(text)s" \
           "%(flavour)s " \
           "%(health_sanity)s \n" \
           "%(taboo_text)s" \
           "%(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_enemy_card(c):
    formater = {"name": "***%s**" % c['name'] if c['is_unique'] else "**%s**" % c['name'],
                "subtext": " _-%s-_" % c['subname'] if 'subname' in c else "",
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s* " % c['traits'],
                "text": "%s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": format_set(c),
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
           "\n %(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_act_card_f(c):
    formater = {"name": "**%s**" % c['name'],
                "stage": "__Acto %s__" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "clues": format_clues(c),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": ":paintbrush: %s" % c['illustrator']}

    text = "¡Carta de Acto encontrada!: \n\n" \
           "%(name)s \n" \
           "%(stage)s \n" \
           "%(flavour)s" \
           "%(clues)s \n" \
           "%(text)s" \
           "\n %(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_agenda_card_f(c):
    formater = {"name": "**%s**" % c['name'],
                "stage": "__Plan %s__" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "doom": format_text("[doom] %s" % (c['doom'] if "doom" in c else "-")),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": ":paintbrush: %s" % c['illustrator']}

    text = "¡Carta de Plan encontrada!: \n\n" \
           "%(name)s \n" \
           "%(stage)s \n" \
           "%(flavour)s" \
           "%(doom)s \n" \
           "%(text)s" \
           "\n %(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_location_card(c):
    formater = {"name": "**%s**" % c['name'],
                "subtext": " _-%s-_" % c['subname'] if 'subname' in c else "",
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": format_set(c),
                "shroud": "Velo: %s \n" % str(c['shroud']),
                "clues": format_clues(c),
                }

    text = "¡Carta de Lugar Encontrada!: \n\n" \
           "%(name)s%(subtext)s\n" \
           "%(traits)s" \
           "%(text)s" \
           "%(flavour)s " \
           "%(shroud)s " \
           "%(clues)s" \
           "\n %(artist)s \n" \
           "%(pack)s" % formater

    return text


def format_scenario_card(c):
    formater = {"name": "**%s**" % c['name'],
                "text": "> %s \n" % format_text(c['text']),
                "b_text": "> %s \n" % format_text(c['back_text']),
                "pack": format_set(c)}

    text = "¡Carta de Escenario encontrada!: \n\n" \
           "%(name)s \n\n" \
           "%(text)s \n" \
           "%(b_text)s " \
           "%(pack)s" % formater

    return text


def format_treachery_card(c):
    formater = {"name": "***%s**" % c['name'] if c['is_unique'] else "**%s**" % c['name'],
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*" % c['traits'],
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": ":paintbrush: %s" % c['illustrator'],
                "set": format_set(c)}

    text = "¡Carta de Traición Encontrada!: \n\n" \
           "%(name)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(text)s" \
           "%(flavour)s " \
           "%(artist)s \n" \
           "%(set)s" % formater

    return text


def format_inv_card_f(c):
    formater = {"class": format_text("[%s]" % c['faction_code']),
                "name": "**%s**" % c['name'],
                "subname": "_-%s-_" % c['subname'],
                "skills": format_inv_skills(c),
                "health_sanity": format_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                "ability": "> %s \n" % format_card_text(c),
                "artist": ":paintbrush: %s" % c['illustrator'],
                "pack": format_set(c),
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
