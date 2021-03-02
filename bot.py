import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from backs.search import resolve_back_search
from core.resolve import resolve_search
from core.search import card_search
from decks.formating import format_deck, format_deck_cards
from decks.search import search_for_upgrades, find_deck
from e_cards.search import use_ec_keywords
from p_cards.search import use_pc_keywords

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]

raw_text = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')

    # await bot.change_presence(activity=discord.Game(name="Mod de Parri"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Eric Zann'))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='tus Pensamientos'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='El Rey de Amarillo (Acto 2)'))


# @bot.command(name='t', help='Busca el registro de tabú de la carta pedida')
# async def look_for_taboo(ctx):

@bot.command(name='hhelp')
async def send_help(ctx):
    res = "¿Necesitas ayuda?: \n" \
          "" \
          "\n- !ahj [nombre] ~[subtitulo]~ ([extra]): Busca cartas en ArkhamDB.\n" \
          "[extra] puede contener ser lo siguiente: '0-5' nivel de la carta, " \
          "'G/B/R/M/S/N' la clase de la carta, P para permanente, U para único, E para excepcional, " \
          "C para característica.\n" \
          "Por ejemplo: \"!ahj Whisky (3S)\" devolverá el Whisky de Mosto Ácido de Supervivente de nivel 3. \n" \
          "\n- !ahm [nombre] ~[subtitulo]~: Busca cartas de encuentros (lugares, actos, escenarios, etc.) que no " \
          "sean cartas de jugador estándar. (¡Spoilers!) \n" \
          "\n- !ahback [nombre] ~[subtitulo]~ ([extra]): Muestra la parte de atrás de ciertas cartas que lo permiten." \
          "\n" \
          "El [extra] de !ahback y !ahm permiten buscar cartas por tipo: S: Escenario, A: Acto, P: Plan, T: Traicion," \
          "E: Enemigo, L: Lugar y J: Por cartas de jugador de encuentros." \
          "\n- !ahd [numero]: Busca en ArkhamDB el mazo dado y lo muestra, tanto público como privado.\n" \
          "\n- !ahu [numero] [numero] Busca en ArkhamDB ambos mazos y muestra las mejoras realizadas en los mazos." \
          "Si mejoraste el mazo con ArkhamDB puedes también entregarle sólo el número del mazo más reciente." \
          ""
    await ctx.send(res)


@bot.command(name='hback')
async def look_for_card_back(ctx):

    query = ' '.join(ctx.message.content.split()[1:])

    f_cards = [c for c in ah_all_cards if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)

    response, embed = resolve_back_search(r_cards)

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hj')
async def look_for_player_card(ctx):
    skip = False
    query = ' '.join(ctx.message.content.split()[1:])

    r_cards = card_search(query, ah_player, use_pc_keywords)

    response, embed = resolve_search(r_cards)

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
    response, embed = resolve_search(r_cards)

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hu')
async def look_for_upgrades(ctx):
    query = ctx.message.content.split()[1:]

    response, embed = search_for_upgrades(query, ah_player)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hw')
async def pick_weakness(ctx):
    query = ctx.message.content.split()[1:]

    response, embed = search_for_upgrades(query, ah_player)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)

bot.run(TOKEN)
