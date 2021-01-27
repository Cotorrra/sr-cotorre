import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import requests
from formating import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!ah')

ah_player = sorted([c for c in requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()],
                key=lambda card: card['name'])
# only encounter cards cards
ah_encounter= [c for c in [sorted([c for c in requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()],
                key=lambda card: card['name'])] if "spoilers" in c]

@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')


@bot.command(name='j', help='Busca cartas de Jugador y de Investigador en ArkhamDB')
async def look_for_player_card(ctx, query: str):
    query_cards = [c for c in ah_player if c['name'].lower().__contains__(query.lower())]
    my_card = query_cards[0]

    if my_card['type_code'] == "investigator":
        await ctx.send(format_inv_card_f(my_card))
    else:
        await ctx.send(format_player_card(my_card))

bot.run(TOKEN)
