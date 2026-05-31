name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint (Black + isort)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-lint-${{ hashFiles('requirements.txt', 'pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-lint-

      - name: Install lint dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black==24.4.2 isort==5.13.2 ruff==0.4.4

      - name: Run Black
        run: black --check --diff agents/ core/ tests/

      - name: Run isort
        run: isort --check-only --diff agents/ core/ tests/

      - name: Run ruff
        run: ruff check agents/ core/ tests/

  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    needs: lint

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('requirements.txt', 'pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-${{ matrix.python-version }}-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e ".[dev]"

      - name: Run pytest with coverage
        env:
          REDIS_HOST: localhost
          REDIS_PORT: 6379
        run: |
          pytest tests/ \
            --cov=eegmpi \
            --cov=agents \
            --cov=core \
            --cov-report=xml \
            --cov-report=term-missing \
            -m "not slow and not gpu and not hardware" \
            -v

      - name: Upload coverage to Codecov
        if: matrix.python-version == '3.11'
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unittests
          name: eeg-mpi-coverage
          fail_ci_if_error: false
          token: ${{ secrets.CODECOV_TOKEN }}

  type-check:
    name: Type Check (mypy)
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-mypy-${{ hashFiles('requirements.txt', 'pyproject.toml') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e ".[dev]"

      - name: Run mypy
        run: mypy agents/ core/ --ignore-missing-imports
