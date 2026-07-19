from .helper import update_under_pressure, update_pct, update_avg

def extract_dispossessed_metrics(events:list)-> dict:
    player_dispossessed_metrics = {}

    for event in events:
        if event['type']['name'] == 'Dispossessed':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]

            if p_id not in player_dispossessed_metrics:
                total = 1
                dispossessed_up = update_under_pressure(event)

                dispossessed_interface = {
                    'id': p_id,
                    'name': event['player']['name'],
                    'total_dispossessed': total,
                    'dispossessed_under_pressure':dispossessed_up,
                    'dispossessed_under_pressure_pct':update_pct(total,dispossessed_up),
                    'avg_dispossessed_loc_x': loc_x,
                    'avg_dispossessed_loc_y': loc_y
                }

                player_dispossessed_metrics[p_id] = dispossessed_interface

            else:
                curr_player = player_dispossessed_metrics[p_id]

                curr_player['dispossessed_under_pressure'] += update_under_pressure(event)
                curr_player['avg_dispossessed_loc_x'] = update_avg(curr_player['avg_dispossessed_loc_x'], curr_player['total_dispossessed'], loc_x)
                curr_player['avg_dispossessed_loc_y'] = update_avg(curr_player['avg_dispossessed_loc_y'], curr_player['total_dispossessed'], loc_y)


                curr_player['total_dispossessed'] += 1
                curr_player['dispossessed_under_pressure_pct'] = update_pct(curr_player['total_dispossessed'], curr_player['dispossessed_under_pressure'])
    return player_dispossessed_metrics
