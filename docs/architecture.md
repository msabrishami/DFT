# Architecture

PyCAD is built in layers; each layer only uses the ones above it in this list.

| Layer | Module | Role |
|---|---|---|
| Foundations | `pycad.config`, `pycad.paths`, `pycad.utils` | data locations, constants, helpers |
| Gates | `pycad.node.node` | `Node` and one class per gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUFF, BRCH, IPT) |
| Netlists | `pycad.circuit.circuit_loader`, `pycad.circuit.circuit`, `pycad.circuit.convert` | read `.ckt` and Verilog, levelize, logic simulation |
| Patterns and faults | `pycad.tp_generator`, `pycad.fault_simulation.fault` | test patterns, `Fault` and `FaultList` |
| Testability | `pycad.node.dft_node`, `pycad.circuit.dft_circuit` | SCOAP and STAFAN |
| Fault simulation | `pycad.fault_simulation` (`pfs`, `ppsf`, `deductive_fs`) | single stuck-at fault simulators |
| Test generation | `pycad.atpg` | PODEM and the D-algorithm |

## Circuit model

A netlist becomes a graph of `Node` objects (`unodes` are fan-in, `dnodes` fan-out). Nets
with fan-out get explicit *branch* nodes (`BRCH`, node type `FB`), so every stuck-at fault
site is a node. `DFTNode` and `DFTCircuit` extend `Node` and `Circuit` with the testability
measures and the data the fault simulators need.

## Simulation modes

Every gate implements three evaluation modes: binary (`imply`), ternary with `X` for
unknown (`imply_t`, built on `eval_t`) and bit-parallel (`imply_b`), where each bit of an
integer is a separate pattern or fault. `Circuit.logic_sim`, `logic_sim_t` and
`logic_sim_bitwise` apply them to a whole circuit.

## Fault simulators

- `PFS`: one pattern at a time, one fault per bit (the good circuit is bit 63).
- `PPSF`: one fault at a time, one pattern per bit. `run_ci` estimates detection
  probabilities of faults with confidence intervals, using several processes.
- `DFS`: deductive simulation with fault lists.

The three simulators agree with each other and with a brute-force fault injection through
`Circuit.logic_sim_bitwise`; the tests check this.

## Test generation

`Podem` assigns primary inputs only and works on the cone of the fault. `DAlgorithm`
assigns any node, with forward and backward implication. Both return an `AtpgResult` (status
`detected`, `redundant` or `aborted`, and a pattern with `X` for free inputs) and can build a
whole test set with fault dropping.

## Testing

`tests/test_regression.py` compares results with `tests/golden/baseline.json` (seed 42).
Other tests use independent oracles: the hand-written c17 in `tests/c17_oracle.py`, a
hand-computed SCOAP table and exhaustive search over small circuits.
