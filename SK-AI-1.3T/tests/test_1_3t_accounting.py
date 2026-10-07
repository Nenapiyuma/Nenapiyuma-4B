import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.config import PRESET_CONFIGS
from model.llm import SKLLMForCausalLM

def test_current_parameter_counts_are_exact():
    expected = {
        "sk-llm-mini": 1_311_872,
        "sk-llm-small": 1_213_302_784,
        "sk-llm-medium": 6_195_253_248,
        "sk-llm-large": 56_863_236_096,
    }
    for name, value in expected.items():
        assert PRESET_CONFIGS[name].estimate_parameter_count() == value
        if name == "sk-llm-mini":
            assert SKLLMForCausalLM(PRESET_CONFIGS[name]).num_parameters() == value

def test_1_3t_is_not_claimed_by_existing_presets():
    assert all(c.estimate_parameter_count() != 1_300_000_000_000 for c in PRESET_CONFIGS.values())

def test_1_3t_weight_math():
    n = 1_300_000_000_000
    assert n * 4 == 5_200_000_000_000
    assert n * 2 == 2_600_000_000_000
    assert n == 1_300_000_000_000
    assert n // 2 == 650_000_000_000
