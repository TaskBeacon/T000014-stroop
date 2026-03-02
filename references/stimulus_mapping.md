# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `congruent_red` | `stroop_response` | `congruent_red` | Character "红" shown in red ink; respond by ink color. | `STROOP1935` | Congruent condition where word meaning matches font color. | `psychopy_builtin` | `n/a` | Trigger: `congruent_stim_onset`. |
| `congruent_green` | `stroop_response` | `congruent_green` | Character "绿" shown in green ink; respond by ink color. | `STROOP1935` | Congruent condition where word meaning matches font color. | `psychopy_builtin` | `n/a` | Trigger: `congruent_stim_onset`. |
| `incongruent_red` | `stroop_response` | `incongruent_red` | Character "绿" shown in red ink; ignore word meaning and report ink color. | `STROOP1935` | Incongruent condition where semantic and color channels conflict. | `psychopy_builtin` | `n/a` | Trigger: `incongruent_stim_onset`. |
| `incongruent_green` | `stroop_response` | `incongruent_green` | Character "红" shown in green ink; ignore word meaning and report ink color. | `STROOP1935` | Incongruent condition where semantic and color channels conflict. | `psychopy_builtin` | `n/a` | Trigger: `incongruent_stim_onset`. |
| `all_conditions` | `pre_stim_fixation` | `fixation` | Central fixation cross before color-word onset. | `MACLEOD1991` | Standard preparatory fixation before target presentation. | `psychopy_builtin` | `n/a` | Fixed duration `0.5 s`. |
| `all_conditions` | `feedback` | `correct_feedback` / `incorrect_feedback` / `no_response_feedback` | Outcome message shown after response window. | `MACLEOD1991` | Accuracy coding is required for Stroop performance summaries. | `psychopy_builtin` | `n/a` | Outcome text comes from config for localization portability. |
| `block_transition` | `block_feedback` | `block_break` | Inter-block summary with block number and accuracy. | `MACLEOD1991` | Blocked Stroop protocols commonly include rest transitions. | `psychopy_builtin` | `n/a` | Text template formatted with runtime metrics. |
| `task_start_end` | `instruction_text` / `goodbye` | `instruction_text`, `good_bye` | Chinese instruction and ending screens. | `MACLEOD1991` | Clear instructions to name ink color and ignore word meaning are paradigm-defining. | `psychopy_builtin` | `assets/instruction_text_voice.mp3` | Human mode optionally uses generated voice for instructions. |
