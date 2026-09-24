"""Test patterns: random and exhaustive generation, partial patterns, and files.

A test pattern is a list with one value per primary input, in the order of
``circuit.inputs``. Values are ``0`` and ``1`` and, for ternary patterns,
``config.X_VALUE``. A pattern file has a header line with the input node
numbers followed by one comma-separated pattern per line.
"""
import itertools
import os
import random

from pycad import config

MAX_FULL_INPUTS = 12  # exhaustive pattern files grow as 2**inputs


class TPGenerator:
    """Generate test patterns for a circuit.

    Parameters
    ----------
    circuit : Circuit
        The circuit the patterns are for.
    rng : random.Random, optional
        Source of randomness. By default the global ``random`` module is used,
        so ``random.seed`` makes the patterns reproducible. Pass
        ``random.Random(seed)`` for an independent stream.
    """

    def __init__(self, circuit, rng=random):
        self.circuit = circuit
        self.rng = rng

    def _values(self, mode):
        if mode == "b":
            return [0, 1]
        if mode == "x":
            return [0, 1, config.X_VALUE]
        raise ValueError(f"Unknown pattern mode {mode!r}, use 'b' (binary) or 'x' (with X)")

    def gen_single(self, mode="b"):
        """One random pattern.

        ``mode`` is ``"b"`` for values in {0, 1} or ``"x"`` for values in {0, 1, X}.
        """
        values = self._values(mode)
        return [values[self.rng.randint(0, len(values) - 1)]
                for _ in range(len(self.circuit.inputs))]

    def gen_n_random(self, tp_count, mode="b", unique=False):
        """``tp_count`` random patterns (a list; nothing is written to a file).

        With ``unique=True`` no pattern appears twice. If the circuit has too
        few inputs for that many different patterns, repetitions are allowed.
        """
        tp_count = int(tp_count)
        if unique and len(self._values(mode)) ** len(self.circuit.inputs) >= tp_count:
            seen = set()
            tps = []
            while len(tps) < tp_count:
                tp = self.gen_single(mode)
                if tuple(tp) not in seen:
                    seen.add(tuple(tp))
                    tps.append(tp)
            return tps

        return [self.gen_single(mode) for _ in range(tp_count)]

    def _write_file(self, tp_fname, tps):
        os.makedirs(os.path.dirname(os.path.abspath(tp_fname)), exist_ok=True)
        with open(tp_fname, 'w') as outfile:
            outfile.write(",".join(str(node.num) for node in self.circuit.inputs) + "\n")
            for tp in tps:
                outfile.write(",".join(str(val) for val in tp) + "\n")

    def gen_file(self, tp_count, tp_fname=None, mode="b", unique=False):
        """Write ``tp_count`` random patterns to a file.

        If ``tp_fname`` is not given the file goes to ``config.PATTERN_DIR``.

        Returns
        -------
        tuple
            File name and the list of patterns.
        """
        if tp_fname is None:
            tp_fname = os.path.join(
                config.PATTERN_DIR, f"{self.circuit.c_name}_{tp_count}_tp_{mode}.tp")
        tps = self.gen_n_random(tp_count=tp_count, mode=mode, unique=unique)
        self._write_file(tp_fname, tps)
        return tp_fname, tps

    def gen_full(self):
        """All 2**n binary patterns in counting order (the first input is the most significant).

        Every pattern is numbered by reading its values as a binary number.
        """
        return [list(tp) for tp in itertools.product([0, 1], repeat=len(self.circuit.inputs))]

    def gen_full_file(self, tp_fname=None):
        """Write all binary patterns to a file; only for circuits with up to 12 inputs.

        Returns
        -------
        tuple
            File name and the list of patterns.
        """
        if len(self.circuit.inputs) > MAX_FULL_INPUTS:
            raise ValueError(
                f"Cannot write all patterns of a circuit with more than {MAX_FULL_INPUTS} inputs")
        if tp_fname is None:
            tp_fname = os.path.join(config.PATTERN_DIR, f"{self.circuit.c_name}_tp_full.tp")
        tps = self.gen_full()
        self._write_file(tp_fname, tps)
        return tp_fname, tps

    @staticmethod
    def gen_partial(tp, default_value=1):
        """Expand a partially specified pattern into all patterns that match it.

        ``'_'`` and ``None`` entries are replaced by ``default_value``. Each X
        is replaced by both 0 and 1. The patterns come in counting order, and
        ``tp`` itself is not modified.
        """
        tp = [default_value if value == '_' or value is None else value for value in tp]
        unknown = [i for i, value in enumerate(tp) if value == config.X_VALUE]

        tps = []
        for fill in itertools.product([0, 1], repeat=len(unknown)):
            pattern = list(tp)
            for i, bit in zip(unknown, fill, strict=True):
                pattern[i] = bit
            tps.append(pattern)
        return tps

    @staticmethod
    def load_file(fname):
        """Read a pattern file written by ``gen_file`` or ``gen_full_file``.

        The header line is skipped. Values are ``0``, ``1`` or ``X``.
        The order of the inputs is not checked against a circuit.
        """
        if not os.path.exists(fname):
            raise FileNotFoundError(
                f"Test pattern file does not exist: {fname}. "
                "Use gen_file() or gen_full_file() to create it.")

        with open(fname) as infile:
            lines = infile.readlines()

        tps = []
        for line in lines[1:]:
            if not line.strip():
                continue
            tp = []
            for word in line.strip().split(','):
                if word in ('0', '1'):
                    tp.append(int(word))
                elif word.upper() == config.X_VALUE:
                    tp.append(config.X_VALUE)
                else:
                    raise ValueError(f"Invalid value {word!r} in test pattern file {fname}")
            tps.append(tp)
        return tps
