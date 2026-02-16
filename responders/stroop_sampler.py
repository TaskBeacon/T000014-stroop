from __future__ import annotations

from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


class StroopSamplerResponder:
    """Task-specific Stroop sampler responder."""

    def __init__(
        self,
        *,
        red_key: str = "f",
        green_key: str = "j",
        p_correct_congruent: float = 0.90,
        p_correct_incongruent: float = 0.78,
        p_miss: float = 0.05,
        rt_congruent_mean_s: float = 0.35,
        rt_incongruent_mean_s: float = 0.44,
        rt_sd_s: float = 0.07,
        rt_min_s: float = 0.12,
        continue_rt_s: float = 0.25,
    ):
        self.red_key = str(red_key)
        self.green_key = str(green_key)
        self.p_correct_congruent = float(p_correct_congruent)
        self.p_correct_incongruent = float(p_correct_incongruent)
        self.p_miss = float(p_miss)
        self.rt_congruent_mean_s = float(rt_congruent_mean_s)
        self.rt_incongruent_mean_s = float(rt_incongruent_mean_s)
        self.rt_sd_s = max(1e-6, float(rt_sd_s))
        self.rt_min_s = max(0.0, float(rt_min_s))
        self.continue_rt_s = float(continue_rt_s)
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def _pick_key(self, valid_keys: list[str], preferred: str | None = None) -> str | None:
        if not valid_keys:
            return None
        if preferred and preferred in valid_keys:
            return preferred
        return valid_keys[0]

    def _sample_rt(self, mean_s: float) -> float:
        if self._rng is None:
            return max(self.rt_min_s, mean_s)
        return max(self.rt_min_s, float(self._rng.gauss(mean_s, self.rt_sd_s)))

    def _deadline(self, obs: Observation) -> float | None:
        if obs.deadline_s is not None:
            return float(obs.deadline_s)
        if obs.response_window_s is not None:
            return float(obs.response_window_s)
        return None

    def act(self, obs: Observation) -> Action:
        if isinstance(obs, dict):
            obs = Observation.from_dict(obs)
        valid_keys = list(obs.valid_keys or [])
        phase = str(obs.phase or "").strip().lower()

        if phase in ("instruction_text", "block", "goodbye", "block_feedback"):
            key = self._pick_key(valid_keys)
            if key is None:
                return Action(key=None, rt_s=None, meta={"source": "stroop_sampler", "reason": "no_valid_key"})
            return Action(key=key, rt_s=max(0.01, self.continue_rt_s), meta={"source": "stroop_sampler", "phase": phase})

        if phase != "target" or self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "stroop_sampler", "phase": phase, "reason": "withhold"})

        condition = str(obs.condition_id or "").strip().lower()
        congruent = condition.startswith("congruent")
        correct_key = self.red_key if condition.endswith("red") else self.green_key

        if float(self._rng.random()) < self.p_miss:
            return Action(key=None, rt_s=None, meta={"source": "stroop_sampler", "condition": condition, "outcome": "miss"})

        p_correct = self.p_correct_congruent if congruent else self.p_correct_incongruent
        if float(self._rng.random()) <= p_correct:
            key = self._pick_key(valid_keys, preferred=correct_key)
            outcome = "correct"
        else:
            alt_keys = [k for k in valid_keys if k != correct_key]
            key = self._pick_key(alt_keys)
            outcome = "error"
            if key is None:
                return Action(key=None, rt_s=None, meta={"source": "stroop_sampler", "condition": condition, "outcome": "miss"})

        mean_s = self.rt_congruent_mean_s if congruent else self.rt_incongruent_mean_s
        rt_s = self._sample_rt(mean_s)
        deadline = self._deadline(obs)
        if deadline is not None and rt_s > deadline:
            return Action(key=None, rt_s=None, meta={"source": "stroop_sampler", "condition": condition, "outcome": "late"})

        return Action(key=key, rt_s=rt_s, meta={"source": "stroop_sampler", "condition": condition, "outcome": outcome})

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        return None
