# Changelog

## 2.0.0

A renovation of the whole repository. The code before it is tagged `legacy-v0`.

### Package
- `src/pycad` layout with `pyproject.toml`, MIT license, Python 3.11+, CI on 3.11 to 3.13.
- PEP 8 names throughout (for example `scoap_cc`, `stafan_b`, `logic_sim_bitwise`); the
  old names are gone and there are no aliases.
- Gates (`pycad.node`): `GateType` and `NodeType` enums; one table of gate semantics shared by
  binary, ternary (`eval_t`) and bit-parallel evaluation.
- Netlists: Verilog and `.ckt` loading with checks, levelization with loop detection, outputs in
  declaration order.
- `TPGenerator` for random, exhaustive, partial and file patterns.
- SCOAP and STAFAN (multi-process, reproducible with a seed), STAFAN fault coverage estimate.
- Fault simulation: PFS, PPSF with confidence intervals, and a rewritten deductive simulator;
  all cross-checked against brute-force fault injection.
- New `pycad.atpg` with PODEM and the D-algorithm.
- Large helper and experiment code moved to `legacy/`; nothing was deleted.

### Fixed
- SCOAP and STAFAN crashed on logic that reaches no output; a primary output with fan-out got a
  nonzero observability; PPSF confidence-interval runs converged too early with one process
  and could lose their log; faults on unknown nodes and empty pattern lists are rejected
  instead of being ignored; Verilog outputs follow the declaration order; `stafan_fc` works
  after `stafan_c` and `stafan_b`.

### Testing
- 390+ tests: unit tests per gate and layer, a golden regression test, independent oracles
  (hand-written c17, hand-computed SCOAP, exhaustive search) and a README check.
