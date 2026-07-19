from .helper import update_pct, check_outcome, update_avg

def extract_duel_metrics(events:list)-> dict:
    player_duel_metrics = {}
    successful_outcomes = {'Success In Play', 'Won', 'Success Out'}
    unsuccessful_outcomes = {'Lost In Play','Lost Out'}

    for event in events:
        if event['type']['name'] == 'Duel':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]

            if p_id not in player_duel_metrics:
                total = 1
                wins = check_outcome(event,'duel',successful_outcomes)
                duels_with_outcomes = 1 if event['duel'].get('outcome') else 0
                duels_interface = {
                    'id': p_id,
                    'name': event['player']['name'],
                    'total_duels': total,
                    'duels_with_outcome': duels_with_outcomes,
                    'duels_won': wins,
                    'duels_lost': check_outcome(event,'duel',unsuccessful_outcomes),
                    'duel_win_pct': update_pct(duels_with_outcomes,wins),
                    'aerial_duels': 1 if event['duel']['type']['name'] == 'Aerial Lost' else 0,
                    'tackles':1 if event['duel']['type']['name'] == 'Tackle' else 0,
                    'avg_duel_loc_x': loc_x,
                    'avg_duel_loc_y': loc_y
                }

                player_duel_metrics[p_id] = duels_interface
            else:
                curr_player = player_duel_metrics[p_id]
                curr_loc_x = curr_player['avg_duel_loc_x']
                curr_loc_y = curr_player['avg_duel_loc_y']


                # Update the duels won/lost metrics
                curr_player['duels_won'] += check_outcome(event,'duel',successful_outcomes)
                curr_player['duels_lost'] += check_outcome(event,'duel',unsuccessful_outcomes)

                # Update types of duels
                curr_player['aerial_duels'] += 1 if event['duel']['type']['name'] == 'Aerial Lost' else 0
                curr_player['tackles'] += 1 if event['duel']['type']['name'] == 'Tackle' else 0

                # Update the avg loc
                curr_player['avg_duel_loc_x'] = update_avg(curr_loc_x,curr_player['total_duels'],loc_x)
                curr_player['avg_duel_loc_y'] = update_avg(curr_loc_y,curr_player['total_duels'],loc_y)

                # Update win pct after updating th total count
                curr_player['duels_with_outcome']+= 1 if event['duel'].get('outcome') else 0
                curr_player['total_duels'] += 1
                curr_player['duel_win_pct'] = update_pct(curr_player['duels_with_outcome'],curr_player['duels_won'])


    return player_duel_metrics
