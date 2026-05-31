"""Agent 02 — Feature extraction: band power, entropy, coherence, wavelets."""
from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

BANDS = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
    "gamma": (30.0, 50.0),
}


class FeatureExtractionAgent(BaseAgent):
    """Extracts features from preprocessed EEG epochs.

    Features computed (configurable):
    - Per-channel, per-band power (delta, theta, alpha, beta, gamma)
    - Spectral entropy
    - Inter-channel coherence matrix
    - Daubechies-4 wavelet decomposition coefficients

    Publishes feature vectors to ``feature_extraction.output``.
    """

    agent_id = "feature_extraction_agent"
    subscribe_to = ["preprocessing.output"]
    publish_to = "feature_extraction.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.compute_entropy: bool = bool(config.get("entropy", True))
        self.compute_coherence: bool = bool(config.get("coherence", True))
        self.compute_wavelet: bool = bool(config.get("wavelet", True))
        custom_bands: dict[str, list[float]] | None = config.get("bands")
        if custom_bands:
            self.bands = {k: tuple(v) for k, v in custom_bands.items()}  # type: ignore[assignment]
        else:
            self.bands = BANDS

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Compute feature vector from a preprocessed EEG epoch.

        Args:
            payload: Output from :class:`PreprocessingAgent` — contains
                ``data`` (n_channels × n_samples ndarray), ``sfreq``, ``timestamp``.

        Returns:
            Dict with ``features`` key containing a flat feature vector (list of floats)
            and ``feature_names`` key listing each feature's label.
        """
        data: np.ndarray = np.asarray(payload["data"])
        sfreq: float = float(payload["sfreq"])

        features: dict[str, Any] = {}

        # Band power
        band_power = self._band_power(data, sfreq)
        features.update(band_power)

        # Spectral entropy
        if self.compute_entropy:
            features["entropy"] = self._spectral_entropy(data, sfreq).tolist()

        # Coherence
        if self.compute_coherence:
            features["coherence"] = self._coherence(data, sfreq).tolist()

        # Wavelet
        if self.compute_wavelet:
            features["wavelet"] = self._wavelet(data).tolist()

        logger.debug("FeatureExtractionAgent: extracted %d feature groups", len(features))
        return {**payload, "features": features}

    # ── Private helpers ────────────────────────────────────────────────────

    def _band_power(self, data: np.ndarray, sfreq: float) -> dict[str, list[float]]:
        from scipy.signal import welch

        n_per_seg = min(256, data.shape[-1])
        freqs, psd = welch(data, fs=sfreq, nperseg=n_per_seg)
        result = {}
        for band_name, (low, high) in self.bands.items():
            idx = np.logical_and(freqs >= low, freqs <= high)
            power = np.mean(psd[:, idx], axis=-1)  # (n_channels,)
            result[f"band_{band_name}"] = power.tolist()
        return result

    def _spectral_entropy(self, data: np.ndarray, sfreq: float) -> np.ndarray:
        from scipy.signal import welch

        _, psd = welch(data, fs=sfreq, nperseg=min(256, data.shape[-1]))
        psd_norm = psd / (psd.sum(axis=-1, keepdims=True) + 1e-12)
        entropy = -np.sum(psd_norm * np.log2(psd_norm + 1e-12), axis=-1)
        return entropy

    def _coherence(self, data: np.ndarray, sfreq: float) -> np.ndarray:
        from scipy.signal import coherence

        n_ch = data.shape[0]
        coh_matrix = np.zeros((n_ch, n_ch))
        for i in range(n_ch):
            for j in range(i + 1, n_ch):
                _, cxy = coherence(data[i], data[j], fs=sfreq)
                coh_matrix[i, j] = coh_matrix[j, i] = float(np.mean(cxy))
        return coh_matrix

    def _wavelet(self, data: np.ndarray) -> np.ndarray:
        # Simplified — production uses PyWavelets db4
        # Returns approximation coefficients at level 3
        level = 3
        coeffs = data.copy()
        for _ in range(level):
            # Haar approximation (placeholder)
            coeffs = (coeffs[:, 0::2] + coeffs[:, 1::2]) / 2 if coeffs.shape[-1] > 1 else coeffs
        return coeffs
