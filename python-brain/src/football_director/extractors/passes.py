from .helper import successful_pass_check

def extract_pass_metrics(events:list) -> dict:
    # Temp ledger for the pass metrics
    player_pass_metrics = {}

    # Loop through the json event data
    for event in events:
        # Find the pass event
        if event['type']['name'] == 'Pass':
            p_id = event['player']['id']
        # Check if there is anything in player pass metrics
            if p_id not in player_pass_metrics:

                player_passes = {
                    'player_id': p_id,
                    'name': event['player']['name'],
                    'total_passes': 1,
                    'successful_passes': successful_pass_check(event),
                    'avg_pass_length': event['pass']['length'],
                    'avg_pass_angle': event['pass']['angle']
                }

                player_pass_metrics[p_id] = player_passes

            else:
                # If player is already in the dict then update metrics
                # Go to that entry
                current_player = player_pass_metrics[p_id]
                # record the previous count fo calculations later
                previous_pass_total = current_player['total_passes']
                current_player['total_passes'] += 1
                # Go into the event find the successful and unsuccessful ones
                current_player['successful_passes'] += successful_pass_check(event)

                # Calculate the average pass len
                # Multiply the avg by the old count to get sum
                prev_avg_sum = current_player['avg_pass_length'] * previous_pass_total
                # Add new length to the prev sum
                curr_avg_sum = prev_avg_sum + event['pass']['length']
                # Update the average
                current_player['avg_pass_length']= curr_avg_sum / current_player['total_passes']

                # Calc the average pass angle same formula as above
                prev_angle_sum = current_player['avg_pass_angle'] * previous_pass_total
                curr_angle_sum = prev_angle_sum + event['pass']['angle']
                current_player['avg_pass_angle'] = curr_angle_sum / current_player['total_passes']


    return player_pass_metrics



