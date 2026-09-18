"""File-name builders for results written by PyCAD.

These functions only build paths; they never touch the file system. Callers
are responsible for creating the parent directory before writing.
"""
import os

from pycad import config


def stafan_file(c_name: str, tp_count: int, code: str | None = None) -> str:
    """Path of a STAFAN measures file for circuit ``c_name`` and ``tp_count`` patterns."""
    suffix = f"-{code}" if code is not None else ""
    return os.path.join(config.STAFAN_DIR, c_name, f"{c_name}-tp{tp_count}{suffix}.stafan")


def ppsf_ci_file(c_name: str, ci: int, cpu: int, moe: float | None = None) -> str:
    """Path of a PPSF confidence-interval run log."""
    suffix = f"-moe{moe}" if moe is not None else ""
    fname = f"{c_name}-ppsf-ci{ci}-proc{cpu}{suffix}.ppsf"
    return os.path.join(config.FAULT_SIM_DIR, c_name, "ppsf", fname)
