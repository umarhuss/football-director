from .helper import update_avg

def extract_block_metrics(events:list)-> dict:
    player_block_metrics = {}

    for event in events:
        if event['type']['name'] == 'Block':
            p_id = event['player']['id']
            loc_x = event['location'][0]
            loc_y = event['location'][1]


            if p_id not in player_block_metrics:
                total_count = 1
                block_interface = {
                    'id': p_id,
                    'name': event['player']['name'],
                    'total_blocks': total_count,
                    'avg_block_loc_x': loc_x,
                    'avg_block_loc_y': loc_y
                }

                player_block_metrics[p_id] = block_interface

            else:
                curr_player = player_block_metrics[p_id]
                curr_x_avg = curr_player['avg_block_loc_x']
                curr_y_avg = curr_player['avg_block_loc_y']
                curr_total = curr_player['total_blocks']

                curr_player['avg_block_loc_x'] = update_avg(curr_x_avg,curr_total,loc_x)
                curr_player['avg_block_loc_y'] = update_avg(curr_y_avg,curr_total,loc_y)

                curr_player['total_blocks'] += 1
                
    return player_block_metrics
