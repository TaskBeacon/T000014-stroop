# 任务流程审计

- 生成时间：2026-03-24
- 模式：existing
- 任务目录：`E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000014-stroop`

## 1. 输入与来源

- [README.md](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/README.md)
- [config/config.yaml](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/config/config.yaml)
- [src/run_trial.py](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000014-stroop/src/run_trial.py)

## 2. 从源码提取的证据

- `pre_stim_fixation`：`0.5 s`，中央 `+`
- `stroop_response`：`2.0 s`，中文颜色词刺激，按字色作答
- `feedback`：`0.5 s`，正确/错误/未反应三种结果之一
- `iti`：`0.8` 到 `1.2 s`，空白间隔

## 3. 绘图映射

- 采用一条件一时间线。
- 四条时间线分别对应 `congruent_red`、`congruent_green`、`incongruent_red`、`incongruent_green`。
- `feedback` 和 `iti` 都是通过 `show()` 直接呈现的参与者可见屏幕，没有单独的 `set_trial_context(...)`，因此在图中按可见流程推断。
- `feedback` 阶段使用独立中文图片资源，避免纯文本渲染出现问号。
- `ITI` 阶段保留为空白黑屏。
- 根键：`task_plot_spec`
- 规范版本：`0.2`

## 4. 版式与校验

- 输出文件：`task_flow.png`
- `max_conditions`：`4`
- `screens_per_timeline`：`4`
- `auto_width`：`true`
- 结果：自动压缩宽度后，右侧空白明显减少，四条时间线均可读。

## 5. 说明

- 初始自动生成版本把 4 个条件折叠成了 2 条代表性时间线，并遗漏了 `feedback` / `iti`，已手工重写规范修正。
- 反馈图资源使用 `SimHei` 重新生成后，中文输出恢复正常。
