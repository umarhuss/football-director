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

def update_pct(curr_total: int, curr_count:int):
    if curr_total > 0:
        return (curr_count/curr_total) * 100
    else:
        return 0

#  Interceptions

def successful_interceptions(event:dict) -> int:
    success_set = {'Success In Play', 'Won'}

    outcome = event['interception'].get('outcome',{}).get('name',{})
    if outcome in success_set:
        return 1
    else:
        return 0

# Duels

def check_outcome(event: dict, event_type: str, success_set: set) -> int:
    outcome = event[event_type].get('outcome', {}).get('name', '')
    return 1 if outcome in success_set else 0

# Fouls won
def penalty_won_check(event:dict, foul_type:str)-> int:
    if foul_type == 'Foul Won':
        return 1 if event.get('foul_won',{}).get('penalty') == True else 0
    else:
        return 1 if event.get('foul_committed',{}).get('penalty') == True else 0

def defensive_foul_check(event:dict) -> int:
    return 1 if event.get('foul_won',{}).get('defensive') else 0




# Fouls committed
def card_check(event: dict, card_type: str) -> int:
    card = event.get('foul_committed', {}).get('card', {}).get('name', '')
    return 1 if card == card_type else 0

def card_rate(curr_total: int, y_total: int, r_total: int, s_yellow_total: int) -> float:
    card_total = y_total + r_total + s_yellow_total
    if curr_total > 0:
        return (card_total / curr_total) * 100
    return 0.0

def pen_rate(curr_total:int, pen_total:int) -> float:
    if curr_total > 0:
        return (pen_total / curr_total) * 100

    return 0.0

def offensive_foul_check(event: dict) -> int:
    return 1 if event.get('foul_committed', {}).get('offensive') else 0

# Miscontrol

def miscontrol_out(event:dict)-> int:
    return 1 if event.get('out',{}) else 0
