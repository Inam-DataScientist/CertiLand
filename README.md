# CertiLand

### Shielded Reinforcement Learning with Temporal-Logic Verification

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-supported-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-supported-8CAAE6?logo=scipy&logoColor=white)](https://scipy.org/)
[![Tests](https://img.shields.io/badge/tests-49-passing-success)](#testing)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)](.github/workflows/ci.yml)
[![CPU](https://img.shields.io/badge/runtime-CPU%20only-lightgrey)](#installation)

</div>

---

## Overview

**CertiLand** is a self-contained Python implementation for experimenting with:

- temporal-logic specifications
- LTL formula processing
- monitor construction
- safety-shield synthesis
- shielded reinforcement learning
- CTL/PCTL verification
- statistical model checking
- counterexample generation
- reproducible experiments

The repository is intentionally lightweight and runs on **CPU using NumPy/SciPy**.

No external training dataset is required.

---

## Project Structure

```text
SafeLand/
│
├── src/
│   └── safeland/
│       │
│       ├── config.py
│       │
│       ├── world.py
│       │
│       ├── product.py
│       │
│       ├── shield.py
│       │
│       ├── rl.py
│       │
│       ├── verification.py
│       │
│       ├── experiment.py
│       │
│       ├── plots.py
│       │
│       └── logic/
│           ├── ltl.py
│           ├── ctl.py
│           └── pctl.py
│
├── tests/
│
├── configs/
│   └── default.yaml
│
├── scripts/
│   └── reproduce.sh
│
├── results/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── pyproject.toml
├── LICENSE
└── README.md
````

---

# Modules

## `src/safeland/config.py`

Configuration management.

Provides:

* validated configuration objects
* YAML configuration loading
* command-line overrides
* reproducible configuration handling

Example:

```text
--set world.wind_prob=0.4
--set rl.episodes=50000
```

---

## `src/safeland/world.py`

Defines the environment and transition dynamics used by the experiments.

The environment includes:

* UAV position
* altitude
* battery state
* wind
* no-fly regions
* buildings
* geofence
* landing locations
* terminal states

---

## `src/safeland/logic/ltl.py`

LTL processing utilities.

Includes:

* LTL syntax
* parsing
* formula progression
* simplification
* monitor construction

---

## `src/safeland/logic/ctl.py`

CTL processing and explicit-state model checking.

Supports the main CTL operators used by the verification pipeline, including:

```text
EX
AX
EU
AU
EG
AG
EF
AF
```

---

## `src/safeland/logic/pctl.py`

PCTL utilities for discrete-time Markov chains.

Includes support for:

* until properties
* bounded until
* globally-style properties
* reachability probabilities
* expected steps

---

## `src/safeland/product.py`

Constructs the product between the environment and the temporal-logic
monitor.

The resulting structure is used by the shield and verification components.

---

## `src/safeland/shield.py`

Safety-shield implementation.

Includes:

* shield synthesis
* sure shields
* probabilistic shields
* allowed-action computation
* certificate generation
* reserve-map generation

---

## `src/safeland/rl.py`

Reinforcement-learning implementation.

The current implementation provides:

* tabular Q-learning
* shield-aware action selection
* ε-greedy exploration
* constrained action selection
* deterministic training support

No external dataset is required for training.

---

## `src/safeland/verification.py`

Verification and certification utilities.

Includes:

* closed-loop DTMC construction
* closed-loop Kripke structures
* CTL verification
* PCTL verification
* statistical model checking
* counterexample generation

---

## `src/safeland/experiment.py`

Experiment runner.

Provides:

* multiple random seeds
* multiple methods
* experiment configuration
* result collection
* confidence intervals
* summary tables
* reproducible artifacts

---

## `src/safeland/plots.py`

Plotting utilities.

Figures are generated from stored experiment results rather than from
hard-coded values.

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd SafeLand
```

---

## 2. Create an environment

Using Conda:

```bash
conda create -n safeland python=3.10 -y
conda activate safeland
```

Or use any compatible Python environment.

---

## 3. Install the package

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

---

# Quick Start

After installation, run the test suite:

```bash
pytest
```

Then inspect the temporal-logic monitor:

```bash
python -m safeland spec
```

Run the default experiment:

```bash
python -m safeland run --set experiment.name=main
```

Summarize an existing experiment:

```bash
python -m safeland summarize results/main
```

Regenerate figures:

```bash
python -m safeland plot results/main
```

---

# Usage

## Run an Experiment

The main experiment entry point is:

```bash
python -m safeland run
```

The default configuration is:

```text
configs/default.yaml
```

A different experiment name can be supplied with:

```bash
python -m safeland run \
    --set experiment.name=main
```

---

## Override Configuration Values

Configuration values can be changed without modifying source code.

For example:

```bash
python -m safeland run \
    --set world.wind_prob=0.4 \
    --set rl.episodes=50000
```

Multiple values can be supplied in the same command.

---

## Change the Temporal Specification

The specification can also be supplied through configuration overrides.

For example:

```bash
python -m safeland run \
    --set 'spec.safety_ltl=G(!crash & !nfz) & G(low -> F[<=5] landed)'
```

Malformed formulas and unknown atomic propositions are rejected by the
configuration and parsing layer.

---

# Shield Generation

Generate the configured shield and its associated artifacts:

```bash
python -m safeland shield
```

This produces the shield information used by the subsequent learning and
verification stages.

---

# Temporal-Logic Monitor

To inspect the monitor generated from the configured specification:

```bash
python -m safeland spec
```

This command is useful for checking the parsed specification and monitor
construction independently of the learning pipeline.

---

# Verification

The repository provides verification utilities for the learned policy.

The verification pipeline can construct the corresponding closed-loop
structures and evaluate the configured properties.

The relevant implementation is located at:

```text
src/safeland/verification.py
```

The verification module also supports counterexample generation when a
configured property does not hold.

---

# Reproducibility

The repository includes a complete reproduction script:

```bash
bash scripts/reproduce.sh
```

The script provides a convenient way to execute the configured experiment
workflow.

For individual stages, the commands can also be executed manually.

---

# Experiment Outputs

Each experiment stores its configuration and generated artifacts under the
selected results directory.

A typical experiment directory contains:

```text
results/<experiment>/
│
├── config.yaml
├── environment.json
├── shields.json
├── baselines.json
│
└── <seed>/
    ├── metrics.json
    ├── train_curve.csv
    └── policy.npy
```

### `config.yaml`

Stores the configuration used for the run, including the configuration digest.

### `environment.json`

Stores environment and software information associated with the experiment.

### `shields.json`

Stores shield synthesis information and certificate data.

### `baselines.json`

Stores baseline configuration and results.

### `metrics.json`

Stores per-run evaluation metrics.

### `train_curve.csv`

Stores training curves in tabular form.

### `policy.npy`

Stores the resulting policy representation.

---

# Testing

The repository includes an automated test suite.

Run:

```bash
pytest
```

The tests cover the main components of the implementation, including:

* temporal-logic processing
* formula progression
* CTL operators
* PCTL calculations
* product construction
* shield synthesis
* certificate validation
* transition dynamics
* reinforcement-learning behavior
* verification
* statistical model checking
* reproducibility

The repository also includes continuous integration:

```text
.github/workflows/ci.yml
```

---

# Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run the complete test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/<test_file>.py
```

For development, it is recommended to run the test suite after modifying
logic, shield, learning, or verification components.

---

# Configuration

The default configuration is located at:

```text
configs/default.yaml
```

Configuration is intentionally kept separate from the implementation.

This allows experiments to be modified without changing the source code.

The main configurable components include:

```text
world
spec
rl
experiment
```

Additional configuration fields can be inspected directly in:

```text
configs/default.yaml
```

---

# Reproducible Artifacts

For each experiment, the repository records the configuration and generated
artifacts required to inspect the run.

A recommended workflow is:

```text
Configuration
      │
      ▼
Shield Generation
      │
      ▼
RL Training
      │
      ▼
Verification
      │
      ▼
Saved Results
      │
      ├── Metrics
      ├── Training Curves
      ├── Policy
      ├── Certificates
      └── Summary Tables
```

---

# Minimal Command Reference

| Task                             | Command                                       |
| -------------------------------- | --------------------------------------------- |
| Install                          | `pip install -e .`                            |
| Install development dependencies | `pip install -e ".[dev]"`                     |
| Run tests                        | `pytest`                                      |
| Print specification/monitor      | `python -m safeland spec`                     |
| Generate shield                  | `python -m safeland shield`                   |
| Run experiment                   | `python -m safeland run`                      |
| Override configuration           | `python -m safeland run --set key=value`      |
| Summarize results                | `python -m safeland summarize results/<name>` |
| Generate plots                   | `python -m safeland plot results/<name>`      |
| Reproduce workflow               | `bash scripts/reproduce.sh`                   |

---

# Repository Design

The implementation is organized around the following software flow:

```text
Environment
     │
     ▼
Temporal Specification
     │
     ▼
Logic Monitor
     │
     ▼
Product Model
     │
     ▼
Shield
     │
     ▼
Reinforcement Learning
     │
     ▼
Closed-Loop Verification
     │
     ▼
Experiment Artifacts
```

Each stage is implemented as a separate module so that it can be inspected,
tested, and executed independently.

---

# Requirements

The implementation is designed for a standard Python environment and uses
NumPy/SciPy-based computation.

No external dataset is required.

For the exact package versions used for a particular release, refer to:

```text
pyproject.toml
```

---

# License

See [`LICENSE`](LICENSE) for the license applicable to this repository.

---

<div align="center">

### SafeLand

**Formal Logic · Safety Shielding · Reinforcement Learning · Verification**

</div>
