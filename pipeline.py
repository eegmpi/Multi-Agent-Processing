"""Agent 01 — EEG preprocessing: bandpass, notch, ICA, ASR artifact removal."""
from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class PreprocessingAgent(BaseAgent):
    """Cleans raw EEG data before feature extraction.

    Applies (in order):
    1. Bandpass filter
    2. Notch filter (power-line noise)
    3. Independent Component Analysis (ICA) — removes eye and muscle artefacts
    4. Artifact Subspace Reconstruction (ASR) — removes transient bursts

    Publishes cleaned epochs to ``preprocessing.output``.
    """

    agent_id = "preprocessing_agent"
    subscribe_to = ["raw_eeg.input"]
    publish_to = "preprocessing.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.bandpass: tuple[float, float] = tuple(config.get("bandpass", [1, 50]))  # type: ignore[assignment]
        self.notch_freq: float = float(config.get("notch", 50.0))
        self.use_ica: bool = bool(config.get("ica", True))
        self.use_asr: bool = bool(config.get("asr", True))

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Apply preprocessing pipeline to raw EEG payload.

        Args:
            payload: Dict with keys:
                - ``data``: ndarray of shape ``(n_channels, n_samples)``
                - ``sfreq``: sampling frequency in Hz
                - ``timestamp``: epoch start time (Unix float)
                - ``channel_names``: list of channel label strings

        Returns:
            Dict with the same keys, ``data`` replaced by cleaned signal.
        """
        data: np.ndarray = np.asarray(payload["data"])
        sfreq: float = float(payload["sfreq"])

        data = self._bandpass_filter(data, sfreq)
        data = self._notch_filter(data, sfreq)

        if self.use_ica:
            data = self._apply_ica(data)
        if self.use_asr:
            data = self._apply_asr(data, sfreq)

        logger.debug("PreprocessingAgent: cleaned epoch shape=%s", data.shape)
        return {**payload, "data": data.tolist(), "preprocessed": True}

    # ── Private helpers ────────────────────────────────────────────────────

    def _bandpass_filter(self, data: np.ndarray, sfreq: float) -> np.ndarray:
        from scipy.signal import butter, sosfiltfilt

        low, high = self.bandpass
        sos = butter(5, [low, high], btype="bandpass", fs=sfreq, output="sos")
        return sosfiltfilt(sos, data, axis=-1)

    def _notch_filter(self, data: np.ndarray, sfreq: float) -> np.ndarray:
        from scipy.signal import iirnotch, sosfilt

        b, a = iirnotch(self.notch_freq, Q=30.0, fs=sfreq)
        # Convert to SOS for numerical stability
        from scipy.signal import tf2sos

        sos = tf2sos(b, a)
        return sosfilt(sos, data, axis=-1)

    def _apply_ica(self, data: np.ndarray) -> np.ndarray:
        # Placeholder — production uses MNE ICA
        logger.debug("ICA: stub (MNE ICA applied in production)")
        return data

    def _apply_asr(self, data: np.ndarray, sfreq: float) -> np.ndarray:
        # Placeholder — production uses MNE autoreject / ASR
        logger.debug("ASR: stub (ASR applied in production)")
        return data
