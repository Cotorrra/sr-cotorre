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

raw_text = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')

    # await bot.change_presence(activity=discord.Game(name="\"Arkham Horror LCG\""))

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Eric Zann'))


# @bot.command(name='t', help='Busca el registro de tabú de la carta pedida')
# async def look_for_taboo(ctx):

@bot.command(name='hhelp')
async def send_help(ctx):
    res = "¿Necesitas ayuda?: \n" \
          "" \
          "\n- !ahj [nombre] ~[subtitulo]~ ([extra]): Busca cartas en ArkhamDB.\n" \
          "[extra] puede contener ser lo siguiente: '0-5' nivel de la carta, " \
          "'G/B/R/M/S/N' la clase de la carta, P para permanente, U para único, E para excepcional, C para característica.\n" \
          "Por ejemplo: \"!ahj Whisky (3S)\" devolverá el Whisky de Mosto Ácido de Supervivente de nivel 3. \n" \
          "\n- !ahm [nombre] ~[subtitulo]~: Busca cartas de encuentros (lugares, actos, escenarios, etc.) que no " \
          "sean cartas de jugador estándar. (¡Spoilers!) \n" \
          "\n- !ahback [nombre] ~[subtitulo]~ ([extra]): Muestra la parte de atrás de ciertas cartas que lo permiten. \n" \
          "El [extra] de !ahback y !ahm permiten buscar cartas por tipo: S: Escenario, A: Acto, P: Plan, T: Traicion, " \
          "E: Enemigo, L: Lugar y J: Por cartas de jugador de encuentros." \
          "\n- !ahd [numero]: Busca en ArkhamDB el mazo dado y lo muestra, tanto público como privado.\n" \
          "\n- !ahu [numero] [numero] Busca en ArkhamDB ambos mazos y muestra las mejoras realizadas en los mazos." \
          "Si mejoraste el mazo con ArkhamDB puedes también entregarle sólo el número del mazo más reciente." \
          ""
    await ctx.send(res)


@bot.command(name='hback')
async def look_for_card_back(ctx):
    skip = False
    query = ' '.join(ctx.message.content.split()[1:])

    f_cards = [c for c in ah_all_cards if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)

    if r_cards:
        if r_cards[0]['type_code'] == "investigator":
            response = "¡Carta de Investigador encontrada!"
            embed = format_inv_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = "¡Carta de Enemigo encontrada!"
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = "¡Carta de Traición encontrada!"
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            response = "¡Carta de Acto encontrada!"
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            response = "¡Carta de Plan encontrada!"
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            response = "¡Carta de Lugar encontrada!"
            embed = format_location_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            response = "¡Carta de Escenario encontrada!"
            embed = format_scenario_card(r_cards[0])
        else:
            response = "¡Carta de Jugador encontrada!"
            embed = format_player_card(r_cards[0])
    else:
        response = "No encontré ninguna carta"
        embed = False

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hj')
async def look_for_player_card(ctx):
    skip = False
    query = ' '.join(ctx.message.content.split()[1:])

    r_cards = card_search(query, ah_player, use_pc_keywords)

    if r_cards:
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

    else:
        response = "No encontré ninguna carta"
        embed = False

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hd')
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


@bot.command(name='hm')
async def look_for_encounter(ctx):
    query = ' '.join(ctx.message.content.split()[1:])

    r_cards = card_search(query, ah_encounter, use_ec_keywords)

    if r_cards:
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
            embed = format_location_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            response = "¡Carta de Escenario encontrada!"
            embed = format_scenario_card(r_cards[0])
        else:
            response = "¡Carta de Jugador encontrada!"
            embed = format_player_card(r_cards[0])

        if len(r_cards) > 1:
            response += ""  # "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])
    else:
        response = "No encontré ninguna carta"
        embed = False

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hu')
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
            info = check_upgrade_rules(deck2, deck1, ah_player)
            response = "¡Encontré una Mejora!"
            embed = format_upgraded_deck(deck1, info)
            await ctx.send(response, embed=embed)

    else:
        response = "Uso de !ahu [numero] [numero] o bien !ahu [numero]"
        await ctx.send(response)


bot.run(TOKEN)
