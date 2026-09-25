"""Test pattern generation and pattern files."""
import itertools
import os
import random

import pytest

from pycad import config
from pycad.circuit.circuit import Circuit
from pycad.tp_generator import TPGenerator

X = config.X_VALUE


@pytest.fixture(scope="module")
def c17():
    return Circuit(os.path.join(config.CKT_DIR, "c17.ckt"))


def test_random_patterns_have_one_value_per_input(c17):
    tps = TPGenerator(c17).gen_n_random(50)
    assert len(tps) == 50
    assert all(len(tp) == 5 and set(tp) <= {0, 1} for tp in tps)


def test_ternary_mode_produces_x(c17):
    tps = TPGenerator(c17, rng=random.Random(1)).gen_n_random(200, mode="x")
    assert {v for tp in tps for v in tp} == {0, 1, X}


def test_unknown_mode_is_rejected(c17):
    with pytest.raises(ValueError, match="mode"):
        TPGenerator(c17).gen_single("z")


def test_global_seed_and_private_rng_are_reproducible(c17):
    random.seed(5)
    first = TPGenerator(c17).gen_n_random(10)
    random.seed(5)
    assert TPGenerator(c17).gen_n_random(10) == first
    assert (TPGenerator(c17, rng=random.Random(5)).gen_n_random(10)
            == TPGenerator(c17, rng=random.Random(5)).gen_n_random(10))


def test_private_rng_leaves_the_global_stream_alone(c17):
    random.seed(9)
    expected = random.random()
    random.seed(9)
    TPGenerator(c17, rng=random.Random(1)).gen_n_random(10)
    assert random.random() == expected


@pytest.mark.parametrize("mode, count", [("b", 32), ("x", 100)])
def test_unique_patterns_are_all_different(c17, mode, count):
    tps = TPGenerator(c17).gen_n_random(count, mode=mode, unique=True)
    assert len(tps) == count
    assert len({tuple(tp) for tp in tps}) == count


def test_unique_falls_back_to_repetition_when_too_few_patterns_exist(c17):
    tps = TPGenerator(c17).gen_n_random(40, unique=True)  # only 32 binary patterns exist
    assert len(tps) == 40


def test_full_set_is_every_pattern_in_counting_order(c17):
    tps = TPGenerator(c17).gen_full()
    assert tps == [list(t) for t in itertools.product([0, 1], repeat=5)]
    assert [int("".join(map(str, tp)), 2) for tp in tps] == list(range(32))


def test_partial_pattern_expansion(c17):
    tp = [1, X, "_", X, None]
    assert TPGenerator(c17).gen_partial(tp) == [
        [1, 0, 1, 0, 1], [1, 0, 1, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 1]]
    assert tp == [1, X, "_", X, None]  # not modified
    assert TPGenerator.gen_partial([0, "_"], default_value=0) == [[0, 0]]
    assert TPGenerator.gen_partial([0, 1]) == [[0, 1]]


def test_file_round_trip(c17, tmp_path):
    fname = tmp_path / "sub" / "tps.tp"
    tp_fname, tps = TPGenerator(c17, rng=random.Random(3)).gen_file(15, str(fname), mode="x")
    assert tp_fname == str(fname)
    assert fname.read_text().splitlines()[0] == "1,2,3,6,7"
    assert TPGenerator.load_file(str(fname)) == tps


def test_default_file_goes_to_the_pattern_directory(c17, tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PATTERN_DIR", str(tmp_path / "patterns"))
    tp_fname, _ = TPGenerator(c17).gen_file(4)
    assert tp_fname == str(tmp_path / "patterns" / "c17_4_tp_b.tp")
    assert os.path.exists(tp_fname)


def test_full_file_holds_every_pattern(c17, tmp_path):
    tp_fname, tps = TPGenerator(c17).gen_full_file(str(tmp_path / "full.tp"))
    assert TPGenerator.load_file(tp_fname) == tps
    assert len(tps) == 32


def test_full_file_refuses_large_circuits(tmp_path):
    big = Circuit(os.path.join(config.CKT_DIR, "c432.ckt"))
    with pytest.raises(ValueError, match="12"):
        TPGenerator(big).gen_full_file(str(tmp_path / "full.tp"))
    assert not (tmp_path / "full.tp").exists()


def test_load_file_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        TPGenerator.load_file(str(tmp_path / "missing.tp"))
    bad = tmp_path / "bad.tp"
    bad.write_text("1,2\n0,2\n")
    with pytest.raises(ValueError, match="'2'"):
        TPGenerator.load_file(str(bad))


def test_load_file_accepts_x_and_blank_lines(tmp_path):
    f = tmp_path / "x.tp"
    f.write_text("1,2,3\n0,X,1\n1,x,0\n\n")
    assert TPGenerator.load_file(str(f)) == [[0, X, 1], [1, X, 0]]
