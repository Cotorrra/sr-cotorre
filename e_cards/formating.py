import discord.embeds

from core.formating import *
from e_cards.formating_utils import format_enemy_stats, format_attack, format_clues


def format_enemy_card(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "type": "__%s__\n" % c['type_name'],
                "traits": "*%s*\n" % c['traits'],
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "stats": format_enemy_stats(c),
                "attack": "Ataque: %s\n" % format_attack(c) if format_attack(c) != "" else "",
                "victory": format_victory(c),
                "vengeance": format_vengeance(c),
                }

    m_title = " %(faction)s %(name)s%(subtext)s" % formater
    m_description = "%(type)s" \
                    "%(traits)s" \
                    "%(stats)s\n" \
                    "%(text)s" \
                    "%(attack)s\n" \
                    "%(flavour)s \n" \
                    "%(victory)s" \
                    "%(vengeance)s\n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_act_card_f(c):
    formater = {"name": format_name(c),
                "stage": "__Acto %s__\n" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "clues": "%s\n" % format_clues(c),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": format_illustrator(c)
                }

    m_title = "%(name)s " % formater
    m_description = "%(stage)s" \
                    "%(clues)s\n" \
                    "%(flavour)s" \
                    "%(text)s \n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_agenda_card_f(c):
    formater = {"name": format_name(c),
                "stage": "__Plan %s__\n" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "doom": format_text("[doom] %s" % (c['doom'] if "doom" in c else "-")),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "pack": format_set(c),
                "artist": format_illustrator(c)}

    m_title = "%(name)s " % formater
    m_description = "%(stage)s" \
                    "%(doom)s\n" \
                    "%(flavour)s" \
                    "%(text)s\n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_location_card_f(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "shroud": "Velo: %s" % str(c['shroud']),
                "clues": format_clues(c),
                "victory": format_victory(c),
                "vengeance": format_vengeance(c),
                }
    m_title = "%(name)s%(subtext)s" % formater
    m_description = "%(traits)s" \
                    "%(shroud)s | %(clues)s \n" \
                    "%(text)s" \
                    "%(flavour)s \n" \
                    "%(victory)s" \
                    "%(vengeance)s\n" % formater
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
                    "%(b_text)s \n" % formater
    m_footnote = "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_treachery_card(c):
    formater = {"name": format_name(c),
                "faction": format_faction(c),
                "type": "__%s__\n" % c['type_name'],
                "traits": "*%s*\n" % c['traits'],
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                "artist": format_illustrator(c),
                "set": format_set(c)}

    m_title = "%(faction)s %(name)s" % formater
    m_description = "%(type)s" \
                    "%(traits)s \n" \
                    "%(text)s \n" \
                    "%(flavour)s \n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(set)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed
