from .helper import penalty_won_check, update_pct, defensive_foul_check,update_avg

def extract_fouls_won_metrics(events:list)-> dict:
    player_fouls_won_metrics = {}

    for event in events:
        if event['type']['name'] == 'Foul Won':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]

            if p_id not in player_fouls_won_metrics:
                total = 1
                pen_won = penalty_won_check(event,'Foul Won')
                fouls_won_interface = {
                    'id': p_id,
                    'name': event['player']['name'],
                    'total_fouls_won': total,
                    'penalties_won':pen_won,
                    'penalty_won_rate':update_pct(total,pen_won),
                    'defensive_fouls_won':defensive_foul_check(event),
                    'free_kicks_won': total - pen_won,
                    'avg_foul_won_loc_x':loc_x,
                    'avg_foul_won_loc_y':loc_y,
                }

                player_fouls_won_metrics[p_id] = fouls_won_interface
            else:
                curr_player = player_fouls_won_metrics[p_id]


                curr_player['penalties_won'] += penalty_won_check(event,'Foul Won')
                curr_player['defensive_fouls_won'] += defensive_foul_check(event)

                curr_player['avg_foul_won_loc_x'] = update_avg(curr_player['avg_foul_won_loc_x'], curr_player['total_fouls_won'], loc_x)
                curr_player['avg_foul_won_loc_y'] = update_avg(curr_player['avg_foul_won_loc_y'], curr_player['total_fouls_won'], loc_y)

                curr_player['total_fouls_won'] += 1
                curr_player['free_kicks_won'] = curr_player['total_fouls_won'] - curr_player['penalties_won']
                curr_player['penalty_won_rate'] = update_pct(curr_player['total_fouls_won'], curr_player['penalties_won'])


    return player_fouls_won_metrics
