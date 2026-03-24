# 源证据摘录（Stroop Task）

## 输入文件
- [README.md](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/README.md)
- [config/config.yaml](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/config/config.yaml)
- [src/run_trial.py](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/src/run_trial.py)

## 选定条件
- `congruent_red`
- `congruent_green`
- `incongruent_red`
- `incongruent_green`

## 关键试次流程
- `pre_stim_fixation`：`0.5 s`，中央 `+`
- `stroop_response`：`2.0 s`，显示单个中文颜色词，并按字色作答
- `feedback`：`0.5 s`，根据正确/错误/未反应显示 trial 反馈
- `iti`：`0.8` 到 `1.2 s`，空白间隔

## 备注
- `feedback` 和 `iti` 都是通过 `show()` 直接呈现的参与者可见屏幕，代码里没有单独的 `set_trial_context(...)`，因此在审计中按可见流程推断。
- 这次绘图按 4 个条件分别保留时间线，不再折叠成代表性逻辑。
