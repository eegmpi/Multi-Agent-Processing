"""Integration tests for the EEG-MPI Pipeline."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.config import Config
from core.pipeline import Pipeline


@pytest.fixture
def config(tmp_path) -> Config:
    """Config with all agents enabled and mocked Redis."""
    cfg = Config.__new__(Config)
    cfg._data = {
        "eegmpi": {"version": "2.4.1", "mode": "demo"},
        "source": {"device": "sample", "channels": 4, "sample_rate": 250, "buffer_size": 256},
        "message_bus": {"backend": "redis", "host": "localhost", "port": 6379},
        "agents": {
            "preprocessing": {"enabled": True, "bandpass": [1, 50], "notch": 50, "ica": False, "asr": False},
            "feature_extraction": {"enabled": True, "entropy": True, "coherence": False, "wavelet": False},
            "classification": {
                "enabled": True,
                "model": "eegnet_transformer",
                "targets": ["focus"],
                "confidence_threshold": 0.80,
            },
            "decision": {"enabled": True, "strategy": "rule_based", "action_space": ["idle", "command_left"]},
            "visualization": {"enabled": False},
        },
        "logging": {"level": "WARNING", "output": ["console"]},
    }
    return cfg


@pytest.mark.asyncio
async def test_pipeline_starts_and_stops(config: Config) -> None:
    """Pipeline should start enabled agents and stop without errors."""
    with (
        patch("core.pipeline.MessageBus") as MockBus,
    ):
        mock_bus_instance = MagicMock()
        mock_bus_instance.connect = AsyncMock()
        mock_bus_instance.disconnect = AsyncMock()
        mock_bus_instance.subscribe = AsyncMock(return_value=aiter_empty())
        MockBus.return_value = mock_bus_instance

        pipeline = Pipeline(config)
        # Patch agent start/stop
        with patch.object(pipeline, "_agents", []):
            await pipeline.start()
            await pipeline.stop()


@pytest.mark.asyncio
async def test_pipeline_skips_disabled_agent(config: Config) -> None:
    """Visualization agent (disabled) should not be instantiated."""
    config._data["agents"]["visualization"]["enabled"] = False
    with patch("core.pipeline.MessageBus") as MockBus:
        mock_bus_instance = MagicMock()
        mock_bus_instance.connect = AsyncMock()
        mock_bus_instance.disconnect = AsyncMock()
        MockBus.return_value = mock_bus_instance

        pipeline = Pipeline(config)
        with patch("core.pipeline.VisualizationAgent") as MockViz:
            MockViz.return_value = MagicMock(start=AsyncMock(), stop=AsyncMock())
            await pipeline.start()
            MockViz.assert_not_called()
            await pipeline.stop()


# Helper: async generator that yields nothing
async def aiter_empty():
    return
    yield  # make it an async generator
