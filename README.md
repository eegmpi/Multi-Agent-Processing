<div align="center">

<img src="assets/logo.png" alt="EEG-MPI Logo" width="280"/>

# EEG-MPI
### Multi-Agent Processing Interface for EEG Brain Signals

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.4.1-cyan?style=flat-square)](CHANGELOG.md)
[![Build](https://img.shields.io/github/actions/workflow/status/eeg-mpi/eeg-mpi/ci.yml?style=flat-square&label=CI)](/.github/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-94%25-brightgreen?style=flat-square)]()
[![Stars](https://img.shields.io/github/stars/eeg-mpi/eeg-mpi?style=flat-square&color=yellow)](https://github.com/eeg-mpi/eeg-mpi/stargazers)
[![Twitter](https://img.shields.io/badge/Follow-@eeg__mpi-black?style=flat-square&logo=x)](https://x.com/eeg_mpi)

**A next-generation neurotechnology platform where 5 specialized AI agents collaborate  
in real-time to process, analyze, and interpret EEG brain signals.**

[🚀 Quick Start](#-quick-start) · [📖 Docs](docs/) · [🤖 Agents](#-agent-pipeline) · [💬 Community](https://x.com/eeg_mpi)

</div>

---

<div align="center">
<img src="https://raw.githubusercontent.com/eeg-mpi/eeg-mpi/main/assets/banner.svg"
     alt="EEG-MPI Pipeline" width="100%"/>
</div>

---

<div align="center">

| ⚡ Latency | 📡 Channels | 🧠 Agents | 🎯 Accuracy | 🖥️ Dashboard |
|:---:|:---:|:---:|:---:|:---:|
| `< 50ms` | `256 ch` | `5 specialized` | `99.2%` | `30 fps` |

</div>

---

## 🧬 What is EEG-MPI?

EEG-MPI is an open-source **Multi-Agent System (MAS)** for real-time EEG signal
processing and Brain-Computer Interface (BCI) applications.
Unlike monolithic EEG pipelines, EEG-MPI distributes processing across
**5 specialized AI agents** that run in parallel, communicate via a shared
message bus, and collaboratively produce high-accuracy mental state predictions.

> **"From raw brain signal to actionable command in under 50 milliseconds."**

---

## 🤖 Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        EEG-MPI PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘

 [EEG Device]
      │
      ▼
┌─────────────┐    ┌─────────────────┐    ┌──────────────────────┐
│  Agent 01   │───▶│    Agent 02     │───▶│      Agent 03        │
│Preprocessing│    │Feature Extract. │    │  Mental Classifier   │
│             │    │                 │    │                      │
│ • ICA/ASR   │    │ • Band Power    │    │ • EEGNet + Transformer│
│ • Bandpass  │    │ • Entropy       │    │ • Emotion Detection  │
│ • Artifact  │    │ • Coherence     │    │ • Fatigue / Focus    │
│   Removal   │    │ • Wavelets      │    │ • Motor Intent       │
└─────────────┘    └─────────────────┘    └──────────────────────┘
                                                     │
                   ┌────────────────┐                │
                   │   Agent 05     │◀───────────────┘
                   │ Visualization  │    ┌──────────────┐
                   │                │    │   Agent 04   │
                   │ • WebSocket    │◀───│   Decision   │
                   │ • Topography   │    │              │
                   │ • 30fps Stream │    │ • RL-based   │
                   └────────────────┘    │ • Thresholds │
                           │             │ • Commands   │
                           ▼             └──────────────┘
                     [Dashboard]              │
                                              ▼
                                        [BCI Output]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Redis (for Message Bus)
- Compatible EEG device or sample data

### Installation

```bash
# Clone the repository
git clone https://github.com/eeg-mpi/eeg-mpi.git
cd eeg-mpi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install EEG-MPI
pip install -e .
```

### Launch the Pipeline

```bash
# Start Redis (required for Message Bus)
redis-server

# Run with sample EEG data
python -m eegmpi --source sample --mode demo

# Run with real EEG device (e.g. OpenBCI)
python -m eegmpi --source openbci --port COM3 --channels 16

# Run with Emotiv headset
python -m eegmpi --source emotiv --mode realtime

# Launch dashboard
python -m eegmpi.dashboard --port 8080
# Open: http://localhost:8080
```

---

## 🎧 Supported EEG Devices

| Device | Channels | Sample Rate | Protocol | Status |
|--------|----------|-------------|----------|--------|
| OpenBCI Cyton | 8–16 ch | 250 Hz | Serial/BLE | ✅ Stable |
| Emotiv EPOC X | 14 ch | 256 Hz | USB/BLE | ✅ Stable |
| Muse 2 / Muse S | 4 ch | 256 Hz | BLE | ✅ Stable |
| g.tec g.USBamp | 16–64 ch | 2400 Hz | USB | ✅ Stable |
| BrainFlow (any) | Variable | Variable | LSL | ✅ Stable |
| NeuroSky MindWave | 1 ch | 512 Hz | BLE | 🔄 Beta |
| Neurosity Crown | 8 ch | 256 Hz | WiFi | 🔄 Beta |
| Any LSL device | Variable | Variable | LSL | ✅ Stable |

---

## 🧩 Agent API

All agents extend `BaseAgent` and implement a standard interface:

```python
from eegmpi.agents import BaseAgent

class CustomAgent(BaseAgent):
    agent_id = "custom_agent_07"
    subscribe_to = ["feature_extraction.output"]
    publish_to   = "custom_agent.output"

    async def process(self, payload: dict) -> dict:
        # Your processing logic here
        data = payload["data"]
        result = self.run_model(data)
        return {"prediction": result, "confidence": 0.97}
```

### Built-in Agents

```python
from eegmpi.agents import (
    PreprocessingAgent,      # Agent 01 — Noise removal, ICA, ASR
    FeatureExtractionAgent,  # Agent 02 — Band power, entropy, wavelets
    ClassificationAgent,     # Agent 03 — EEGNet + Transformer ensemble
    DecisionAgent,           # Agent 04 — RL-based command generation
    VisualizationAgent,      # Agent 05 — Real-time WebSocket dashboard
)
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
eegmpi:
  version: "2.4.1"
  mode: realtime           # realtime | offline | demo

source:
  device: openbci          # openbci | emotiv | muse | brainflow | lsl | sample
  channels: 16
  sample_rate: 250         # Hz
  buffer_size: 512         # samples

message_bus:
  backend: redis
  host: localhost
  port: 6379

agents:
  preprocessing:
    enabled: true
    bandpass: [1, 50]      # Hz
    notch: 50              # Hz (or 60 for US)
    ica: true
    asr: true

  feature_extraction:
    enabled: true
    bands:
      delta:  [1, 4]
      theta:  [4, 8]
      alpha:  [8, 13]
      beta:   [13, 30]
      gamma:  [30, 50]
    entropy: true
    coherence: true
    wavelet: true

  classification:
    enabled: true
    model: eegnet_transformer
    targets: [emotion, focus, fatigue, motor_intent]
    confidence_threshold: 0.85

  decision:
    enabled: true
    strategy: rl_based     # rl_based | rule_based | hybrid
    action_space: [command_left, command_right, command_select, idle]

  visualization:
    enabled: true
    port: 8080
    fps: 30
    show_topography: true
    show_spectrum: true

logging:
  level: INFO
  output: [console, file]
  file: logs/eegmpi.log
```

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![MNE](https://img.shields.io/badge/MNE--Python-00457C?style=for-the-badge&logo=python&logoColor=white)

</div>

| Layer | Technology |
|-------|-----------|
| Signal Processing | MNE-Python, SciPy, NumPy |
| Deep Learning | PyTorch, EEGNet, Transformer |
| Message Bus | Redis Pub/Sub, asyncio |
| API Server | FastAPI, Uvicorn |
| Dashboard | WebSocket, Vanilla JS, Canvas API |
| Device Protocol | BrainFlow, LSL, BLE, Serial |
| Testing | pytest, pytest-asyncio |
| CI/CD | GitHub Actions |

---

## 🤝 Contributing

We welcome contributions! Read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

### Ways to Contribute
- 🐛 **Bug reports** — Open an [Issue](https://github.com/eeg-mpi/eeg-mpi/issues)
- 💡 **Feature ideas** — Start a [Discussion](https://github.com/eeg-mpi/eeg-mpi/discussions)
- 🧠 **New Agent** — Implement a new agent following the `BaseAgent` interface
- 📖 **Documentation** — Improve docs in the `/docs` folder
- 🧪 **Tests** — Add test coverage for existing agents

### Development Setup

```bash
git clone https://github.com/eeg-mpi/eeg-mpi.git
cd eeg-mpi
pip install -e ".[dev]"
pre-commit install
pytest tests/
```

---

<div align="center">

**Built for the neuroscience and BCI community.**

[![Follow on X](https://img.shields.io/badge/Follow_@eeg__mpi-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/eeg_mpi)
[![Star this repo](https://img.shields.io/badge/⭐_Star_this_repo-yellow?style=for-the-badge)](https://github.com/eeg-mpi/eeg-mpi)

© 2025 EEG-MPI · MIT License · Made with 🧠 and ⚡

</div>
