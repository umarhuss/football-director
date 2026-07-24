from .helper import update_avg

def extract_ball_recovery_metrics(events:list)-> dict:
    player_ball_recovery_metrics = {}

    for event in events:
        if event['type']['name'] == 'Ball Recovery':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]


            if p_id not in player_ball_recovery_metrics:
                ball_recovery_interface = {
                    'player_id': p_id,
                    'player_name': event['player']['name'],
                    'total_recovery': 1,
                    'avg_recovery_loc_x': loc_x,
                    'avg_recovery_loc_y': loc_y
                }

                player_ball_recovery_metrics[p_id] = ball_recovery_interface

            else:
                curr_player = player_ball_recovery_metrics[p_id]
                curr_x_avg = curr_player['avg_recovery_loc_x']
                curr_y_avg = curr_player['avg_recovery_loc_y']
                curr_total = curr_player['total_recovery']

                curr_player['avg_recovery_loc_x'] = update_avg(curr_x_avg,curr_total,loc_x)
                curr_player['avg_recovery_loc_y'] = update_avg(curr_y_avg,curr_total,loc_y)

                curr_player['total_recovery'] += 1

    return player_ball_recovery_metrics
