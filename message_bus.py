"""Agent 05 — Real-time WebSocket dashboard streaming at 30 fps."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class VisualizationAgent(BaseAgent):
    """Streams EEG data and predictions to the browser dashboard via WebSocket.

    Listens on two topics:
    - ``preprocessing.output`` — raw + cleaned signal for waveform display
    - ``decision.output`` — commands and predictions for status panel

    Broadcasts JSON frames to all connected WebSocket clients at up to 30 fps.
    Also computes a simplified topographic scalp map from channel power values.
    """

    agent_id = "visualization_agent"
    subscribe_to = ["preprocessing.output", "decision.output"]
    publish_to = "visualization.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.port: int = int(config.get("port", 8080))
        self.fps: int = int(config.get("fps", 30))
        self.show_topography: bool = bool(config.get("show_topography", True))
        self.show_spectrum: bool = bool(config.get("show_spectrum", True))
        self._clients: set[Any] = set()
        self._frame_interval: float = 1.0 / self.fps

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Package payload into a dashboard frame and broadcast to clients.

        Args:
            payload: Either preprocessed EEG or decision output payload.

        Returns:
            Passthrough of the payload (unchanged).
        """
        frame = self._build_frame(payload)
        await self._broadcast(frame)
        return payload

    # ── Frame builder ──────────────────────────────────────────────────────

    def _build_frame(self, payload: dict[str, Any]) -> dict[str, Any]:
        frame: dict[str, Any] = {
            "timestamp": payload.get("timestamp", 0.0),
            "type": "eeg" if "data" in payload else "decision",
        }

        if "data" in payload:
            data = payload["data"]
            # Send only last 256 samples per channel for bandwidth
            if isinstance(data, list):
                frame["eeg"] = [ch[-256:] for ch in data] if data else []
            frame["channel_names"] = payload.get("channel_names", [])

        if "predictions" in payload:
            frame["predictions"] = payload["predictions"]
            frame["command"] = payload.get("command", "idle")

        if "features" in payload and self.show_spectrum:
            frame["band_power"] = {
                k: v for k, v in payload["features"].items() if k.startswith("band_")
            }

        return frame

    # ── WebSocket broadcast ────────────────────────────────────────────────

    async def _broadcast(self, frame: dict[str, Any]) -> None:
        if not self._clients:
            return
        message = json.dumps(frame)
        disconnected = set()
        for ws in self._clients:
            try:
                await ws.send(message)
            except Exception:  # noqa: BLE001
                disconnected.add(ws)
        self._clients -= disconnected

    def register_client(self, ws: Any) -> None:
        """Register a new WebSocket client."""
        self._clients.add(ws)
        logger.info("VisualizationAgent: client connected (total=%d)", len(self._clients))

    def unregister_client(self, ws: Any) -> None:
        """Remove a disconnected WebSocket client."""
        self._clients.discard(ws)
        logger.info("VisualizationAgent: client disconnected (total=%d)", len(self._clients))
