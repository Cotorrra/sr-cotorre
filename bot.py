import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

from decks.deck import *
from formating.formating_emb import *
from utils import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter cards include: Special player cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]

showing = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')
    await bot.change_presence(activity=discord.Game(name="probar nuevas cosas"))


# @bot.command(name='t', help='Busca el registro de tabú de la carta pedida')
# async def look_for_taboo(ctx):
"""
@bot.command(name='hhelp')
async def send_help(ctx):
    response = "¿Necesitas ayuda?: " \
               "\n !ahd [numero] Busca en ArkhamDB el mazo dado y lo muestra, tanto públicos como privados.\n" \
               "!ahj [nombre] ~[subtitulo]~ ([extra]) Busca cartas en ArkhamDB.\n" \
               "[extra] puede contener ser lo siguiente: '0-5' nivel de la carta, " \
               "'G/B/R/M/S/N' la clase de la carta, P para permanente, U para único, E para excepcional.\n" \
               "!ahm [nombre] ~[subtitulo]~ busca cartas de encuentros (lugares, actos, escenarios, etc.) que no " \
               "sean cartas de jugador estándar. \n"
    await ctx.send(response)
"""

@bot.command(name='hje')
async def look_for_player_card(ctx):
    skip = False
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = ah_player.copy()

    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext(c, sub_query)]

    if keyword_mode:
        r_cards = use_pc_keywords(r_cards, keyword_query)

    r_cards = search(query, r_cards)

    if len(r_cards) == 0 or len(r_cards) == len(ah_player):
        response = "No encontré ninguna carta"
        embed = False

    else:
        if r_cards[0]['name'] == "Debilidad básica aleatoria":
            skip = True
            response = "No encontré ninguna carta"
            embed = False

        elif r_cards[0]['type_code'] == "investigator":
            response = "¡Carta de Investigador Encontrada!"
            embed = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = "¡Carta de Enemigo Encontrada!"
            embed = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = "¡Carta de Traición Encontrada!"
            embed = format_treachery_card(r_cards[0])
        else:
            response = "¡Carta de Jugador Encontrada!"
            embed = format_player_card(r_cards[0])

        if len(r_cards) > 1 and not skip:
            response += ""  # "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hde')
async def look_for_deck(ctx, code: str):
    deck = find_deck(code)
    if not deck:
        response = "Mazo no encontrado"
        await ctx.send(response)
    else:
        deck_info = format_deck_cards(deck, ah_all_cards)
        embed = format_deck(deck, deck_info)
        response = "¡Mazo Encontrado!"
        await ctx.send(response, embed=embed)


@bot.command(name='hme')
async def look_for_encounter(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = sorted(ah_encounter.copy())
    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext_ec(c, sub_query)]
    if keyword_mode:
        r_cards = use_ec_keywords(r_cards, keyword_query)

    r_cards = search(query, r_cards)

    if len(r_cards) == 0 or len(r_cards) == len(ah_encounter):
        response = "No encontré ninguna carta"
        embed = False
    else:
        if r_cards[0]['type_code'] == "investigator":
            response = "¡Carta de Investigador encontrada!"
            embed = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = "¡Carta de Enemigo encontrada!"
            embed = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = "¡Carta de Traición encontrada!"
            embed = format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            response = "¡Carta de Acto encontrada!"
            embed = format_act_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            response = "¡Carta de Plan encontrada!"
            embed = format_agenda_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            response = "¡Carta de Lugar encontrada!"
            embed = format_location_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            response = "¡Carta de Escenario encontrada!"
            embed = format_scenario_card(r_cards[0])
        else:
            response = "¡Carta de Jugador encontrada!"
            embed = format_player_card(r_cards[0])

        if len(r_cards) > 1:
            response += ""  # "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hue')
async def look_for_upgrades(ctx):
    query = ctx.message.content.split()[1:]
    if len(query) >= 2:
        deck1 = find_deck(query[0])
        deck2 = find_deck(query[1])
        if not deck1 or deck2:
            response = "No encontre uno de los mazos."
            await ctx.send(response)
        else:
            info = check_upgrade_rules(deck1, deck2, ah_player)
            response = "¡Encontré una Mejora!"
            embed = format_upgraded_deck(deck1, info)
            await ctx.send(response, embed=embed)

    elif len(query) == 1:
        deck1 = find_deck(query[0])
        deck2 = find_former_deck(query[0])
        if not deck1:
            response = "No encontré el mazo."
            ctx.send(response)
        elif not deck2:
            response = "El Mazo dado no contiene una mejora."
            ctx.send(response)
        else:
            info = check_upgrade_rules(deck1, deck2, ah_player)
            response = "¡Encontré una Mejora!"
            embed = format_upgraded_deck(deck1, info)
            await ctx.send(response, embed=embed)

    else:
        response = "Uso de !ahu [numero] [numero] o bien !ahu [numero]"
        await ctx.send(response)


bot.run(TOKEN)
