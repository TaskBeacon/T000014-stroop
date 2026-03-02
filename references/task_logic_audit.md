# Task Logic Audit

## 1. Paradigm Intent

- Task: Stroop color-word interference task (single-word, two-choice color naming)
- Primary construct: Selective attention and interference control during response selection
- Manipulated factors:
  - Congruency (`congruent` vs `incongruent`)
  - Ink color (`red` vs `green`)
- Dependent measures:
  - Reaction time (RT) to color response
  - Accuracy by congruency
  - No-response rate
- Key citations:
  - `STROOP1935`
  - `MACLEOD1991`
  - `MACLEOD1988`
  - `BOTVINICK2001`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 (human), 1 (qa/sim)
- Trials per block: 60 (human), 16 (qa/sim)
- Randomization/counterbalancing:
  - Conditions sampled from `task.conditions` by `BlockUnit.generate_conditions()`.
  - Even condition sampling is implied when no `condition_weights` are provided.
- Condition generation method:
  - Built-in PsyFlow condition generation.
- Runtime-generated trial values:
  - ITI sampled from configured range `[0.8, 1.2]` seconds.

### Trial State Machine

1. State name: `pre_stim_fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: fixation cross (`+`)
   - Valid keys: `task.key_list`
   - Timeout behavior: auto-advance after `fixation_duration`
   - Next state: `stroop_response`

2. State name: `stroop_response`
   - Onset trigger: `congruent_stim_onset` or `incongruent_stim_onset`
   - Stimuli shown: one color-word item (`congruent_*` / `incongruent_*`)
   - Valid keys: `task.key_list`
   - Timeout behavior: closes at `stim_duration`; no response marked as miss
   - Next state: `feedback`

3. State name: `feedback`
   - Onset trigger: one of `feedback_correct_response`, `feedback_incorrect_response`, `feedback_no_response`
   - Stimuli shown: outcome text from config
   - Valid keys: none
   - Timeout behavior: auto-advance after `feedback_duration`
   - Next state: `iti`

4. State name: `iti`
   - Onset trigger: none
   - Stimuli shown: blank interval
   - Valid keys: none
   - Timeout behavior: auto-advance after sampled ITI
   - Next state: next trial

## 3. Condition Semantics

- Condition ID: `congruent_red`
  - Participant-facing meaning: red word in red color.
  - Stimulus realization: text "红" in red.
  - Correct response: `red_key`.

- Condition ID: `congruent_green`
  - Participant-facing meaning: green word in green color.
  - Stimulus realization: text "绿" in green.
  - Correct response: `green_key`.

- Condition ID: `incongruent_red`
  - Participant-facing meaning: green word in red color (conflict).
  - Stimulus realization: text "绿" in red.
  - Correct response: `red_key`.

- Condition ID: `incongruent_green`
  - Participant-facing meaning: red word in green color (conflict).
  - Stimulus realization: text "红" in green.
  - Correct response: `green_key`.

Participant-facing text/stimuli source:

- Source: `config/*.yaml` under `stimuli`.
- Why appropriate: supports localization without runtime-code edits.
- Localization strategy: replace text content in config while preserving runtime flow in `src/run_trial.py`.

## 4. Response and Scoring Rules

- Response mapping:
  - Red ink -> `task.red_key` (default `f`)
  - Green ink -> `task.green_key` (default `j`)
- Response key source: `task` section in config.
- Missing-response policy:
  - If no key within `stim_duration`, classify as no response and show miss feedback.
- Correctness logic:
  - `StimUnit.capture_response(..., correct_keys=...)` computes `hit`.
- Reward/penalty updates:
  - No monetary scoring in this baseline variant.
- Running metrics:
  - Block-level accuracy displayed at block transition.

## 5. Stimulus Layout Plan

- Screen: `pre_stim_fixation`
  - Stimulus IDs: `fixation`
  - Layout: center
  - Rationale: neutral pre-target anchor.

- Screen: `stroop_response`
  - Stimulus IDs: one color-word item per trial
  - Layout: centered single text item, no overlap risk
  - Rationale: isolate color naming and semantic interference.

- Screen: `feedback`
  - Stimulus IDs: one feedback text item
  - Layout: centered text
  - Rationale: immediate trial outcome communication.

- Screen: instruction / block break / goodbye
  - Stimulus IDs: `instruction_text`, `block_break`, `good_bye`
  - Layout: centered textbox/text with configured size and line spacing
  - Rationale: readable transition and instruction screens.

## 6. Trigger Plan

- `exp_onset` / `exp_end`: experiment boundary markers
- `block_onset` / `block_end`: block boundary markers
- `fixation_onset`: fixation onset
- `congruent_stim_onset`: congruent trial stimulus onset
- `incongruent_stim_onset`: incongruent trial stimulus onset
- `red_key_press` / `green_key_press`: response channel markers
- `feedback_correct_response` / `feedback_incorrect_response` / `feedback_no_response`: outcome markers

## 7. Architecture Decisions (Auditability)

- `main.py` style: one mode-aware runtime (`human`, `qa`, `sim`) with shared setup.
- `utils.py` used: no task-specific helper is required.
- Custom controller used: no.
- Why PsyFlow-native path is sufficient:
  - Condition generation, response capture, and trigger emission are directly expressible with standard `BlockUnit` and `StimUnit`.
- Legacy/backward-compatibility fallback logic required: no.

## 8. Inference Log

- Decision: block count/trial count for human profile set to `3 x 60`.
  - Why inference was required: selected references establish paradigmatic structure but do not enforce a single mandatory run length.
  - Citation-supported rationale: `MACLEOD1991` supports repeated sampling for stable congruency effects.

- Decision: QA/sim shortened to `1 x 16`.
  - Why inference was required: development gates need mechanism coverage with fast runtime.
  - Citation-supported rationale: non-human smoke profiles are engineering adaptations and do not alter paradigm semantics.

- Decision: feedback screens retained in this implementation.
  - Why inference was required: original Stroop protocols vary in feedback use.
  - Citation-supported rationale: outcome coding remains compatible with `MACLEOD1991` analysis framework.
