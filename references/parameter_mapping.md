# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `conditions` | `task.conditions` | `['congruent_red', 'congruent_green', 'incongruent_red', 'incongruent_green']` | `STROOP1935` | Canonical Stroop manipulation contrasts congruent vs incongruent color-word pairings. | `direct` | Conditions encode congruency and ink color jointly. |
| `response_keys` | `task.red_key`, `task.green_key` | `red->f`, `green->j` | `MACLEOD1991` | Color naming via fixed response mapping is standard in computerized Stroop variants. | `adapted` | Keyboard mapping adapted for two-choice motor response. |
| `trial_count` | `task.total_blocks`, `task.trial_per_block` | Human: `3 x 60`; QA/sim: `1 x 16` | `MACLEOD1991` | Stable Stroop interference requires repeated sampling of both trial types. | `adapted` | QA/sim reduced for smoke tests only. |
| `fixation_duration` | `timing.fixation_duration` | `0.5 s` | `MACLEOD1988` | Pre-stimulus fixation is commonly used to control preparatory state before color-word onset. | `inferred` | Fixed value chosen for simple timing auditability. |
| `stim_duration` | `timing.stim_duration` | `2.0 s` | `MACLEOD1991` | Response-window bounded color naming is standard in RT/accuracy Stroop measurement. | `adapted` | Trial terminates on response before timeout. |
| `feedback_duration` | `timing.feedback_duration` | `0.5 s` | `MACLEOD1991` | Accuracy feedback is optional but common in training/practice or behavioral protocol variants. | `adapted` | Uses correct/incorrect/no-response text feedback. |
| `iti_range` | `timing.iti_duration` | `[0.8, 1.2] s` | `BOTVINICK2001` | Jittered ITI reduces temporal expectation and trial-onset anticipation in conflict paradigms. | `inferred` | Implemented as random duration in configured range. |
| `trigger_stim_onset` | `triggers.map.congruent_stim_onset`, `triggers.map.incongruent_stim_onset` | `10`, `20` | `BOTVINICK2001` | Congruent/incongruent event separation supports conflict-locked analyses in EEG settings. | `adapted` | Separate markers by congruency class. |
| `trigger_response` | `triggers.map.red_key_press`, `triggers.map.green_key_press` | `30`, `31` | `MACLEOD1991` | RT and response-channel identity are central Stroop outcome variables. | `direct` | Keys mapped to color decisions. |
| `trigger_feedback` | `triggers.map.feedback_correct_response`, `feedback_incorrect_response`, `feedback_no_response` | `51`, `52`, `53` | `MACLEOD1991` | Trial outcome classification (correct/error/miss) is required for accuracy analysis. | `adapted` | Outcome-specific trigger plan. |
