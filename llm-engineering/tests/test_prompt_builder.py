import importlib.util


def load_module():
    spec = importlib.util.spec_from_file_location(
        "prompt_engineering", "01-prompt-engineering.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_prompt_raises_on_unknown_pattern():
    module = load_module()
    builder = module.PromptBuilder()

    try:
        builder.build_prompt("nonexistent_pattern", {})
    except ValueError as e:
        assert "Unknown pattern" in str(e)
        assert "nonexistent_pattern" in str(e)
    else:
        raise AssertionError("Expected ValueError for unknown pattern")