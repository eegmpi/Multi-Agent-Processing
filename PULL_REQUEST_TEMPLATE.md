"""Tests for PreprocessingAgent."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest

from agents.preprocessing_agent import PreprocessingAgent


@pytest.fixture
def mock_bus() -> MagicMock:
    bus = MagicMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture
def agent(mock_bus: MagicMock) -> PreprocessingAgent:
    config = {"bandpass": [1, 50], "notch": 50, "ica": False, "asr": False}
    return PreprocessingAgent(config, mock_bus)


def _make_payload(n_channels: int = 8, n_samples: int = 512, sfreq: float = 250.0) -> dict:
    rng = np.random.default_rng(42)
    data = rng.standard_normal((n_channels, n_samples))
    return {
        "data": data.tolist(),
        "sfreq": sfreq,
        "timestamp": 1_700_000_000.0,
        "channel_names": [f"CH{i}" for i in range(n_channels)],
    }


@pytest.mark.asyncio
async def test_process_returns_dict(agent: PreprocessingAgent) -> None:
    payload = _make_payload()
    result = await agent.process(payload)
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_process_preserves_shape(agent: PreprocessingAgent) -> None:
    payload = _make_payload(n_channels=8, n_samples=512)
    result = await agent.process(payload)
    data = np.array(result["data"])
    assert data.shape == (8, 512)


@pytest.mark.asyncio
async def test_process_sets_preprocessed_flag(agent: PreprocessingAgent) -> None:
    payload = _make_payload()
    result = await agent.process(payload)
    assert result.get("preprocessed") is True


@pytest.mark.asyncio
async def test_process_preserves_timestamp(agent: PreprocessingAgent) -> None:
    payload = _make_payload()
    result = await agent.process(payload)
    assert result["timestamp"] == payload["timestamp"]


@pytest.mark.asyncio
async def test_bandpass_reduces_high_freq_noise(agent: PreprocessingAgent) -> None:
    """After bandpass, energy above cutoff should be reduced."""
    sfreq = 250.0
    t = np.linspace(0, 2, int(sfreq * 2), endpoint=False)
    # Signal: 10 Hz (pass) + 100 Hz (stop)
    signal = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 100 * t)
    data = signal[np.newaxis, :]  # (1, n_samples)

    filtered = agent._bandpass_filter(data, sfreq)
    from scipy.signal import welch

    freqs, psd_orig = welch(data[0], fs=sfreq)
    freqs, psd_filt = welch(filtered[0], fs=sfreq)

    idx_high = np.where(freqs > 60)[0]
    # High-frequency power should be lower after filtering
    assert psd_filt[idx_high].mean() < psd_orig[idx_high].mean()
