import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import requests

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
               "</b>": "**",
               "<b>": "**",
               "[[": "***",
               "]]": "***",
               "\n": "\n > ",
               }

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!ah')

ah_api = sorted([c for c in requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()],
                key=lambda card: card['name'])
# only player cards
ah_api_p = [c for c in ah_api if "spoiler" not in c]

@bot.command(name='j')
async def look_for_player_card(ctx, query: str):
    query_cards = [c for c in ah_api if c['name'].lower().__contains__(query.lower())]
    my_card = query_cards[0]

    await ctx.send(format_player_card(my_card))


def format_player_card(c):
    formater = {"name": "***%s**" % c['name'] if c['is_unique'] else "**%s**" % c['name'],
                "level": ("" if c['xp'] == 0 else "(%s)" % c['xp']) if "xp" in c else "",
                "subtext": "_-%s-_" % c['subtext'] if 'subtext' in c else "",
                "faction": format_card_text("[%s]" % c['faction_code']),
                "type": "**%s**" % c['type_name'],
                "traits": "__%s__" % c['traits'],
                "icons": "Íconos de Habilidad: %s \n" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "Coste: %s \n" % c['cost'] if "cost" in c else "",
                "text": "> %s \n" % format_card_text(c['text']),
                "flavour": "__%s__\n" % c['flavor'] if "flavor" in c else "",
                "artist": c['illustrator'],
                "pack": "%s #%s" % (c['pack_name'], str(c['position']))}

    text = "%(name)s %(level)s %(subtext)s\n" \
           "%(type)s %(faction)s \n" \
           "%(traits)s \n" \
           "%(costs)s" \
           "%(icons)s" \
           "%(text)s" \
           "%(flavour)s" \
           ":paintbrush: %(artist)s \n" \
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
    text = "%(will)s%(int)s%(com)s%(agi)s%(wild)s" % formater
    return text


def format_card_text(text):
    for key, value in text_format.items():
        text = text.replace(key, value)
    return text


bot.run(TOKEN)
