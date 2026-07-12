from .helper import update_avg,successful_interceptions,update_pct


def extract_interception_metrics(events:list)-> dict:
    player_interception_metrics = {}

    for event in events:
        if event['type']['name'] == 'Interception':
            p_id = event['player']['id']
            p_name = event['player']['name']

            # locations
            loc_x = event['location'][0]
            loc_y = event['location'][1]

            # Calc successful interceptions
            successful = successful_interceptions(event)

            if p_id not in player_interception_metrics:
                interception_interface = {
                    'id': p_id,
                    'name': p_name,
                    'total_interceptions': 1,
                    'successful_interceptions': successful,
                    'avg_interception_loc_x': loc_x,
                    'avg_interception_loc_y': loc_y,
                    'interception_success_pct': update_pct(1,successful)
                }

                player_interception_metrics[p_id] = interception_interface
            else:
                current_player = player_interception_metrics[p_id]
                current_player['successful_interceptions'] += successful

                # Update avg
                curr_avg_x = current_player['avg_interception_loc_x']
                curr_avg_y = current_player['avg_interception_loc_y']
                curr_count = current_player['total_interceptions']

                # Update the loc metrics
                current_player['avg_interception_loc_x'] = update_avg(curr_avg_x, curr_count, loc_x)
                current_player['avg_interception_loc_y'] = update_avg(curr_avg_y, curr_count, loc_y)


                # Update total count for pct
                current_player['total_interceptions'] += 1
                current_player['interception_success_pct'] = update_pct(current_player['total_interceptions'],current_player['successful_interceptions'])


    return player_interception_metrics
