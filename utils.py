import re
import unidecode


def search(query, cards):
    r_cards = sorted([c for c in cards if hits_in_string(c['name'], query) > 0],
                     key=lambda card: -hits_in_string(card['name'], query))

    # Sales en los resultados aparte si estas igual de hits con las palabras
    r_cards = [c for c in r_cards if hits_in_string(c['name'], query) == hits_in_string(r_cards[0]['name'], query)]
    return r_cards


def use_keywords(cards, key_list):
    filtered_cards = cards
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if filter_by_level(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c['exceptional']]
        if char == "b":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'seeker']
        if char == "g":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'guardian']
        if char == "r":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'rogue']
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'survivor']
        if char == "m":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'mystic']
        if char == "n":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'neutral']
        if char == "u":
            filtered_cards = [c for c in filtered_cards if c['unique']]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['permanent']]

    return filtered_cards



def filter_by_level(card, lvl):
    if 'xp' in card:
        return card['xp'] == lvl
    else:
        return 0 == lvl


def filter_by_subtext(card, sub):
    if "subname" in card:
        return hits_in_string(card['subname'], sub) > 0
    else:
        return False


def find_and_extract(string, start_s, end_s):
    fst_occ = string.find(start_s) + 1
    snd_occ = string[fst_occ:].find(end_s)
    extract = string[fst_occ: fst_occ + snd_occ]
    base = string.replace("%s%s%s)" % (start_s, extract, end_s), "", 1)
    return base, extract


def hits_in_string(s1, s2):
    hits = 0
    for w1 in list(set(s1.lower().split())):
        for w2 in list(set(s2.lower().split())):
            w1_c = re.sub(r'[^a-z]', '', unidecode.unidecode(w1))
            w2_c = re.sub(r'[^a-z]', '', unidecode.unidecode(w2))
            if w1_c == w2_c:
                hits += 1
    return hits