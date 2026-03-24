# Stroop Task

![Maturity: smoke_tested](https://img.shields.io/badge/Maturity-smoke_tested-d97706?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Stroop Task |
| Version | v1.1.2 |
| URL / Repository | https://github.com/TaskBeacon/T000014-stroop |
| Short Description | Classic color-word Stroop task measuring interference control (congruent vs incongruent trials). |
| Created By | Zhipeng Cao (zhipeng30@foxmail.com) |
| Date Updated | 2026-03-02 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior / EEG |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## Run Modes

- Human (default): `python main.py`
- QA: `python main.py qa --config config/config_qa.yaml`
- Scripted Sim: `python main.py sim --config config/config_scripted_sim.yaml`
- Sampler Sim: `python main.py sim --config config/config_sampler_sim.yaml`

## 1. Task Overview

This Stroop implementation presents Chinese color words in either congruent or incongruent ink colors. Participants respond to ink color while ignoring word meaning. The key outcomes are reaction time and accuracy differences between congruent and incongruent conditions.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

| Step | Description |
|---|---|
| Setup | Load config, initialize mode context (`human/qa/sim`), open PsychoPy window, load stimuli, initialize trigger runtime. |
| Instruction | Show task instructions (`instruction_text`; optional voice in human mode). |
| Block Loop | Generate conditions and run trial loop via `BlockUnit.run_trial(...)`. |
| Block Summary | Compute block accuracy and show `block_break` screen. |
| Finalize | Show `good_bye`, send `exp_end`, save CSV, close trigger runtime, quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Fixation | Show fixation cross (`+`) for `fixation_duration`. |
| Stroop Response | Show one condition stimulus (`congruent_*` / `incongruent_*`) and capture response within `stim_duration`. |
| Feedback | Show `correct_feedback`, `incorrect_feedback`, or `no_response_feedback`. |
| ITI | Blank interval sampled from `iti_duration`. |

### Controller Logic

No adaptive controller is used in this baseline Stroop variant.

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant ID (3 digits). |
| `subname` | Participant name (pinyin). |
| `age` | Age (5-60). |
| `gender` | `Male` or `Female`. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `window.size` | `[1920, 1080]` |
| `window.units` | `deg` |
| `window.fullscreen` | `true` |
| `window.bg_color` | `gray` |
| `window.monitor_width_cm` | `60` |
| `window.monitor_distance_cm` | `72` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `fixation` | `text` | Central `+` fixation. |
| `congruent_red` | `text` | Character "红" in red. |
| `congruent_green` | `text` | Character "绿" in green. |
| `incongruent_red` | `text` | Character "绿" in red. |
| `incongruent_green` | `text` | Character "红" in green. |
| `correct_feedback` | `text` | Correct response message. |
| `incorrect_feedback` | `text` | Incorrect response message. |
| `no_response_feedback` | `text` | No-response message. |
| `instruction_text` | `textbox` | Chinese task instructions. |
| `block_break` | `text` | Block transition with accuracy summary. |
| `good_bye` | `text` | End-of-task message. |

### d. Timing

| Phase | Duration |
|---|---|
| `fixation_duration` | `0.5 s` |
| `stim_duration` | `2.0 s` |
| `feedback_duration` | `0.5 s` |
| `iti_duration` | Random in `[0.8, 1.2] s` |

### e. Triggers

| Event | Code |
|---|---:|
| `exp_onset` | 98 |
| `exp_end` | 99 |
| `block_onset` | 100 |
| `block_end` | 101 |
| `fixation_onset` | 1 |
| `congruent_stim_onset` | 10 |
| `incongruent_stim_onset` | 20 |
| `red_key_press` | 30 |
| `green_key_press` | 31 |
| `feedback_correct_response` | 51 |
| `feedback_incorrect_response` | 52 |
| `feedback_no_response` | 53 |

## 4. Methods (for academic publication)

Participants performed a computerized Stroop color-word task. Each trial started with a fixation cross, followed by a single Chinese color word rendered in either congruent or incongruent ink color. Participants were instructed to respond to the ink color (red vs green) while ignoring lexical meaning.

Stimuli remained on screen for up to 2 seconds or until response, followed by brief trial-wise feedback and a jittered inter-trial interval. The design included both congruent and incongruent trials within each block, enabling estimation of classical Stroop interference through reaction-time and accuracy contrasts.

The task is implemented for behavioral and EEG-compatible runs with explicit trigger coding for experiment boundaries, stimulus onset class, response channel, and feedback outcome.
