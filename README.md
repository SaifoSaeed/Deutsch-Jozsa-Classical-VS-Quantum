# Deutsch-Jozsa: Classical VS Quantum
A Python benchmarking suite comparing the classical and quantum algorithmic
implementations of the Deutsch-Jozsa problem. This repository evaluates the oracle query
complexity and execution time overhead, showcasing the deterministic constant-time O(1)
efficiency of quantum circuits against the classical bounds.
## Overview
The Deutsch-Jozsa algorithm determines whether a hidden Boolean function (the oracle) is
**constant** or **balanced**.
- **Classical limit:** Requires up to $2^{n-1} + 1$ queries in the worst-case scenario.
- **Quantum advantage:** Resolves the function type in exactly **1 query** using quantum
parallelism and phase kickback.
This project features both local simulation via `AerSimulator` and the ability to dispatch jobs
to real IBM Quantum hardware using Qiskit Runtime primitives.
## Features
- **Classical Simulation:** Dynamically generates truth tables for randomized
constant/balanced functions and iteratively queries them.
- **Quantum Implementation:** Builds generalized $n$-qubit quantum oracles using Qiskit.
Implements the full Deutsch-Jozsa circuit with `BackendSamplerV2` and `SamplerV2`.
- **Statistical Aggregation:** Executes multiple runs ($t$) across a range of bitstring lengths
($n$) to calculate and plot the *Best*, *Worst*, and *Average* performance metrics.
- **Hardware Execution:** Supports the `--real` command-line flag to target the least-busy
operational IBM Quantum Processing Unit (QPU) via the ISA-aware Pass Manager.
## Project Structure
```text
Deutsch-Jozsa-Classical-VS-Quantum/
├── main.py # Central benchmarking script and plotting engine
└── src/
├── classical.py # Classical oracle generation and loop logic
└── quantum.py # Qiskit circuit generation and primitive execution
```
## Dependencies
Ensure you have a working Python environment. Install the required packages:
```bash
pip install numpy matplotlib qiskit qiskit-aer qiskit-ibm-runtime

```
## Usage
Run the benchmarking script from the root directory. You can specify the input register
constraints and the number of iterative tests per size.
### Local Simulation (Default)
```bash
python main.py -n 3 -x 8 -t 5
```
This will run the experiment for qubit register sizes from $n=3$ to $n=7$, repeating the
execution 5 times to gather average/worst-case statistics on the local `AerSimulator`.
### Real Hardware Execution
```bash
python main.py -r -n 3 -x 6 -t 3
```
Appending the `-r` or `--real` flag routes the quantum jobs to IBM Quantum cloud services.
> **Note:** You must have your IBMQ API credentials configured globally or cached in your
environment using `QiskitRuntimeService.save_account(...)`.
## Outputs
Upon completion, the script generates a `benchmark.png` file containing a dual-axis plot:
1. **Oracle Query Complexity:** Illustrates the divergence between classical scaling and
the flat O(1) line of the quantum algorithm.
2. **Execution Overhead:** Visualizes the wall-clock time required to prepare, transpile,
and execute the queries (capturing API overhead and Qiskit DAG compilation latency).
