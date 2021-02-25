from core.formating import *


def format_enemy_stats(c):
    formater = {"health": "[health] %s%s " % (format_number(c['health']) if "health" in c else "-",
                                              "[per_investigator]" if c[
                                                  "health_per_investigator"] else ""),
                "combat": "[combat] %s " % (format_number(c['enemy_fight']) if "enemy_fight" in c else "-"),
                "agility": "[agility] %s" % (format_number(c['enemy_evade']) if "enemy_evade" in c else "-")
                }

    return format_text("%(combat)s | %(health)s | %(agility)s\n" % formater)


def format_clues(c):
    if "clues" in c:
        clues = str(c['clues'])
        if c['clues_fixed'] or c['clues'] == 0:
            return format_text("[clues] %s" % clues)
        else:
            return format_text("[clues] %s [per_investigator]" % clues)
    else:
        return format_text("[clues] -")


def format_attack(c):
    formater = {
        "damage": "[health]" * c['enemy_damage'] if "enemy_damage" in c else "",
        "horror": "[sanity]" * c['enemy_horror'] if "enemy_horror" in c else "",
    }
    return format_text("%(damage)s%(horror)s" % formater)

