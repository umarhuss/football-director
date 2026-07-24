from .helper import update_under_pressure, update_pct, miscontrol_out, update_avg

def extract_miscontrol_metrics(events:list)-> dict:
    player_miscontrol_metrics = {}

    for event in events:
        if event['type']['name'] == 'Miscontrol':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]


            if p_id not in player_miscontrol_metrics:
                total = 1
                total_miscontrols_up = update_under_pressure(event)
                miscontrol_interface = {
                    'player_id': p_id,
                    'player_name': event['player']['name'],
                    'total_miscontrols': total,
                    'miscontrols_under_pressure': total_miscontrols_up,
                    'miscontrols_under_pressure_pct': update_pct(total, total_miscontrols_up),
                    'miscontrols_out': miscontrol_out(event),
                    'avg_miscontrol_loc_x': loc_x,
                    'avg_miscontrol_loc_y': loc_y
                }

                player_miscontrol_metrics[p_id] = miscontrol_interface

            else:
                curr_player = player_miscontrol_metrics[p_id]

                curr_player['miscontrols_under_pressure'] += update_under_pressure(event)
                curr_player['miscontrols_out'] += miscontrol_out(event)
                curr_player['avg_miscontrol_loc_x'] = update_avg(curr_player['avg_miscontrol_loc_x'], curr_player['total_miscontrols'], loc_x)
                curr_player['avg_miscontrol_loc_y'] = update_avg(curr_player['avg_miscontrol_loc_y'], curr_player['total_miscontrols'], loc_y)



                curr_player['total_miscontrols'] += 1
                curr_player['miscontrols_under_pressure_pct'] = update_pct(curr_player['total_miscontrols'],curr_player['miscontrols_under_pressure'])

    return player_miscontrol_metrics

