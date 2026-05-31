"""Agent 04 — RL-based decision making and BCI command generation."""
from __future__ import annotations

import logging
from typing import Any

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

DEFAULT_ACTION_SPACE = ["command_left", "command_right", "command_select", "idle"]


class DecisionAgent(BaseAgent):
    """Converts mental state predictions into BCI output commands.

    Supports three decision strategies:

    - ``rl_based``: Reinforcement learning policy (Q-table or DQN)
    - ``rule_based``: Deterministic threshold rules
    - ``hybrid``: Rule-based with RL override above confidence threshold

    Publishes commands to ``decision.output``.
    """

    agent_id = "decision_agent"
    subscribe_to = ["classification.output"]
    publish_to = "decision.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.strategy: str = config.get("strategy", "rl_based")
        self.action_space: list[str] = config.get("action_space", DEFAULT_ACTION_SPACE)
        logger.info("DecisionAgent: strategy=%s actions=%s", self.strategy, self.action_space)

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Map classification predictions to a BCI command.

        Args:
            payload: Output from :class:`ClassificationAgent` — contains
                ``predictions`` dict and ``any_uncertain`` flag.

        Returns:
            Dict with ``command`` (string from action_space), ``confidence``,
            and ``strategy_used``.
        """
        predictions: dict[str, Any] = payload.get("predictions", {})

        if self.strategy == "rule_based":
            command, confidence = self._rule_based(predictions)
        elif self.strategy == "rl_based":
            command, confidence = self._rl_based(predictions)
        else:  # hybrid
            command, confidence = self._hybrid(predictions)

        logger.debug("DecisionAgent: command=%s confidence=%.3f", command, confidence)
        return {
            **payload,
            "command": command,
            "command_confidence": round(confidence, 4),
            "strategy_used": self.strategy,
        }

    # ── Strategies ─────────────────────────────────────────────────────────

    def _rule_based(self, predictions: dict[str, Any]) -> tuple[str, float]:
        motor = predictions.get("motor_intent", {})
        label = motor.get("label", "idle")
        confidence = motor.get("confidence", 0.5)
        mapping = {
            "left": "command_left",
            "right": "command_right",
            "feet": "command_select",
            "tongue": "command_select",
            "idle": "idle",
            "uncertain": "idle",
        }
        return mapping.get(label, "idle"), confidence

    def _rl_based(self, predictions: dict[str, Any]) -> tuple[str, float]:
        # Stub: production loads a trained DQN policy
        motor = predictions.get("motor_intent", {})
        label = motor.get("label", "idle")
        confidence = motor.get("confidence", 0.5)
        # RL adjusts based on full state (all target predictions)
        # For now delegate to rule-based mapping
        command, _ = self._rule_based(predictions)
        return command, min(confidence * 1.05, 1.0)

    def _hybrid(self, predictions: dict[str, Any]) -> tuple[str, float]:
        motor = predictions.get("motor_intent", {})
        confidence = motor.get("confidence", 0.0)
        if confidence >= 0.90:
            return self._rl_based(predictions)
        return self._rule_based(predictions)
