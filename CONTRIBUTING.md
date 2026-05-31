# Contributing to EEG-MPI

Thank you for your interest in contributing to EEG-MPI! This document outlines the process for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Branch Naming](#branch-naming)
- [Pull Request Process](#pull-request-process)
- [Agent Development Tutorial](#agent-development-tutorial)
- [Testing](#testing)

---

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/). Be respectful and inclusive in all interactions.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/eeg-mpi.git
   cd eeg-mpi
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/eeg-mpi/eeg-mpi.git
   ```

---

## Development Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest tests/ -v
```

### Dev dependencies include:
- `black` — code formatter
- `isort` — import sorter
- `mypy` — static type checker
- `pytest` + `pytest-asyncio` + `pytest-cov` — testing
- `pre-commit` — git hooks

---

## Code Style

### Formatting — Black

All code must be formatted with [Black](https://black.readthedocs.io/) (line length: 88):

```bash
black agents/ core/ tests/
```

### Imports — isort

Imports must be sorted with [isort](https://pycqa.github.io/isort/) (Black-compatible profile):

```bash
isort agents/ core/ tests/
```

### Type Hints

All public functions and methods **must** include type annotations:

```python
# Good
async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
    ...

# Bad
async def process(self, payload):
    ...
```

### Docstrings

Use Google-style docstrings for all public classes and methods:

```python
class PreprocessingAgent(BaseAgent):
    """Handles EEG signal preprocessing including ICA and artifact removal.

    Args:
        config: Agent configuration dictionary.
        bus: Shared message bus instance.

    Attributes:
        bandpass: Tuple of (low_freq, high_freq) in Hz.
    """
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| New feature / agent | `feature/<description>` | `feature/gamma-band-agent` |
| Bug fix | `fix/<issue-id>` | `fix/issue-142` |
| Documentation | `docs/<description>` | `docs/api-reference-update` |
| Refactor | `refactor/<description>` | `refactor/message-bus-async` |
| Tests | `test/<description>` | `test/classification-coverage` |
| Release | `release/<version>` | `release/2.5.0` |

---

## Pull Request Process

### Before Opening a PR

- [ ] Branch is up-to-date with `main` or `develop`
- [ ] All tests pass: `pytest tests/ --cov=eegmpi`
- [ ] Code is formatted: `black --check .` and `isort --check .`
- [ ] Type hints added and `mypy` passes
- [ ] Docstrings written for new public APIs
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] New agents include at least one unit test

### PR Checklist (copy into your PR description)

```markdown
## PR Checklist
- [ ] Tests pass (`pytest tests/`)
- [ ] Black + isort formatting applied
- [ ] Type hints added
- [ ] Docstrings written
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or clearly documented)
- [ ] Screenshots / output attached (if UI change)
```

### Review Process

1. At least **1 approving review** required for `develop`
2. At least **2 approving reviews** required for `main`
3. CI must pass (lint + tests on Python 3.10, 3.11, 3.12)

---

## Agent Development Tutorial

### Step 1 — Subclass `BaseAgent`

```python
# agents/my_agent.py
from __future__ import annotations
from typing import Any
from .base_agent import BaseAgent


class MyCustomAgent(BaseAgent):
    """One-line summary of what this agent does.

    Subscribes to the output of FeatureExtractionAgent and
    publishes enriched features with custom metadata.
    """

    agent_id = "my_custom_agent"
    subscribe_to = ["feature_extraction.output"]
    publish_to = "my_custom_agent.output"

    def __init__(self, config: dict[str, Any], bus: Any) -> None:
        super().__init__(config, bus)
        self.threshold: float = config.get("threshold", 0.75)

    async def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Core processing logic.

        Args:
            payload: Dict containing 'data', 'timestamp', 'channel_names'.

        Returns:
            Dict with 'result', 'confidence', and 'metadata'.
        """
        data = payload["data"]
        result = self._run_my_model(data)
        return {
            "result": result,
            "confidence": 0.92,
            "metadata": {"threshold_used": self.threshold},
        }

    def _run_my_model(self, data: Any) -> Any:
        # Your implementation here
        return data
```

### Step 2 — Register in `agents/__init__.py`

```python
from .my_agent import MyCustomAgent

__all__ = [
    "PreprocessingAgent",
    "FeatureExtractionAgent",
    "ClassificationAgent",
    "DecisionAgent",
    "VisualizationAgent",
    "MyCustomAgent",  # Add this
]
```

### Step 3 — Write a test

```python
# tests/test_my_agent.py
import pytest
from agents.my_agent import MyCustomAgent


@pytest.fixture
def agent(mock_bus):
    config = {"threshold": 0.80}
    return MyCustomAgent(config, mock_bus)


@pytest.mark.asyncio
async def test_process_returns_result(agent):
    payload = {"data": [0.1, 0.2, 0.3], "timestamp": 1234567890.0}
    output = await agent.process(payload)
    assert "result" in output
    assert "confidence" in output
    assert 0.0 <= output["confidence"] <= 1.0
```

### Step 4 — Add config block in `config.yaml`

```yaml
agents:
  my_custom_agent:
    enabled: true
    threshold: 0.80
```

---

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=eegmpi --cov-report=term-missing

# Run only fast unit tests (exclude slow integration tests)
pytest tests/ -m "not slow"

# Run a specific test file
pytest tests/test_preprocessing.py -v
```

### Test markers

| Marker | Usage |
|--------|-------|
| `@pytest.mark.slow` | Long-running / integration tests |
| `@pytest.mark.asyncio` | Async test functions |
| `@pytest.mark.gpu` | Tests requiring a GPU |

---

## Questions?

Open a [Discussion](https://github.com/eeg-mpi/eeg-mpi/discussions) or reach out on [X @eeg_mpi](https://x.com/eeg_mpi).
