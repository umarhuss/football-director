from .helper import update_avg, update_pct, update_under_pressure


def extract_clearance_metrics(events:list)-> dict:
    player_clearance_metrics = {}

    for event in events:
        if event['type']['name'] == 'Clearance':
            p_id = event['player']['id']
            p_name = event['player']['name']
            body_part = event.get('clearance',{}).get('body_part',{}).get('name', {'Other'})
            loc_x = event['location'][0]
            loc_y = event['location'][1]

            if p_id not in player_clearance_metrics:
                total_count = 1
                pressure_count = update_under_pressure(event)

                clearance_interface = {
                    'id': p_id,
                    'name':p_name,
                    'total_clearances': total_count,
                    'clearances_under_pressure': pressure_count,
                    'clearances_under_pressure_pct': update_pct(total_count,pressure_count),
                    'avg_clearance_loc_x': loc_x,
                    'avg_clearance_loc_y': loc_y,
                    'aerial_clearances': 1 if event.get('clearance', {}).get('aerial_won') else 0,
                    'headed_clearances': 1 if body_part == 'Head' else 0,
                    'left_foot_clearances': 1 if body_part == 'Left Foot' else 0,
                    'right_foot_clearances': 1 if body_part == 'Right Foot' else 0,
                    'other_clearances': 1 if body_part == 'Other' else 0
                }

                player_clearance_metrics[p_id] = clearance_interface
            else:
                curr_player = player_clearance_metrics[p_id]
                curr_total_count = curr_player['total_clearances']
                curr_pressure_count = curr_player['clearances_under_pressure']
                curr_avg_loc_x = curr_player['avg_clearance_loc_x']
                curr_avg_loc_y = curr_player['avg_clearance_loc_y']


                curr_player['clearances_under_pressure'] += update_under_pressure(event)
                curr_player['avg_clearance_loc_x'] = update_avg(curr_avg_loc_x,curr_total_count,loc_x)
                curr_player['avg_clearance_loc_y'] = update_avg(curr_avg_loc_y,curr_total_count,loc_y)


                curr_player['aerial_clearances']+= 1 if event.get('clearance', {}).get('aerial_won') else 0
                curr_player['headed_clearances']+= 1 if body_part == 'Head' else 0
                curr_player['left_foot_clearances'] += 1 if body_part == 'Left Foot' else 0
                curr_player['right_foot_clearances']+= 1 if body_part == 'Right Foot' else 0
                curr_player['other_clearances']+= 1 if body_part == 'Other' else 0

                # After total updated and pressure updated
                curr_player['total_clearances'] += 1
                curr_player['clearances_under_pressure_pct'] = update_pct(curr_player['total_clearances'],curr_player['clearances_under_pressure'])


    return player_clearance_metrics
