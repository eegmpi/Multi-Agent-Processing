name: Tests

on:
  schedule:
    # Run full test suite (including slow tests) every night at 02:00 UTC
    - cron: "0 2 * * *"
  workflow_dispatch:
    inputs:
      run_slow:
        description: "Include slow / integration tests"
        required: false
        default: "true"
        type: boolean

jobs:
  full-test-suite:
    name: Full Tests (Python ${{ matrix.python-version }}, ${{ matrix.os }})
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
        os: [ubuntu-latest, macos-latest, windows-latest]

    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e ".[dev]"

      - name: Run full test suite
        run: |
          pytest tests/ \
            --cov=eegmpi --cov=agents --cov=core \
            --cov-report=xml \
            -m "not gpu and not hardware" \
            -v --tb=long

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: full-suite
          token: ${{ secrets.CODECOV_TOKEN }}
