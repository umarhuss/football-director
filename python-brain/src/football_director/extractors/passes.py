from .helper import (successful_pass_check,update_avg,update_under_pressure,
                     update_pct)

def extract_pass_metrics(events:list) -> dict:
    # Temp ledger for the pass metrics
    player_pass_metrics = {}

    # In final version code to check the processed file table
    # in DB to for idempotency.

    # Loop through the json event data
    for event in events:
        # Find the pass event
        if event['type']['name'] == 'Pass':
            p_id = event['player']['id']

        # Check if there is anything in player pass metrics
            if p_id not in player_pass_metrics:
                passes_under_pressure = update_under_pressure(event)
                completion_under_pressure_pct = update_pct(1, passes_under_pressure)

                player_passes = {
                    'player_id': p_id,
                    'name': event['player']['name'],
                    'total_passes': 1,
                    'successful_passes': successful_pass_check(event),
                    'avg_pass_length': event['pass']['length'],
                    'avg_pass_angle': event['pass']['angle'],
                    'passes_under_pressure': passes_under_pressure,
                    'successful_passes_under_pressure': successful_pass_check(event) if update_under_pressure(event) else 0,
                    'pass_completion_under_pressure_pct': completion_under_pressure_pct
                }

                player_pass_metrics[p_id] = player_passes

            else:
                # If player is already in the dict then update metrics
                current_player = player_pass_metrics[p_id]
                pass_total = current_player['total_passes']

                # Current pass length metrics
                pass_len_avg = current_player['avg_pass_length']
                new_pass_len = event['pass']['length']

                # Current pass angle metrics
                curr_angle_avg = current_player['avg_pass_angle']
                new_pass_angle = event['pass']['angle']


                # Calculate the average pass length
                current_player['avg_pass_length'] = update_avg(pass_len_avg,pass_total,new_pass_len)
                # Calculate the average pass angle
                current_player['avg_pass_angle'] = update_avg(curr_angle_avg,pass_total,new_pass_angle)
                # Go into the event find the successful and unsuccessful ones
                current_player['successful_passes'] += successful_pass_check(event)
                # Update counts
                current_player['passes_under_pressure'] += update_under_pressure(event)
                current_player['successful_passes_under_pressure'] += successful_pass_check(event) if update_under_pressure(event) else 0
                # Update the pass completion pct
                current_player['pass_completion_under_pressure_pct'] = update_pct(
                current_player['passes_under_pressure'],
                current_player['successful_passes_under_pressure']
                )

                # Update the total pass count
                current_player['total_passes'] += 1

    return player_pass_metrics



