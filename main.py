from psyflow import BlockUnit, StimBank, StimUnit, SubInfo, TaskSettings, initialize_triggers
from psyflow import load_config, count_down, initialize_exp
import pandas as pd
from psychopy import core
from functools import partial
import numpy as np
from src.run_trial import run_trial

# 1. Load config
cfg = load_config()

# 2. Collect subject info
subform = SubInfo(cfg['subform_config'])
subject_data = subform.collect()

# 3. Load task settings
settings = TaskSettings.from_dict(cfg['task_config'])
settings.add_subinfo(subject_data)

# 4. Setup triggers
settings.triggers = cfg['trigger_config']

trigger_runtime = initialize_triggers(cfg)

# 5. Set up window & input
win, kb = initialize_exp(settings)

# 6. Setup stimulus bank
stim_bank = StimBank(win, cfg['stim_config']).convert_to_voice('instruction_text', voice=settings.voice_name).preload_all()

# 7. Save settings to a JSON file for record-keeping
settings.save_to_json()

# Send experiment start trigger
trigger_runtime.send(settings.triggers.get("exp_onset"))

# Show instructions
StimUnit('instruction_text', win, kb) \
    .add_stim(stim_bank.get('instruction_text')) \
    .add_stim(stim_bank.get('instruction_text_voice')) \
    .wait_and_continue()

all_data = []
for block_i in range(settings.total_blocks):
    # Display countdown before each block
    count_down(win, 3, color='white')

    # 8. Setup and run the block
    block = BlockUnit(
        block_id=f"block_{block_i}",
        block_idx=block_i,
        settings=settings,
        window=win,
        keyboard=kb
    ) \
    .generate_conditions() \
    .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset"))) \
    .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end"))) \
    .run_trial(partial(run_trial, stim_bank=stim_bank, trigger_runtime=trigger_runtime)) \
    .to_dict(all_data)

    # --- Block Feedback ---
    block_trials = block.get_all_data()
    # Calculate accuracy and mean reaction time for the block
    correct_trials = [t for t in block_trials if t.get('stimulus_hit', False) is True]
    accuracy = len(correct_trials) / len(block_trials) if block_trials else 0
    


    # Display the feedback screen
    StimUnit('block_feedback', win, kb) \
        .add_stim(stim_bank.get_and_format('block_break', 
                                             block_num=block_i + 1, 
                                             total_blocks=settings.total_blocks,
                                             accuracy=accuracy)) \
        .wait_and_continue()

# --- End of Experiment ---
# Display goodbye message
StimUnit('goodbye', win, kb) \
    .add_stim(stim_bank.get('good_bye')) \
    .wait_and_continue(terminate=True) 

# Send experiment end trigger
trigger_runtime.send(settings.triggers.get("exp_end"))

# 9. Save data to CSV
df = pd.DataFrame(all_data)
df.to_csv(settings.res_file, index=False)
print(f"Data saved to {settings.res_file}")

# 10. Close everything
trigger_runtime.close()
core.quit()



