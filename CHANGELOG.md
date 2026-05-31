# Changelog

All notable changes to EEG-MPI are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [2.4.1] — 2025-06-10

### Fixed
- Fixed race condition in `MessageBus.subscribe()` under high-throughput scenarios (#312)
- Corrected ICA component rejection threshold being applied before bandpass filter (#308)
- Resolved WebSocket disconnect not cleaning up VisualizationAgent subscriber (#305)
- Fixed `config.yaml` `notch` frequency being ignored when set to `60` Hz (#301)

### Changed
- Improved error messages in `BaseAgent.process()` when payload is malformed
- Updated `brainflow` dependency to 5.12.1 for improved Neurosity Crown stability

---

## [2.4.0] — 2025-05-20

### Added
- **RL-based Decision Agent**: `DecisionAgent` now supports reinforcement learning strategy via `strategy: rl_based` in config (#289)
- New `action_space` config key for `DecisionAgent` to define BCI output commands (#289)
- `VisualizationAgent` now streams topographic head maps at 30 fps via WebSocket (#281)
- Support for **Neurosity Crown** headset (beta) via BrainFlow adapter (#276)
- `--mode demo` flag for zero-hardware testing with synthetic EEG data (#274)
- Coverage badge in README; CI now uploads to Codecov on every push (#270)

### Changed
- `ClassificationAgent` ensemble upgraded: EEGNet + Transformer (previously EEGNet-only) — accuracy improved from 97.1% to 99.2% (#285)
- Message bus topic naming convention changed from `dot.separated` to `snake_case` (see migration guide in docs) (#279)
- `config.yaml` schema version bumped; old configs auto-migrated on load with deprecation warning (#271)

### Deprecated
- `ClassificationAgent(model="eegnet")` — use `model: eegnet_transformer` instead; legacy alias retained until v3.0 (#285)

### Fixed
- Memory leak in `FeatureExtractionAgent` when processing >128-channel recordings (#293)
- `PreprocessingAgent` incorrectly applying 50 Hz notch to US-region configs (#288)

---

## [2.3.2] — 2025-04-08

### Fixed
- Patch for numpy 2.0 compatibility (`np.bool` → `np.bool_`) across all agents (#261)
- Fixed `setup.py` not including `dashboard/` assets in sdist (#257)
- Corrected LSL inlet timeout causing pipeline stall on stream reconnect (#254)

---

## [2.3.0] — 2025-03-15

### Added
- **Coherence feature** in `FeatureExtractionAgent`: inter-channel coherence matrix (#240)
- Wavelet decomposition (Daubechies-4) added as optional feature extraction step (#237)
- `BaseAgent.on_error()` hook for custom error handling in subclasses (#233)
- GitHub Issue and PR templates (#229)

### Changed
- `PreprocessingAgent` now uses MNE-Python `autoreject` for epoch rejection instead of simple threshold (#243)
- Minimum Python version raised from 3.10 to 3.11 (#235)
- `requirements.txt` fully pinned to exact versions for reproducibility (#228)

### Fixed
- `FeatureExtractionAgent` entropy calculation was using natural log instead of log-base-2 (#245)
- Dashboard websocket reconnect logic now uses exponential backoff (#241)

---

## [2.2.0] — 2025-02-01

### Added
- **Multi-target classification**: `ClassificationAgent` can now predict emotion, focus, fatigue, and motor intent simultaneously (#215)
- `confidence_threshold` config key; predictions below threshold are marked `uncertain` (#212)
- Real-time power spectrum display in dashboard (#208)
- BrainFlow LSL passthrough for universal device support (#204)

### Changed
- Async rewrite of `MessageBus` using `asyncio` — latency reduced from ~120ms to <50ms (#218)
- Agent startup order is now deterministic (topological sort of subscriptions) (#210)

### Fixed
- `ClassificationAgent` model weights not loading correctly on Windows paths with spaces (#220)
- Muse S disconnection not triggering pipeline graceful shutdown (#216)

---

## [2.1.0] — 2024-12-10

### Added
- Fatigue detection model in `ClassificationAgent` (#188)
- `--channels` CLI flag for `eegmpi` entrypoint (#185)
- `examples/cognitive_load_monitor.py` (#182)

### Changed
- `VisualizationAgent` rewritten with Canvas API (removed Three.js dependency) (#191)
- Config loading now supports environment variable overrides via `EEGMPI_` prefix (#186)

### Fixed
- Band power values were not normalized per epoch length (#194)
- Fixed g.tec driver crashing on macOS 14 Sonoma (#190)

---

## [2.0.0] — 2024-10-01

### Added
- **Multi-Agent architecture** — complete rewrite from monolithic pipeline (#150)
- `BaseAgent` abstract class with `subscribe_to` / `publish_to` interface (#150)
- Redis-backed `MessageBus` for inter-agent communication (#150)
- `PreprocessingAgent`, `FeatureExtractionAgent`, `ClassificationAgent`, `DecisionAgent`, `VisualizationAgent` (#150)
- Real-time WebSocket dashboard (#155)
- `config.yaml` driven configuration (#152)
- GitHub Actions CI with matrix testing on Python 3.10–3.12 (#158)
- Full async pipeline with `asyncio` (#150)

### Changed
- Complete API break from v1.x — see [Migration Guide](docs/migration_v2.md)

### Removed
- Legacy `eeg_pipeline.py` monolithic script
- Synchronous processing mode

---

## [1.3.1] — 2024-07-14

### Fixed
- Bandpass filter order causing instability at high sample rates (#112)
- OpenBCI Cyton serial timeout on Linux (#109)

---

## [1.3.0] — 2024-06-20

### Added
- Emotion detection (valence/arousal) using DEAP-trained model (#98)
- Muse 2 and Muse S support via BLE (#94)
- `examples/emotion_detection.py` (#98)

### Changed
- Upgraded to MNE-Python 1.6.0 (#100)

---

## [1.2.0] — 2024-04-05

### Added
- Motor imagery classification (left/right hand, feet, tongue) (#78)
- `examples/motor_imagery_bci.py` (#78)
- ICA artifact removal using FastICA (#75)

---

## [1.1.0] — 2024-02-18

### Added
- g.tec g.USBamp driver (#60)
- Emotiv EPOC X support (#57)
- Band power features (delta, theta, alpha, beta, gamma) (#54)

### Fixed
- Memory usage scaling linearly with recording length (#62)

---

## [1.0.0] — 2023-12-01

### Added
- Initial release of EEG-MPI
- OpenBCI Cyton support (8-channel)
- Basic bandpass filtering and notch filter
- Alpha/beta power ratio computation
- Simple threshold-based command output
- MIT License

---

[Unreleased]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.4.1...HEAD
[2.4.1]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.3.2...v2.4.0
[2.3.2]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.3.0...v2.3.2
[2.3.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v1.3.1...v2.0.0
[1.3.1]: https://github.com/eeg-mpi/eeg-mpi/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/eeg-mpi/eeg-mpi/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/eeg-mpi/eeg-mpi/releases/tag/v1.0.0
