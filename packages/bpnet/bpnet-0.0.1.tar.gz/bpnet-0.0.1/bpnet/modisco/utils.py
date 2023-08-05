"""Small helper-functions for used by modisco classes
"""
import pandas as pd
import numpy as np
from kipoi.readers import HDF5Reader
from bpnet.cli.contrib import ContribFile
from bpnet.functions import mean
import warnings


def bootstrap_mean(x, n=100):
    """Bootstrap the mean computation"""
    out = []

    for i in range(n):
        idx = pd.Series(np.arange(len(x))).sample(frac=1.0, replace=True).values
        out.append(x[idx].mean(0))
    outm = np.stack(out)
    return outm.mean(0), outm.std(0)


def nan_like(a, dtype=float):
    a = np.empty(a.shape, dtype)
    a.fill(np.nan)
    return a


def ic_scale(x):
    from modisco.visualization import viz_sequence
    background = np.array([0.27, 0.23, 0.23, 0.27])
    return viz_sequence.ic_scale(x, background=background)


def shorten_pattern(pattern):
    """metacluster_0/pattern_1 -> m1_p1
    """
    return pattern.replace("metacluster_", "m").replace("/", "_").replace("pattern_", "p")


def longer_pattern(shortpattern):
    """m1_p1 -> metacluster_0/pattern_1
    """
    return shortpattern.replace("_", "/").replace("m", "metacluster_").replace("p", "pattern_")


def extract_name_short(ps):
    m, p = ps.split("_")
    return {"metacluster": int(m.replace("m", "")), "pattern": int(p.replace("p", ""))}


def extract_name_long(ps):
    m, p = ps.split("/")
    return {"metacluster": int(m.replace("metacluster_", "")), "pattern": int(p.replace("pattern_", ""))}
