from .helper import calculate_distance,update_avg,progressive_carries,update_under_pressure

def extract_carry_metrics(events:list) -> dict:
    # Temporary ledger for the player carry metrics
    player_carries_metrics = {}

    # loop through event finding the 'Carry' key word
    for event in events:
        if  event['type']['name'] == 'Carry':
            p_id = event['player']['id']

            # Global  metrics
            start_location = event['location']
            end_location = event['carry']['end_location']
            carry_distance = calculate_distance(start_location, end_location)



            # If player id not in the metrics dict create a entry and insert
            if p_id not in player_carries_metrics:

                carry_interface = {
                    'player_id': p_id,
                    'player name': event['player']['name'],
                    'total_carries': 1,
                    'avg_carry_distance':carry_distance,
                    'progressive_carries': progressive_carries(start_location,end_location),
                    'avg_carry_duration': event['duration'],
                    'carries_under_pressure': update_under_pressure(event),
                    'carries_under_pressure_pct': 0

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
                carry_duration = event['duration']


                current_player['avg_carry_distance'] = update_avg(curr_carry_avg,curr_count,carry_distance)
                current_player['progressive_carries'] += progressive_carries(start_location,end_location)
                current_player['avg_carry_duration'] = update_avg(curr_duration_avg,curr_count,carry_duration)
                # This must go last as i need the current count for the avg calc
                current_player['total_carries'] += 1

    return player_carries_metrics
