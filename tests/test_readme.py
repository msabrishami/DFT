"""The quick start of the README must run as written."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_readme_quick_start_runs(capsys):
    with open(os.path.join(ROOT, "README.md")) as infile:
        blocks = re.findall(r"```python\n(.*?)```", infile.read(), flags=re.S)
    assert blocks
    exec(compile(blocks[0], "README.md", "exec"), {})
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "[1, 0]"
    assert any(line.startswith("detected") for line in lines)
