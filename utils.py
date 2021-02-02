import re
import unidecode

# def search(query, ):


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