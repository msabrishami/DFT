# Roadmap

Open work items for PyCAD, roughly in priority order.

## Package
- [ ] Revive test point insertion (`legacy/tpi`). It depends on `legacy/experiments`
      (`pd_ppsf`), which in turn imports `tpi`.
- [ ] Fix the SSTA module: `circuit_ssta.py` imports `pycad.utils` but needs the functions in
      `pycad.ssta.utils_ssta`, and `cycle`, `margin` and `cuts` are undefined names. Needs the
      `gekko` extra; decide whether it stays in the package.
- [ ] A documented `pycad` command line (pfs, ppsf, ppsf-ci, stafan-save, lev-backward) to
      replace the scripts in `legacy/scripts`.
- [ ] Type hints for the public API.

## Paused from the 2.0.0 clean-up
- [ ] Speedups that keep results identical: STAFAN counting 64 patterns at a time, PPSF
      re-simulating from the fault site, cached simulation dispatch, incremental simulation
      and an X-path check in PODEM.
- [ ] API consistency: one logging argument (`log_fname`/`log_dir`), `paths` helpers for the
      STAFAN/SCOAP/pattern files, enum comparisons of gate and node types instead of strings,
      `logic_sim_file` through `TPGenerator`, a `Circuit.detects` helper.
- [ ] SCOAP for XOR/XNOR gates with more than two inputs; Windows support for the
      fork-based `pycad.parallel`.
- [ ] Remove SSTA-only node fields and unused `config` constants together with the SSTA work.

## Data
- [ ] **Move the large Verilog benchmark sets (`data/verilog/`, ~19 MB) out of git** and
      fetch them on demand with a download script. For now they stay in the repository.
- [ ] Consolidate the duplicate `data/config.py` (still used by `data/download_data.py` for
      its circuit lists), and tidy `data/` (translators, `.isc`, `.bench`, `.ckt` formats).

## Machine learning
- [ ] Turn `gnn/` into an optional example project (`pip install pycad[gnn]`) with its own
      README and no hard-coded paths.

## Documentation
- [x] README, architecture notes and a tested quick start.
- [ ] A longer tutorial and API reference.
