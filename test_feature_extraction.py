"""Tests for ClassificationAgent."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from agents.classification_agent import ClassificationAgent

TARGETS = ["emotion", "focus", "fatigue", "motor_intent"]


@pytest.fixture
def mock_bus() -> MagicMock:
    bus = MagicMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def agent(mock_bus: MagicMock) -> ClassificationAgent:
    config = {
        "model": "eegnet_transformer",
        "targets": TARGETS,
        "confidence_threshold": 0.85,
    }
    return ClassificationAgent(config, mock_bus)


def _feature_payload() -> dict:
    return {
        "timestamp": 1_700_000_000.0,
        "sfreq": 250.0,
        "features": {
            "band_delta": [0.1, 0.2, 0.3, 0.4],
            "band_alpha": [0.5, 0.6, 0.7, 0.8],
            "entropy": [1.2, 1.3, 1.1, 1.4],
        },
    }


@pytest.mark.asyncio
async def test_predictions_key_present(agent: ClassificationAgent) -> None:
    result = await agent.process(_feature_payload())
    assert "predictions" in result


@pytest.mark.asyncio
async def test_all_targets_in_predictions(agent: ClassificationAgent) -> None:
    result = await agent.process(_feature_payload())
    for target in TARGETS:
        assert target in result["predictions"]


@pytest.mark.asyncio
async def test_prediction_has_required_fields(agent: ClassificationAgent) -> None:
    result = await agent.process(_feature_payload())
    for target, pred in result["predictions"].items():
        assert "label" in pred, f"{target} missing 'label'"
        assert "confidence" in pred, f"{target} missing 'confidence'"
        assert "uncertain" in pred, f"{target} missing 'uncertain'"


@pytest.mark.asyncio
async def test_confidence_in_valid_range(agent: ClassificationAgent) -> None:
    result = await agent.process(_feature_payload())
    for target, pred in result["predictions"].items():
        assert 0.0 <= pred["confidence"] <= 1.0, f"{target} confidence out of range"


@pytest.mark.asyncio
async def test_uncertain_label_when_below_threshold(mock_bus: MagicMock) -> None:
    """Force all predictions uncertain by setting very high threshold."""
    config = {"model": "eegnet_transformer", "targets": TARGETS, "confidence_threshold": 0.9999}
    agent = ClassificationAgent(config, mock_bus)
    result = await agent.process(_feature_payload())
    uncertain_labels = [p["label"] for p in result["predictions"].values()]
    # At least some should be uncertain
    assert any(lbl == "uncertain" for lbl in uncertain_labels)
