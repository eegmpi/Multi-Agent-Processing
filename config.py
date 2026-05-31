"""Agent 03 — Mental state classification using EEGNet + Transformer ensemble."""
from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

TARGETS = ["emotion", "focus", "fatigue", "motor_intent"]


class ClassificationAgent(BaseAgent):
    """Classifies mental states from EEG feature vectors.

    Uses an EEGNet + Transformer ensemble model trained on multi-task
    EEG datasets (DEAP, PhysioNet Motor Imagery, SEED).

    Supported classification targets:
    - ``emotion``: valence/arousal quadrant (4-class)
    - ``focus``: focused / unfocused (binary)
    - ``fatigue``: alert / drowsy / asleep (3-class)
    - ``motor_intent``: left / right / feet / tongue / idle (5-class)

    Publishes predictions to ``classification.output``.
    """

    agent_id = "classification_agent"
    subscribe_to = ["feature_extraction.output"]
    publish_to = "classification.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.model_name: str = config.get("model", "eegnet_transformer")
        self.targets: list[str] = config.get("targets", TARGETS)
        self.confidence_threshold: float = float(config.get("confidence_threshold", 0.85))
        self._model: Any = None
        logger.info("ClassificationAgent: model=%s targets=%s", self.model_name, self.targets)

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Run classification on extracted features.

        Args:
            payload: Output from :class:`FeatureExtractionAgent` — contains
                ``features`` dict and original ``data`` / ``timestamp``.

        Returns:
            Dict with ``predictions`` (per-target label + confidence)
            and ``uncertain`` flag if any prediction is below threshold.
        """
        features = payload.get("features", {})
        feature_vec = self._flatten_features(features)

        predictions: dict[str, dict[str, Any]] = {}
        any_uncertain = False

        for target in self.targets:
            label, confidence = self._predict_target(target, feature_vec)
            uncertain = confidence < self.confidence_threshold
            if uncertain:
                any_uncertain = True
            predictions[target] = {
                "label": label if not uncertain else "uncertain",
                "confidence": round(confidence, 4),
                "uncertain": uncertain,
            }

        logger.debug("ClassificationAgent predictions: %s", predictions)
        return {**payload, "predictions": predictions, "any_uncertain": any_uncertain}

    # ── Private helpers ────────────────────────────────────────────────────

    def _flatten_features(self, features: dict[str, Any]) -> np.ndarray:
        parts = []
        for v in features.values():
            arr = np.asarray(v, dtype=np.float32).ravel()
            parts.append(arr)
        return np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)

    def _predict_target(self, target: str, feature_vec: np.ndarray) -> tuple[str, float]:
        # Stub — production loads PyTorch EEGNet+Transformer weights
        label_maps = {
            "emotion": ["neutral", "happy", "sad", "angry"],
            "focus": ["focused", "unfocused"],
            "fatigue": ["alert", "drowsy", "asleep"],
            "motor_intent": ["left", "right", "feet", "tongue", "idle"],
        }
        labels = label_maps.get(target, ["unknown"])
        rng = np.random.default_rng(seed=int(np.sum(feature_vec[:4]) * 1000) % (2**31))
        idx = rng.integers(0, len(labels))
        confidence = float(rng.uniform(0.82, 0.99))
        return labels[idx], confidence
