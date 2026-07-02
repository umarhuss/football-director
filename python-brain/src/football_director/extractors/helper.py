import math

# Pass helper function to update the pass count for player
def successful_pass_check(pass_event: dict):
    if 'outcome' not in pass_event['pass']:
        return 1
    else:
        return 0

# Helper to calc the average carry distance
def avg_carry_distance(start_location: list , end_location:list) -> float:
    # Assign the start and end variables
    x1, y1 = start_location
    x2, y2 = end_location

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


