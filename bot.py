import json
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import requests
from formating import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!ah')

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter cards include: Special player cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]

showing = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')



@bot.command(name='j',
             help='Busca cartas de Jugador y de Investigador en ArkhamDB, '
                  'puedes usar (X) para buscar un nivel particular y/o ~X~ para buscar un subtexto en particular')
async def look_for_player_card(ctx):

    query = ' '.join(ctx.message.content.split()[1:])
    lvl_mode = False
    lvl_query = ""
    sub_text_mode = False
    sub_query = ""

    if query.__contains__("(") and query.__contains__(")"):
        lvl_mode = True
        (query, lvl_query) = find_and_extract(query, "(", ")")

    if query.find("~") >= 0:
        sub_text_mode = True
        query = query.replace("~%s~" % sub_query, "", 1)
        (query, sub_query) = find_and_extract(query, "~", "~")

    r_cards = sorted([c for c in ah_player if hits_in_string(c['name'], query) > 0],
                     key=lambda card: -hits_in_string(card['name'], query))

    # Sales en los resultados aparte si estas igual de hits con las palabras
    r_cards = [c for c in r_cards if hits_in_string(c['name'], query) == hits_in_string(r_cards[0]['name'], query)]

    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext(c, sub_query)]

    if lvl_mode:
        r_cards = [c for c in r_cards if filter_by_level(c, int(lvl_query))]

    if len(r_cards) == 0:
        response = "No encontré ninguna carta"

    else:
        if r_cards[0]['type_code'] == "investigator":
            response = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = format_treachery_card(r_cards[0])

        else:
            response = format_player_card(r_cards[0])

        if len(r_cards) > 1:
            response += "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])
    await dev_send(showing, ctx, response)


@bot.command(name='d', help='Busca mazos públicos y privados en ArkhamDB con su código')
async def look_for_deck(ctx, code: str):
    link = 'https://es.arkhamdb.com/api/public/deck/%s' % code
    req = requests.get(link)
    if req.url != link:
        link = 'https://es.arkhamdb.com/api/public/decklist/%s' % code
        req = requests.get(link)
        if req.url != link:
            response = "Mazo no encontrado"
            await dev_send(showing, ctx, response)

    deck_info = format_deck_cards(req.json(), ah_all_cards)
    response = format_deck(req.json(), deck_info)

    await dev_send(showing, ctx, response)


# @bot.command(name='e', help='Busca cartas de encuentros (En construcción)')
# async def look_for_encounter(ctx, code: str):
#    response = "En construcción"
#    await dev_send(showing, ctx, response)


async def dev_send(debug, ctx, string):
    if debug:
        await ctx.send("```%s```" % string)
    else:
        await ctx.send(string)

bot.run(TOKEN)
