"""Output-path helpers used by the experiment scripts in legacy/experiments.

Moved out of pycad.utils; the helpers still used by the package now live in
pycad.paths. Kept for reference only.
"""
import os

from pycad import config as cfg


def path_ppsf():
    pass


def path_ppsf_ci(c_name, ci, cpu, moe=None):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    path = os.path.join(path, "ppsf")
    if not os.path.exists(path):
        os.makedirs(path)
    if moe is None:
        fname = f"{c_name}-ppsf-ci{ci}-proc{cpu}.ppsf"
    else:
        fname = f"{c_name}-ppsf-ci{ci}-proc{cpu}-moe{moe}.ppsf"
    fname = os.path.join(path, fname)
    return fname

def path_ppsf_ci_try(c_name, ci, cpu, max_idx=20):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    path = os.path.join(path, "ppsf")

    for i in range(max_idx):
        fname = f"{c_name}-ppsf-ci{ci}-proc{cpu}-try{i}.log"
        fname = os.path.join(path, fname)
        if not os.path.exists(fname):
            break
    return fname

def path_stafan(c_name, tp):
    path = os.path.join(cfg.STAFAN_DIR, c_name)
    fname = os.path.join(path, f"{c_name}-tp{tp}.stafan")
    return fname

def path_graph_v0(c_name, tp, ci, cpu):
    if not os.path.exists(cfg.GRAPH_DIR):
        os.mkdir(cfg.GRAPH_DIR)
    fname = f"{c_name}-stafan{tp}-ci{ci}-proc{cpu}"
    fname = os.path.join(cfg.GRAPH_DIR, fname + ".gml")
    return fname 

def path_stafan_code(c_name, tp, code=None):
    path = os.path.join(cfg.STAFAN_DIR, c_name)
    if not os.path.exists(path):
        os.makedirs(path)
    if code is None:
        fname = os.path.join(path, f"{c_name}-tp{tp}.stafan")
    else:
        fname = os.path.join(path, f"{c_name}-tp{tp}-{code}.stafan")
    return fname 

def path_tpfc_pfs(c_name, tp, idx):
    path = os.path.join(cfg.FAULT_SIM_DIR, c_name)
    if not os.path.exists(path):
        os.makedirs(path)
    fname = os.path.join(path, f"tpfc-pfs-{c_name}-tp{tp}-part{idx}.csv")
    return fname

def path_tpfc_ppsf_fig(c_name, tp, ci, cpu):
    fname = f"tpfc-ppsf-{c_name}-tp{tp}-ci{ci}-proc{cpu}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname

def path_tpfc_pfs_fig(c_name, tp, times):
    fname = f"tpfc-pfs-{c_name}-tp{tp}-times{times}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname

def path_tpfc_compare(c_name, tp, tpLoad, ci, cpu, k_stafan, k_pfs):
    fname = f"tpfc-compare-{c_name}-tp{tp}-ci{ci}"
    fname += f"-tpLoad{tpLoad}-proc{cpu}-Kpfs{k_pfs}-Kstafan{k_stafan}.png"
    fname = os.path.join(cfg.FIG_DIR, fname)
    return fname
