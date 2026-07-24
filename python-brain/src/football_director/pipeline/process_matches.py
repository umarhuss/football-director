from pathlib import Path
import json
from ..extractors import (
    extract_pass_metrics,
    extract_carry_metrics,
    extract_shot_metrics,
    extract_pressure_metrics,
    extract_interception_metrics,
    extract_clearance_metrics,
    extract_block_metrics,
    extract_ball_recovery_metrics,
    extract_duel_metrics,
    extract_fouls_won_metrics,
    extract_fouls_committed_metrics,
    extract_miscontrol_metrics,
    extract_dispossessed_metrics
)
import traceback

def process_matches(matches_path:Path, events_path:Path) -> dict:
    player_profile = {}

    for comp_folder in matches_path.iterdir():
        comp_id = comp_folder.name
        for match in comp_folder.iterdir():
            if match.is_file():
                season_id = match.name
                with open(f'{matches_path}/{comp_id}/{season_id}') as curr_match:
                    matches = json.load(curr_match)
                    for i in matches:
                        match_id = i['match_id']

                        # Go the events folder now
                        with open(f'{events_path}/{match_id}.json') as c:
                            curr_event = json.load(c)

                        # Initialise extractors
                        pass_metrics = {}
                        carry_metrics = {}
                        shot_metrics = {}
                        pressure_metrics = {}
                        interception_metrics = {}
                        clearance_metrics = {}
                        block_metrics = {}
                        ball_recovery_metrics = {}
                        duel_metrics = {}
                        fouls_won_metrics = {}
                        fouls_committed_metrics = {}
                        miscontrol_metrics = {}
                        dispossessed_metrics = {}

                        # Run extractors
                        try:
                            pass_metrics = extract_pass_metrics(curr_event)
                            carry_metrics = extract_carry_metrics(curr_event)
                            shot_metrics = extract_shot_metrics(curr_event)
                            pressure_metrics = extract_pressure_metrics(curr_event)
                            interception_metrics = extract_interception_metrics(curr_event)
                            clearance_metrics = extract_clearance_metrics(curr_event)
                            block_metrics = extract_block_metrics(curr_event)
                            ball_recovery_metrics = extract_ball_recovery_metrics(curr_event)
                            duel_metrics = extract_duel_metrics(curr_event)
                            fouls_won_metrics = extract_fouls_won_metrics(curr_event)
                            fouls_committed_metrics = extract_fouls_committed_metrics(curr_event)
                            miscontrol_metrics = extract_miscontrol_metrics(curr_event)
                            dispossessed_metrics = extract_dispossessed_metrics(curr_event)

                            # Make a list of the outputs to loop though

                            extractor_outputs = [
                            pass_metrics, carry_metrics, shot_metrics, pressure_metrics,
                            interception_metrics,clearance_metrics,block_metrics,ball_recovery_metrics,
                            duel_metrics,fouls_won_metrics,fouls_committed_metrics,miscontrol_metrics,
                            dispossessed_metrics
                            ]

                            # Merge the player ids
                            for output in extractor_outputs:
                                for player_id, metrics in output.items():
                                    if player_id not in player_profile:
                                        player_profile[player_id] = {}
                                    player_profile[player_id].update(metrics)

                        except Exception as e:
                            print(f"Error processing match {match_id}:")
                            traceback.print_exc()
                            continue


    return player_profile
