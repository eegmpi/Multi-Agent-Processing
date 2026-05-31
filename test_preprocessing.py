"""Tests for FeatureExtractionAgent."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest

from agents.feature_extraction_agent import FeatureExtractionAgent


@pytest.fixture
def mock_bus() -> MagicMock:
    bus = MagicMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def agent(mock_bus: MagicMock) -> FeatureExtractionAgent:
    config = {"entropy": True, "coherence": True, "wavelet": True}
    return FeatureExtractionAgent(config, mock_bus)


def _preprocessed_payload(n_channels: int = 4, n_samples: int = 256, sfreq: float = 250.0) -> dict:
    rng = np.random.default_rng(0)
    data = rng.standard_normal((n_channels, n_samples))
    return {
        "data": data.tolist(),
        "sfreq": sfreq,
        "timestamp": 1_700_000_000.0,
        "channel_names": [f"CH{i}" for i in range(n_channels)],
        "preprocessed": True,
    }


@pytest.mark.asyncio
async def test_process_adds_features_key(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload())
    assert "features" in result


@pytest.mark.asyncio
async def test_band_power_keys_present(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload())
    features = result["features"]
    for band in ["delta", "theta", "alpha", "beta", "gamma"]:
        assert f"band_{band}" in features, f"Missing band_{band}"


@pytest.mark.asyncio
async def test_entropy_present(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload())
    assert "entropy" in result["features"]


@pytest.mark.asyncio
async def test_coherence_present(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload(n_channels=4))
    assert "coherence" in result["features"]


@pytest.mark.asyncio
async def test_wavelet_present(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload())
    assert "wavelet" in result["features"]


@pytest.mark.asyncio
async def test_band_power_values_non_negative(agent: FeatureExtractionAgent) -> None:
    result = await agent.process(_preprocessed_payload())
    features = result["features"]
    for band in ["delta", "theta", "alpha", "beta", "gamma"]:
        vals = features[f"band_{band}"]
        assert all(v >= 0 for v in vals), f"Negative power in {band}"
