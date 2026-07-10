import math

# Pass helper function to update the pass count for player
def successful_pass_check(pass_event: dict):
    if 'outcome' not in pass_event['pass']:
        return 1
    else:
        return 0

# Helper to calc the average distance
def calculate_distance(start_location: list , end_location:list) -> float:
    # Assign the start and end variables
    x1, y1 = start_location[0], start_location[1]
    x2, y2 = end_location[0], end_location[1]


    # return the distance carried
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)


# Update average function
def update_avg(curr_average:float, curr_count:int, new_metric: float) -> float:
    # Calc previous average
    prev_avg_sum = curr_average * curr_count
    # Add the new metric to the sum
    new_avg_sum = prev_avg_sum + new_metric

    # Return the new average with updated count
    return new_avg_sum / (curr_count + 1)


# Progressive carries calc
def progressive_carries(start_loc: list, end_loc:list) -> int:
    # Check if the carry was progressive
    if end_loc[0] > start_loc[0] and end_loc[0] - start_loc[0] >= 10:
        return 1
    else:
        return 0


# Update shots metrics
def update_goals(event: dict) -> int:
    outcome = event['shot'].get('outcome', {}).get('name', '')
    return 1 if outcome == 'Goal' else 0

def update_shots_on_target(event: dict) -> int:
    outcome = event['shot'].get('outcome', {}).get('name', '')
    return 1 if outcome in {'Goal', 'Saved'} else 0

def update_open_play_shots(event: dict) -> int:
    shot_type = event['shot'].get('type', {}).get('name', '')
    return 1 if shot_type == 'Open Play' else 0

def update_under_pressure(event:dict) -> int:
    return 1 if event.get('under_pressure') else 0

def update_under_pressure_pct(curr_total: int, curr_pressure_count:int):
    if curr_total > 0:
        return (curr_pressure_count/curr_total) * 100
    else:
        return 0

