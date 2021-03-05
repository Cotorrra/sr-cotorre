

def format_text(text):
    text_format = {"[free]": "<:Libre:789610643262799913>",
                   "[fast]": "<:Libre:789610643262799913>",
                   "[elder_sign]": "<:arcano:799004602183843851>",
                   "[willpower]": "<:Voluntad:789619119704113173>",
                   "[combat]": "<:Combate:789619139403972639>",
                   "[intellect]": "<:Intelecto:789619129082576966>",
                   "[agility]": "<:Agilidad:789619149730218044>",
                   "[action]": "<:Accion:789610653912399891>",
                   "[reaction]": "<:Reaccion:789610628339073075>",
                   "[bless]": "<:bendicion:799051903816171550>",
                   "[curse]": "<:maldicion:799050838928654347>",
                   "[wild]": "<:Comodin:789619157657583636>",
                   "[skull]": "<:calavera:799059800276336721>",
                   "[cultist]": "<:sectario:799004435762249729>",
                   "[tablet]": "<:tablilla:799004747687526410>",
                   "[elder_thing]": "<:primigenio:799059800230461441>",
                   "[auto_fail]": "<:fallo:799004322796797953>",
                   "[mystic]": "<:Mistico:786679149196476467>",
                   "[seeker]": "<:Buscador:786679131768225823>",
                   "[guardian]": "<:Guardian:786679100273852457>",
                   "[rogue]": "<:Rebelde:786679171257991199>",
                   "[survivor]": "<:Superviviente:786679182284947517>",
                   "[neutral]": "<:Neutral:786679389303603221>",
                   "[mythos]": "<:encuentro:808047457971470388>",
                   "[health]": "<:Salud:808821841413668904>",
                   "[sanity]": "<:Cordura:808821830608617493>",
                   "[per_investigator]": "<:Porinvestigador:789610613650489434>",
                   "[doom]": "<:perdicion:801160341886468138>",
                   "[clues]": "<:pista:801161173864808548>",
                   "</b>": "**",
                   "<b>": "**",
                   "<em>": "_",
                   "</em>": "_",
                   "<i>": "_",
                   "</i>": "_",
                   "<u>": "__",
                   "</u>": "__",
                   "[[": "***",
                   "]]": "***",
                   "<cite>": "\n— ",
                   "</cite>": "",
                   }

    for key, value in text_format.items():
        text = text.replace(key, value)
    return text


def format_set(c):
    text = "%s #%s" % (c['pack_name'], str(c['position']))
    if "encounter_code" in c:
        text += ": %s #%s" % (c['encounter_name'], str(c['encounter_position']))
        if c['quantity'] > 1:
            text += "-%s" % str(c['encounter_position'] + c['quantity'] - 1)
    text += "."
    return text


def format_card_text(c, tag="text"):
    formating = {"\n": "\n> "}
    text = format_text(c[tag]) if tag in c else ""
    for key, value in formating.items():
        text = text.replace(key, value)
    return text


def format_victory(c):
    if "victory" in c:
        return "> **Victoria %s.**\n" % c['victory']
    else:
        return ""


def format_vengeance(c):
    if "vengeance" in c:
        return "> **Venganza %s.**\n" % c['vengeance']
    else:
        return ""


def format_number(n):
    if int(n) == -2:
        return "X"
    else:
        return str(n)


def format_faction(c):
    if 'faction2_code' in c:
        return format_text("[%s]/[%s]" % (c['faction_code'], c['faction2_code']))
    else:
        return format_text("[%s]" % c['faction_code'])


faction_order = {
    "guardian": "0",
    "seeker": "1",
    "rogue": "2",
    "mystic": "3",
    "survivor": "4",
    "neutral": "5",
    "mythos": "6",
}


def set_thumbnail_image(c, embed, back=False):
    if "imagesrc" in c:
        if back:
            if "backimagesrc" in c:
                embed.set_thumbnail(url="https://arkhamdb.com%s" % c["backimagesrc"])
            else:
                embed.set_thumbnail(url="https://arkhamdb.com%s" % c["imagesrc"])
        else:
            embed.set_thumbnail(url="https://arkhamdb.com%s" % c["imagesrc"])


def format_illustrator(c):
    return "🖌 %s" % c['illustrator']


def format_name(c):
    return "*%s" % c['name'] if c['is_unique'] else "%s" % c['name']


def format_subtext(c):
    return ": _%s_" % c['subname'] if 'subname' in c else ""


def color_picker(c):
    colors = {
        "survivor": 0xcc3038,
        "rogue": 0x107116,
        "guardian": 0x2b80c5,
        "mystic": 0x4331b9,
        "seeker": 0xec8426,
        "neutral": 0x606060,
        "mythos": 0x000000,
    }
    return colors[c['faction_code']]

