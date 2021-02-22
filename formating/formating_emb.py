from formating.formating_utils import *

import discord.embeds


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

    embed = discord.Embed(title=m_title, description=m_description, color=info['color'])
    if len(info['assets']) > 0:
        embed.add_field(name="%(assets)s" % formater, value=make_string(info, 'assets')[1], inline=False)

    if len(info['permanents']) > 0:
        embed.add_field(name="%(permanents)s" % formater, value=make_string(info, 'permanents')[1], inline=False)

    if len(info['events']) > 0:
        embed.add_field(name="%(events)s" % formater, value=make_string(info, 'events')[1], inline=False)

    if len(info['skills']) > 0:
        embed.add_field(name="%(skills)s" % formater, value=make_string(info, 'skills')[1], inline=False)

    if len(info['skills']) > 0:
        embed.add_field(name="%(treachery)s" % formater, value=make_string(info, 'treachery')[1], inline=False)

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

    if in_out_len(info, 'arcane_upg') > 0:
        embed.add_field(name="Mejora de Investigación Arcana", value=format_upgrades(info, 'arcane_upg'), inline=False)

    if len(info['parallel_buy']) > 0:
        embed.add_field(name="Mejora Especial (Agnes/Skids)", value=format_special_upgr(info), inline=False)

    if in_out_len(info, 'adaptable') > 0:
        embed.add_field(name="Cambios por Adaptable (-):",
                        value=format_list_of_cards(format_in_out_upgr(info, "adaptable")[0]), inline=True)

        embed.add_field(name="Cambios por Adaptable (+)",
                        value=format_list_of_cards(format_in_out_upgr(info, "adaptable")[1]), inline=True)

    return embed


def format_player_card(c):
    formater = {"name": format_name(c),
                "level": format_xp(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "icons": "Iconos de Habilidad: %s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % format_number(c['cost']) if "cost" in c else "",
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "health_sanity": "%s \n" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
                "taboo_text": format_taboo_text(c['code'])
                }
    m_title = " %(faction)s %(name)s%(subtext)s%(level)s" % formater
    m_description = "%(type)s \n" \
                    "%(traits)s" \
                    "%(costs)s" \
                    "%(icons)s" \
                    "%(text)s\n" \
                    "%(flavour)s " \
                    "%(health_sanity)s \n" \
                    "%(taboo_text)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_enemy_card(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s* " % c['traits'],
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "stats": format_enemy_stats(c),
                "attack": "Ataque: %s\n" % format_attack(c) if format_attack(c) != "" else ""}

    m_title = " %(faction)s %(name)s%(subtext)s" % formater
    m_description = "%(type)s \n" \
                    "%(traits)s \n" \
                    "%(stats)s" \
                    "%(text)s" \
                    "%(flavour)s " \
                    "%(attack)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_act_card_f(c):
    formater = {"name": format_name(c),
                "stage": "__Acto %s__" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "clues": format_clues(c),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": format_illustrator(c)}

    m_title = "%(name)s " % formater
    m_description = "%(stage)s \n" \
                    "%(flavour)s" \
                    "%(clues)s \n" \
                    "%(text)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_agenda_card_f(c):
    formater = {"name": format_name(c),
                "stage": "__Plan %s__" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "doom": format_text("[doom] %s" % (c['doom'] if "doom" in c else "-")),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": format_illustrator(c)}

    m_title = "%(name)s " % formater
    m_description = "%(stage)s \n" \
                    "%(flavour)s" \
                    "%(doom)s \n" \
                    "%(text)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_location_card(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "shroud": "Velo: %s \n" % str(c['shroud']),
                "clues": format_clues(c),
                }
    m_title = "%(name)s%(subtext)s" % formater
    m_description = "%(traits)s" \
                    "%(text)s" \
                    "%(flavour)s " \
                    "%(shroud)s " \
                    "%(clues)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_scenario_card(c):
    formater = {"name": format_name(c),
                "text": "> %s \n" % format_text(c['text']),
                "b_text": "> %s \n" % format_text(c['back_text']),
                "pack": format_set(c)}

    m_title = "%(name)s" % formater
    m_description = "%(text)s \n" \
                    "%(b_text)s " % formater
    m_footnote = "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_treachery_card(c):
    formater = {"name": format_name(c),
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "traits": "*%s*" % c['traits'],
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": format_illustrator(c),
                "set": format_set(c)}

    m_title = "%(faction)s %(name)s" % formater
    m_description = "%(type)s \n" \
                    "%(traits)s \n" \
                    "%(text)s" \
                    "%(flavour)s " % formater
    m_footnote = "%(artist)s \n" \
                 "%(set)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_inv_card_f(c):
    formater = {"class": format_faction(c),
                "name": format_name(c),
                "subname": format_subtext(c),
                "skills": format_inv_skills(c),
                "health_sanity": format_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                "ability": "> %s \n" % format_card_text(c),
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "traits": "*%s*" % c['traits'],
                "taboo_text": format_taboo_text(c['code'])
                }

    m_title = "%(class)s %(name)s %(subname)s " % formater
    m_description = "%(traits)s \n" \
                    "%(skills)s \n" \
                    "%(ability)s \n" \
                    "%(health_sanity)s \n\n" \
                    "%(taboo_text)s" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed
