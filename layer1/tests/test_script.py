import pytest

from hb_layer1.script import ScriptError, choose_tool, fill_arguments, normalise_tool

NESTED = {"type": "function", "function": {"name": "read", "parameters": {"required": ["path"]}}}
FLAT = {"name": "bash", "parameters": {"required": ["command"]}}


def test_both_tool_schema_shapes_are_understood():
    assert normalise_tool(NESTED)[0] == "read"
    assert normalise_tool(FLAT)[0] == "bash"


def test_preference_order_decides_which_offered_tool_is_called():
    name, _ = choose_tool([FLAT, NESTED], ("read", "bash"))
    assert name == "read"


def test_an_arm_without_the_preferred_tool_is_an_error_not_a_guess():
    with pytest.raises(ScriptError, match="none of"):
        choose_tool([FLAT], ("read",))


def test_no_tools_at_all_is_an_error():
    with pytest.raises(ScriptError, match="no tool schemas"):
        choose_tool([], ("read",))


def test_arguments_come_from_the_arms_own_schema():
    _, parameters = normalise_tool(NESTED)
    assert fill_arguments(parameters, "/w/PROBE.md") == {"path": "/w/PROBE.md"}


def test_an_unknown_required_argument_raises_rather_than_being_invented():
    parameters = {"required": ["quantum_flux"], "properties": {"quantum_flux": {}}}
    with pytest.raises(ScriptError, match="quantum_flux"):
        fill_arguments(parameters, "/w/PROBE.md")


def test_optional_properties_are_left_out():
    parameters = {"required": ["path"], "properties": {"path": {}, "offset": {}}}
    assert "offset" not in fill_arguments(parameters, "/w/PROBE.md")
