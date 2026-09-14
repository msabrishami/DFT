# Roadmap

Open work items for PyCAD, roughly in priority order.

## Package
- [ ] Fix deductive fault simulation (`pycad.fault_simulation.deductive_fs`): the DFT node
      classes have no `dfs()` method, so `DFS.single()` raises `AttributeError`.
- [ ] Port the best D-algorithm / PODEM / ATPG implementation from `legacy/inventory` into
      the package, with tests (several near-duplicate versions exist there).
- [ ] Revive observation point insertion (`legacy/tpi`). It currently depends on
      `legacy/experiments` (`pd_ppsf`), which in turn imports `tpi`.
- [ ] Replace the entry-point scripts in `legacy/scripts` with a documented `pycad` CLI.
- [ ] Remove debugging hooks (`import IPython`, `pdb`) from `pycad.node`.
- [ ] Stop fault simulators creating `data/fault_sim/<circuit>` directories as a side effect
      of construction.
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
