import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import requests
from formating import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!ah')

ah_all_cards = sorted([c for c in requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()],
                   key=lambda card: card['name'])

ah_player = sorted([c for c in requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()],
                   key=lambda card: card['name'])
# only encounter cards cards
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]

ah_deck_cards = sorted

showing = True


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')


@bot.command(name='j', help='Busca cartas de Jugador y de Investigador en ArkhamDB')
async def look_for_player_card(ctx, query: str):
    query_cards = [c for c in ah_player if c['name'].lower().__contains__(query.lower())]
    my_card = query_cards[0]

    if my_card['type_code'] == "investigator":
        response = format_inv_card_f(my_card)

    else:
        response = format_player_card(my_card)

    await dev_send(showing, ctx, response)


@bot.command(name='d', help='Busca cartas de Jugador y de Investigador en ArkhamDB')
async def look_for_deck(ctx, code: str):
    req = requests.get('https://es.arkhamdb.com/api/public/decklist/%s' % code).json()
    if req == {}:
        response = "El Mazo que buscas no existe :c"
    else:
        deck_info = format_deck_cards(req, ah_all_cards)
        response = format_deck(req, deck_info)

    await dev_send(showing, ctx, response)


async def dev_send(debug, ctx, string):
    if debug:
        await ctx.send("```%s```" % string)
    else:
        await ctx.send(string)


bot.run(TOKEN)
