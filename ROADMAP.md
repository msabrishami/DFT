# Roadmap

Open work items for PyCAD, roughly in priority order.

## Package
- [ ] Fix the SSTA module: `circuit_ssta.py` imports `pycad.utils` but needs the functions in
      `pycad.ssta.utils_ssta`, and `cycle`, `margin` and `cuts` are undefined names.
- [x] `pycad.atpg`: PODEM and the D-algorithm, rewritten on the current library and tested
      against exhaustive search and fault simulation (the old versions stay in `legacy/inventory`).
- [ ] Revive observation point insertion (`legacy/tpi`). It currently depends on
      `legacy/experiments` (`pd_ppsf`), which in turn imports `tpi`.
- [ ] Replace the entry-point scripts in `legacy/scripts` with a documented `pycad` CLI.
- [ ] Add type hints and docstrings to the public API; add linting (ruff) to CI.
- [ ] Decide what to do with the SSTA module (needs the `gekko` extra).

## Data
- [ ] **Move the large Verilog benchmark sets (`data/verilog/`, ~19 MB) out of git** and
      fetch them on demand with a download script. For now they stay in the repository.
- [ ] Consolidate the duplicate `data/config.py`, and tidy `data/` (translators, `.isc`,
      `.bench`, `.ckt` formats).

## Machine learning
- [ ] Turn `gnn/` into an optional example project (`pip install pycad[gnn]`) with its own
      README and no hard-coded paths.

## Documentation
- [ ] Rewrite `README.md` (the current one describes a 2019 course project).
- [ ] Add architecture notes and a quick-start tutorial.
