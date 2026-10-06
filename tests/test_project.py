from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_compile():
    sources = sorted((ROOT / "scripts").glob("*.py"))
    assert sources, "No Python scripts found"
    for path in sources:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_size_limit_is_strict():
    source = (ROOT / "scripts" / "check_size.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    values = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "MAX_BYTES" for t in node.targets)
    ]
    assert values == [1_500_000_000]


def test_example_dataset_is_valid_jsonl():
    dataset = ROOT / "data" / "train.example.jsonl"
    assert dataset.is_file()
    rows = [
        json.loads(line)
        for line in dataset.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows
    for row in rows:
        assert isinstance(row, dict)
        assert "instruction" in row
        assert "output" in row
        assert isinstance(row["instruction"], str)
        assert isinstance(row["output"], str)


def test_qlora_config_exists():
    config = ROOT / "configs" / "qlora.yaml"
    assert config.is_file()
    text = config.read_text(encoding="utf-8")
    assert "base_model:" in text
    assert "output_dir:" in text
