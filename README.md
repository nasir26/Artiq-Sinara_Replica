# ARTIQ–Sinara Replica

A software replica of the [ARTIQ](https://m-labs.hk/artiq/) (Advanced Real-Time Infrastructure for Quantum physics) experiment control framework, developed for quantum hardware prototyping and algorithm validation at **C-DAC Noida**.

> **Author:** Nasir Ali  
> **Affiliation:** C-DAC Noida / MSc Physics, Jawaharlal Nehru University  
> **ARTIQ Release:** 8 (via Nix flake)

---

## Overview

ARTIQ is the leading open-source control system for trapped-ion and other quantum hardware experiments. This repository contains:

- A **Nix-based reproducible environment** (ARTIQ release-8 + scientific Python stack)
- **Experiment scripts** covering TTL I/O, DDS, DMA, datasets, and scan infrastructure
- A **comprehensive test suite** validating all major ARTIQ features in software (no hardware required)
- **Visualisation scripts** that generate publication-quality plots for quantum physics experiments

---

## Repository Structure

```
artiq/
├── flake.nix                     # Nix environment — ARTIQ 8 + numpy/scipy/matplotlib
├── flake.lock                    # Pinned dependency graph
├── device_db.py                  # Virtual device database (TTL, DDS, core, DMA)
│
├── hello_world.py                # Minimal sanity-check experiment
├── session1.py                   # Parallel pulse sequencing with at_mu / now_mu
├── sess.py                       # TTL toggle session
├── sess1.py                      # Extended TTL session
├── session4_dma.py               # DMA (Direct Memory Access) pulse playback
│
├── arguments_test.py             # EnvExperiment argument type coverage
├── dataset_test.py               # Dataset read/write/broadcast lifecycle
├── scan_test.py                  # RangeScan / GridScan infrastructure
├── inint.py                      # Initialisation utilities
│
├── artiq_comprehensive_tests.py  # Full test suite — 10+ feature tests, no hardware
├── artiq_visual_tests.py         # Matplotlib visualisations of quantum experiments
│
└── plots/                        # Pre-generated output figures
    ├── rabi_oscillation.png
    ├── ramsey_interference.png
    ├── bloch_sphere.png
    ├── quantum_gates.png
    ├── state_tomography.png
    ├── ttl_sequences.png
    ├── dds_waveforms.png
    ├── 2d_scan_heatmaps.png
    └── performance_dashboard.png
```

---

## Environment Setup

This project uses [Nix](https://nixos.org/) for a fully reproducible environment.

### Prerequisites

- Nix with flakes enabled (`~/.config/nix/nix.conf`: `experimental-features = nix-command flakes`)

### Enter the environment

```bash
nix develop
```

This pulls ARTIQ release-8 from the M-Labs binary cache and drops you into a shell with `artiq`, `numpy`, `scipy`, `matplotlib`, and `pandas` available.

### Run an experiment (software simulation)

```bash
# Basic hello world
python hello_world.py

# Comprehensive test suite (no hardware needed)
python artiq_comprehensive_tests.py

# Generate all visualisation plots
python artiq_visual_tests.py
```

---

## Experiment Highlights

### Parallel Pulse Sequencing — `session1.py`

Demonstrates ARTIQ's precise timeline control using `now_mu()` / `at_mu()` to schedule overlapping TTL pulses on separate channels simultaneously.

### DMA Playback — `session4_dma.py`

Records a pulse sequence to the core device's Direct Memory Access buffer and replays it with deterministic sub-nanosecond timing — the standard technique for repeated pulse patterns in quantum gate experiments.

### Comprehensive Test Suite — `artiq_comprehensive_tests.py`

Covers:
| # | Test | What it validates |
|---|------|-------------------|
| 01 | Basic Structure | Experiment lifecycle: `build → prepare → run → analyze` |
| 02 | Argument Types | `NumberValue`, `StringValue`, `BooleanValue`, `EnumerationValue` |
| 03 | Dataset API | `set_dataset`, `get_dataset`, broadcast and persistence flags |
| 04 | Scan Infrastructure | `RangeScan`, `GridScan`, scan point generation |
| 05 | Scheduler API | Priority queues, pipeline stages |
| 06 | Exception Handling | ARTIQ-specific exception propagation |
| 07 | Units & Constants | `us`, `ns`, `MHz`, `dB` SI prefixes |
| 08 | Parallel Sections | `parallel` / `sequential` context managers |
| 09 | DMA API | Record, erase, playback |
| 10 | NumPy Integration | Array operations inside ARTIQ experiments |

### Visualisation — `artiq_visual_tests.py`

Generates nine plots including Rabi oscillations, Ramsey interference fringes, Bloch sphere trajectories, quantum gate matrices, state tomography density matrices, TTL timing diagrams, DDS waveforms, 2-D parameter scan heatmaps, and a performance dashboard.

---

## Device Database

`device_db.py` defines a virtual Sinara-compatible device set:

| Device | Type | Description |
|--------|------|-------------|
| `core` | Core | RISC-V (rv32g) soft-core, 1 ns ref period |
| `core_cache` | CoreCache | Key–value cache on core device |
| `core_dma` | CoreDMA | Direct memory access controller |
| `ttl0`–`ttl1` | TTLOut | Digital output channels |

---

## Relation to Real Sinara Hardware

This replica targets software-level compatibility with the Sinara hardware ecosystem:

| Sinara board | Emulated by |
|---|---|
| Kasli (core) | `device_db.py` core entry, `rv32g` target |
| BNC TTL | `TTLOut` channels `ttl0`, `ttl1` |
| Urukul DDS | *(planned)* |
| Phaser RF | *(planned)* |

---

## License

Developed for research purposes at C-DAC Noida. ARTIQ itself is licensed under LGPL-3.0 by M-Labs Ltd.
