from .helper import avg_carry_distance,update_avg,progressive_carries

def extract_carry_metrics(events:list) -> dict:
    # Temporary ledger for the player carry metrics
    player_carries_metrics = {}

    # loop through event finding the 'Carry' key word
    for event in events:
        if  event['type']['name'] == 'Carry':
            p_id = event['player']['id']

            # Location metrics
            start_location = event['location']
            end_location = event['carry']['end_location']

            # If player id not in the metrics dict create a entry and insert
            if p_id not in player_carries_metrics:

                carry_interface = {
                    'player_id': p_id,
                    'player name': event['player']['name'],
                    'total_carries': 1,
                    'avg_carry_distance':avg_carry_distance(start_location, end_location),
                    'progressive_carries': progressive_carries(start_location,end_location),
                    'avg_carry_duration': event['duration']

                }
                # Save to the player metrics
                player_carries_metrics[p_id] = carry_interface

            # else update that players metrics
            else:
                # Get player information
                current_player = player_carries_metrics[p_id]
                curr_carry_avg = current_player['avg_carry_distance']
                curr_duration_avg = current_player['avg_carry_duration']
                curr_count = current_player['total_carries']
                carry_distance = avg_carry_distance(start_location, end_location)
                carry_duration = event['duration']


                current_player['avg_carry_distance'] = update_avg(curr_carry_avg,curr_count,carry_distance)
                current_player['progressive_carries'] += progressive_carries(start_location,end_location)
                current_player['avg_carry_duration'] = update_avg(curr_duration_avg,curr_count,carry_duration)
                # This must go last as i need the current count for the avg calc
                current_player['total_carries'] += 1

    return player_carries_metrics
