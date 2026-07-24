from .helper import penalty_won_check,card_check, pen_rate, card_rate, update_avg, offensive_foul_check

def extract_fouls_committed_metrics(events:list)-> dict:
    player_fouls_committed_metrics = {}

    for event in events:
        if event['type']['name'] == 'Foul Committed':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]


            if p_id not in player_fouls_committed_metrics:
                total = 1
                pen_total = penalty_won_check(event,'Foul Committed')
                y_card_count = card_check(event, 'Yellow Card')
                r_card_count = card_check(event, 'Red Card')
                sec_y_count = card_check(event, 'Second Yellow')

                fouls_committed_interface = {
                        'player_id': p_id,
                        'player_name': event['player']['name'],
                        'total_fouls_committed': total,
                        'penalties_conceded': pen_total,
                        'yellow_cards': y_card_count,
                        'red_cards': r_card_count,
                        'offensive_fouls': offensive_foul_check(event),
                        'second_yellows': sec_y_count,
                        'card_rate': card_rate(total,y_card_count,r_card_count,sec_y_count),
                        'penalty_rate': pen_rate(total,pen_total),
                        'avg_foul_committed_loc_x':loc_x,
                        'avg_foul_committed_loc_y':loc_y,
                }

                player_fouls_committed_metrics[p_id] = fouls_committed_interface

            else:
                curr_player = player_fouls_committed_metrics[p_id]

                curr_player['penalties_conceded'] += penalty_won_check(event,'Foul Committed')
                curr_player['yellow_cards'] += card_check(event, 'Yellow Card')
                curr_player['red_cards'] += card_check(event, 'Red Card')
                curr_player['second_yellows']+= card_check(event, 'Second Yellow')
                curr_player['offensive_fouls'] += offensive_foul_check(event)

                curr_player['avg_foul_committed_loc_x'] = update_avg(curr_player['avg_foul_committed_loc_x'], curr_player['total_fouls_committed'], loc_x)
                curr_player['avg_foul_committed_loc_y'] = update_avg(curr_player['avg_foul_committed_loc_y'], curr_player['total_fouls_committed'], loc_y)

                curr_player['total_fouls_committed'] += 1

                total = curr_player['total_fouls_committed']
                yellow_count = curr_player['yellow_cards']
                red_count = curr_player['red_cards']
                s_yellow_count = curr_player['second_yellows']
                pen_total = curr_player['penalties_conceded']

                curr_player['card_rate'] = card_rate(total, yellow_count,red_count, s_yellow_count)
                curr_player['penalty_rate'] = pen_rate(total, pen_total)

    return player_fouls_committed_metrics

