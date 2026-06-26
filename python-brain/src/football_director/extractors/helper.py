# Pass helper function to update the pass count for player
def successful_pass_check(pass_event: dict):
    if 'outcome' not in pass_event['pass']:
        return 1
    else:
        return 0
