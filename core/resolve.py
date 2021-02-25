from e_cards.formating import format_enemy_card, format_treachery_card, format_act_card_f, format_agenda_card_f, \
    format_location_card_f, format_scenario_card
from p_cards.formating import format_inv_card_f, format_player_card


def resolve_search(r_cards):
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

    return response, embed