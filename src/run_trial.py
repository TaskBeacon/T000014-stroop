from psyflow import StimUnit
from functools import partial

def run_trial(
    win,
    kb,
    settings,
    condition: str,           # e.g., 'congruent_red'
    stim_bank: dict,
    trigger_runtime=None,
):
    """
    Runs a single trial of the Stroop task.

    Args:
        win: The PsychoPy window object.
        kb: The keyboard handler.
        settings: The task settings object.
        condition (str): A string defining the current trial's type,
                         e.g., "congruent_red".
        stim_bank: The stimulus bank containing all visual stimuli.
        trigger_runtime: The object responsible for sending EEG/fMRI triggers.

    Returns:
        dict: A dictionary containing all data recorded for this trial.
    """
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # --- 1. Determine trial properties from condition string ---
    stroop_type, color = condition.split('_')
    correct_response = settings.red_key if color == 'red' else settings.green_key
    stim_name = condition
    
    trial_data.update({
        "stroop_type": stroop_type,
        "color": color,
        "correct_response": correct_response
    })

    # --- 2. Fixation ---
    make_unit(unit_label='fixation') \
        .add_stim(stim_bank.get("fixation")) \
        .show(duration=settings.fixation_duration, onset_trigger=settings.triggers.get("fixation_onset")) \
        .to_dict(trial_data)

    # --- 3. Stroop Stimulus & Response ---
    stim_unit = make_unit(unit_label="stimulus") \
        .add_stim(stim_bank.get(stim_name))
    
    stim_unit.capture_response(
        keys=settings.key_list,
        correct_keys=correct_response,
        duration=settings.stim_duration,
        response_trigger={settings.red_key: settings.triggers.get("red_key_press"), settings.green_key: settings.triggers.get("green_key_press")},
        onset_trigger=settings.triggers.get(f"{stroop_type}_stim_onset"),
        terminate_on_response=True
    )
    stim_unit.to_dict(trial_data)

    # --- 4. Determine Accuracy and Feedback ---
    response = stim_unit.get_state("response", False)
    hit = stim_unit.get_state("hit", False)

    if response and hit:
        feedback_stim = stim_bank.get("correct_feedback")
        feedback_trigger = settings.triggers.get("feedback_correct_response")
    elif response and not hit:
        feedback_stim = stim_bank.get("incorrect_feedback")
        feedback_trigger = settings.triggers.get("feedback_incorrect_response")
    else:
        feedback_stim = stim_bank.get("no_response_feedback")
        feedback_trigger = settings.triggers.get("feedback_no_response")

    # --- 5. Feedback ---
    make_unit(unit_label="feedback") \
        .add_stim(feedback_stim) \
        .show(duration=settings.feedback_duration, onset_trigger=feedback_trigger) \
        .to_dict(trial_data)

    # --- 6. Inter-Trial Interval (ITI) ---
    make_unit(unit_label='iti').show(duration=settings.iti_duration).to_dict(trial_data)

    return trial_data

