from .helper import (calculate_distance,update_avg,update_goals,update_shots_on_target,
                     update_open_play_shots,update_under_pressure)

def extract_shot_metrics(events:list)-> dict:
    # Temp ledger for the player metrics
    player_shot_metrics = {}

    # Find the shot events
    for event in events:
        if event['type']['name'] == 'Shot':
            # Get player id and name
            p_id = event['player']['id']
            p_name = event['player']['name']

            # Get the needed metrics for calculations
            start_shot_loc = event['location']
            end_shot_loc = event['shot']['end_location']
            shot_xg = event['shot']['statsbomb_xg']
            shot_distance = calculate_distance(start_shot_loc,end_shot_loc)

            # Check of the player is already in the ledger
            if p_id not in player_shot_metrics:
                # Create the entry
                shot_interface = {
                    'player_id': p_id,
                    'player_name': p_name,
                    'total_shots': 1,
                    'goals': update_goals(event),
                    'shots_on_target': update_shots_on_target(event),
                    'avg_xg': shot_xg,
                    'total_xg': shot_xg,
                    'open_play_shots': update_open_play_shots(event),
                    'avg_shot_distance': shot_distance,
                    'shots_under_pressure':update_under_pressure(event)
                }
                player_shot_metrics[p_id] = shot_interface
            else:
                # Setup
                current_player = player_shot_metrics[p_id]
                curr_avg_xg = current_player['avg_xg']
                curr_shots_count = current_player['total_shots']
                curr_avg_distance = current_player['avg_shot_distance']

                # update the already existing entry
                current_player['goals'] += update_goals(event)
                current_player['shots_on_target'] += update_shots_on_target(event)

                current_player['avg_xg'] = update_avg(curr_avg_xg,curr_shots_count,shot_xg)
                current_player['total_xg'] += shot_xg
                current_player['open_play_shots'] += update_open_play_shots(event)
                current_player['avg_shot_distance'] = update_avg(curr_avg_distance,curr_shots_count,shot_distance)
                current_player['shots_under_pressure'] += update_under_pressure(event)


                current_player['total_shots'] += 1

    return player_shot_metrics
