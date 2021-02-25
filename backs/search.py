from backs.formating import format_general_card_b, format_location_card_b, format_inv_card_b
from e_cards.formating import format_scenario_card
from p_cards.formating import format_player_card


def resolve_back_search(r_cards):
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

    return response, embed
