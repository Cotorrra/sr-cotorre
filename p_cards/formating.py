import discord.embeds

from core.formating import format_name, format_subtext, format_faction, format_number, format_card_text, format_text, \
    format_illustrator, format_set, set_thumbnail_image, color_picker, faction_order, format_victory
from p_cards.utils import format_xp, format_slot, format_skill_icons, format_health_sanity, format_inv_skills
from taboo.taboo import format_taboo_text


def format_player_card(c):
    formater = {"name": format_name(c),
                "level": format_xp(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "type": "__%s__" % c['type_name'],
                "slot": format_slot(c),
                "traits": "*%s*\n" % c['traits'] if 'traits' in c else "",
                "icons": "Iconos de Habilidad: %s\n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % format_number(c['cost']) if "cost" in c else "",
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "health_sanity": "%s \n" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
                "taboo_text": format_taboo_text(c['code']),
                "victory": format_victory(c),
                }
    m_title = "%(faction)s %(name)s%(subtext)s%(level)s" % formater
    m_description = "%(type)s %(slot)s\n" \
                    "%(traits)s" \
                    "%(costs)s" \
                    "%(icons)s\n" \
                    "%(text)s" \
                    "%(victory)s" \
                    "%(health_sanity)s\n" \
                    "%(flavour)s " \
                    "%(taboo_text)s\n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_inv_card_f(c):
    formater = {"class": format_faction(c),
                "name": format_name(c),
                "subname": format_subtext(c),
                "skills": "%s \n" % format_inv_skills(c),
                "health_sanity": format_text("%s%s\n" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                "ability": "> %s \n" % format_card_text(c),
                "artist": format_illustrator(c),
                "pack": format_set(c),
                "traits": "*%s*\n" % c['traits'],
                "taboo_text": format_taboo_text(c['code']),
                "flavour": "_%s_\n" % c['flavor'] if "flavor" in c else "",
                }

    m_title = "%(class)s %(name)s %(subname)s " % formater
    m_description = "%(skills)s" \
                    "%(traits)s \n" \
                    "%(ability)s" \
                    "%(health_sanity)s \n" \
                    "%(flavour)s" \
                    "%(taboo_text)s \n" % formater
    m_footnote = "%(artist)s \n" \
                 "%(pack)s" % formater

    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c))
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed)
    return embed


def format_player_card_short(c, qty=0):
    formater = {"name": "%s" % c['name'],
                "level": "%s" % format_xp(c),
                "class": faction_order[c['faction_code']] + format_faction(c),
                "quantity": "x%s" % str(qty) if qty > 1 else "",
                "subname": ": _%s_" % c['subname'] if ("subname" in c and not c["is_unique"]) else ""
                }
    text = "%(class)s %(name)s%(level)s%(subname)s %(quantity)s" % formater
    return text


def format_inv_card_f_short(c):
    formater = {"class": format_text("[%s]" % c['faction_code']),
                "name": "%s" % c['name'],
                "skills": format_inv_skills(c),
                "health_sanity": format_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                }
    text = "%(class)s %(name)s %(skills)s| %(health_sanity)s" % formater
    return text


