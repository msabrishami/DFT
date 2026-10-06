# PyCAD

PyCAD is a Python package for gate-level circuit analysis and design for test (DFT).
It reads combinational netlists and offers, on one common circuit model:

- **Logic simulation** in two-valued, three-valued (X) and bit-parallel form
- **Testability measures**: SCOAP (CC0, CC1, CO) and STAFAN (C0, C1, S, B0, B1)
- **Fault simulation** of single stuck-at faults: parallel-fault (PFS), parallel-pattern
  (PPSF, also with confidence intervals) and deductive (DFS)
- **Test generation**: PODEM and the D-algorithm
- Test pattern generation, STIL export, Verilog and `.ckt` netlist readers, and networkx graphs
  of circuits with their measures as node attributes

Statistical static timing analysis (`pycad.ssta`) and test point insertion are not part of the
stable API yet, see [ROADMAP.md](ROADMAP.md).

The package can produce test-related datasets, for example circuit graphs with SCOAP, STAFAN
and detection-probability node attributes, that are used in downstream machine learning
applications (see `gnn/`).

## Install

```bash
git clone https://github.com/msabrishami/DFT.git
cd DFT
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Python 3.11 or newer. The core depends on `numpy` and `networkx` only. The benchmark
circuits live in `data/`; set `PYCAD_DATA_DIR` to use another location.

## Quick start

```python
import os
import random

from pycad import config
from pycad.atpg import Podem
from pycad.circuit.circuit import Circuit
from pycad.circuit.dft_circuit import DFTCircuit
from pycad.fault_simulation.pfs import PFS
from pycad.fault_simulation.ppsf import PPSF

path = os.path.join(config.CKT_DIR, "c17.ckt")   # ISCAS-85 c17

# logic simulation: values of the primary outputs for one pattern
circuit = Circuit(path)
print(circuit.logic_sim([1, 0, 1, 1, 0]))                  # [1, 0]

# testability measures
dft = DFTCircuit(path)
dft.scoap()                                                # CC0, CC1, CO
random.seed(1)
dft.stafan(tp_count=1000)                                  # C0, C1, S, B0, B1
node = dft.nodes["22"]
print(node.CC0, node.CC1, node.CO, node.B1)

# fault simulation with 8 random patterns, all stuck-at faults
coverage_per_pattern, detected = PFS(dft).run(8, faults="all")
print(coverage_per_pattern[-1], len(detected))

# how many of 64 random patterns detect each fault
print(PPSF(dft).run(64, faults="all"))

# test generation
podem = Podem(circuit)
result = podem.generate("22@0")                            # node 22 stuck at 0
print(result.status, result.pattern)                       # 'X' = any value
patterns = podem.generate_test_set(fill=0)                 # whole fault list, fault dropping
print(len(patterns.patterns), len(patterns.detected))
```

Fault names are `<node>@<stuck value>`. See [docs/architecture.md](docs/architecture.md) for
how the modules fit together.

## Layout

| Path | Contents |
|---|---|
| `src/pycad/` | the package |
| `tests/` | unit tests, independent oracles and a golden regression test |
| `data/` | benchmark netlists (ISCAS-85 `.ckt`, Verilog) |
| `gnn/` | graph neural network experiments (optional, work in progress) |
| `legacy/` | earlier scripts, experiments and implementations kept for reference |

## Developers and affiliation

PyCAD development was first started by a group of graduate students at the University of
Southern California (USC), computer engineering, as a joint research project with
[The System Power Optimization and Regulation Technology (SPORT) Lab][1].

**Main developers**

- [M. Saeed Abrishami][10]
- [Ghazal Rafiei][21]

**Graduate students who worked with this platform during their EE658 course**

- [Luke Grantham][20]
- [Yang Shen][14]

**Advisors**

- [Prof. Massoud Pedram][11]
- [Prof. Shahin Nazarian][12]

[1]: http://sportlab.usc.edu/
[10]: http://sportlab.usc.edu/~msabrishami/
[11]: http://www.mpedram.com/
[12]: http://sportlab.usc.edu/~shahin/
[14]: https://www.linkedin.com/in/yshen245/
[20]: https://www.linkedin.com/in/lukegrantham/
[21]: https://github.com/ghazalrafiei

## License

MIT, see [LICENSE](LICENSE).
