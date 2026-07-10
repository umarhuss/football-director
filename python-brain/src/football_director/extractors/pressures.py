from .helper import update_avg

def extract_pressure_metrics(events:list)-> dict:
    player_pressure_metrics = {}

    for event in events:
        if event['type']['name'] == 'Pressure':
            p_id = event['player']['id']
            pressure_duration = event['duration']
            # The x and y tell different things x = high or low and
            # the y = what channels PCA could find this useful.
            pressure_loc_x = event['location'][0]
            pressure_loc_y = event['location'][1]

            if p_id not in player_pressure_metrics:
                pressure_interface ={
                    'player_id': p_id,
                    'player_name': event['player']['name'],
                    'total_pressures': 1,
                    'avg_pressure_duration': pressure_duration,
                    'avg_pressure_loc_x': pressure_loc_x,
                    'avg_pressure_loc_y': pressure_loc_y
                }

                player_pressure_metrics[p_id] = pressure_interface
            else:
                curr_player = player_pressure_metrics[p_id]
                curr_avg_duration = curr_player['avg_pressure_duration']
                curr_total = curr_player['total_pressures']

                curr_avg_pressure_loc_x = curr_player['avg_pressure_loc_x']
                curr_avg_pressure_loc_y = curr_player['avg_pressure_loc_y']

                curr_player['avg_pressure_duration'] = update_avg(curr_avg_duration,curr_total,pressure_duration)
                curr_player['avg_pressure_loc_x'] = update_avg(curr_avg_pressure_loc_x, curr_total,pressure_loc_x)
                curr_player['avg_pressure_loc_y'] = update_avg(curr_avg_pressure_loc_y, curr_total,pressure_loc_y)

                curr_player['total_pressures'] += 1

    return player_pressure_metrics

