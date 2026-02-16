from functools import partial

from psyflow import StimUnit, set_trial_context

# trial stages: cue -> anticipation -> target -> feedback
_TRIAL_COUNTER = 0


def _next_trial_id() -> int:
    global _TRIAL_COUNTER
    _TRIAL_COUNTER += 1
    return _TRIAL_COUNTER


def _deadline_s(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def run_trial(
    win,
    kb,
    settings,
    condition: str,
    stim_bank: dict,
    trigger_runtime=None,
    block_id=None,
    block_idx=None,
):
    """Run one Stroop trial."""
    trial_id = _next_trial_id()
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    stroop_type, color = condition.split("_")
    correct_response = settings.red_key if color == "red" else settings.green_key

    trial_data.update(
        {
            "stroop_type": stroop_type,
            "color": color,
            "correct_response": correct_response,
        }
    )

    # cue / anticipation
    fixation_unit = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation_unit,
        trial_id=trial_id,
        phase="anticipation",
        deadline_s=_deadline_s(settings.fixation_duration),
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={
            "condition": str(condition),
            "stage": "anticipation",
            "stroop_type": stroop_type,
            "color": color,
            "block_idx": block_idx,
        },
        stim_id="fixation",
    )
    fixation_unit.show(
        duration=settings.fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    # target
    stim_unit = make_unit(unit_label="stimulus").add_stim(stim_bank.get(condition))
    set_trial_context(
        stim_unit,
        trial_id=trial_id,
        phase="target",
        deadline_s=_deadline_s(settings.stim_duration),
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={
            "condition": str(condition),
            "stage": "target",
            "stroop_type": stroop_type,
            "color": color,
            "correct_key": str(correct_response),
            "block_idx": block_idx,
        },
        stim_id=str(condition),
    )
    stim_unit.capture_response(
        keys=settings.key_list,
        correct_keys=correct_response,
        duration=settings.stim_duration,
        response_trigger={
            settings.red_key: settings.triggers.get("red_key_press"),
            settings.green_key: settings.triggers.get("green_key_press"),
        },
        onset_trigger=settings.triggers.get(f"{stroop_type}_stim_onset"),
        terminate_on_response=True,
    )
    stim_unit.to_dict(trial_data)

    # feedback
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

    make_unit(unit_label="feedback").add_stim(feedback_stim).show(
        duration=settings.feedback_duration,
        onset_trigger=feedback_trigger,
    ).to_dict(trial_data)

    make_unit(unit_label="iti").show(duration=settings.iti_duration).to_dict(trial_data)

    return trial_data
