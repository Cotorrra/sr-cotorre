import os

from discord.ext import commands
from dotenv import load_dotenv
import requests
from formating import *
from utils import *

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


# @bot.command(name='t', help='Busca el registro de tabú de la carta pedida')
# async def look_for_taboo(ctx):

@bot.command(name='help')
async def send_help(ctx):
    response = "!ahd [numero] Busca en ArkhamDB el mazo dado y lo muestra, tanto públicos como privados.\n" \
                "!ahj [nombre] ~[subtitulo]~ ([extra]) Busca cartas en ArkhamDB.\n" \
                "[extra] puede contener ser lo siguiente: '0-5' nivel de la carta, " \
                "'G/B/R/M/S/N' la clase de la carta, P para permanente, U para único, E para excepcional."
    ctx.send(response)


@bot.command(name='j')
async def look_for_player_card(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = search(query, ah_player)

    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext(c, sub_query)]

    if keyword_mode:
        r_cards = use_pc_keywords(r_cards, keyword_query)

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


@bot.command(name='d')
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

""" # TODO: Armar los format_x...+
@bot.command(name='m')
async def look_for_encounter(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = search(query, ah_encounter)
    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext_ec(c, sub_query)]
    if keyword_mode:
        r_cards = use_ec_keywords(r_cards, keyword_query)

    if len(r_cards) == 0:
        response = "No encontré ninguna carta"

    else:
        if r_cards[0]['type_code'] == "investigator":
            response = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            response = format_act_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            response = format_agenda_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            response = format_location_card(r_cards[0])

        else:
            response = "No sé de qué tipo es esta carta"
            response = format_player_card(r_cards[0])
    await dev_send(showing, ctx, response)
"""

async def dev_send(debug, ctx, string):
    if debug:
        await ctx.send("```%s```" % string)
    else:
        await ctx.send(string)

bot.run(TOKEN)
