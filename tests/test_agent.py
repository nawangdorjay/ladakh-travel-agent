"""Basic tests for the Ladakh Travel Agent."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def test_permits_data_loads():
    """Test that permits.json loads and has expected structure."""
    with open(DATA_DIR / "permits.json") as f:
        data = json.load(f)
    
    assert "areas" in data
    assert len(data["areas"]) > 0
    
    for area, info in data["areas"].items():
        assert "permit_required" in info, f"{area} missing permit_required"
        assert "how_to_apply" in info, f"{area} missing how_to_apply"
        assert "cost" in info, f"{area} missing cost"


def test_routes_data_loads():
    """Test that routes.json loads and has expected structure."""
    with open(DATA_DIR / "routes.json") as f:
        data = json.load(f)
    
    assert "routes" in data
    assert len(data["routes"]) > 0
    
    for route, info in data["routes"].items():
        assert "elevation" in info, f"{route} missing elevation"
        assert "open_season" in info, f"{route} missing open_season"
        assert "tips" in info, f"{route} missing tips"


def test_homestays_data_loads():
    """Test that homestays.json loads and has expected structure."""
    with open(DATA_DIR / "homestays.json") as f:
        data = json.load(f)
    
    assert "homestays" in data
    assert len(data["homestays"]) > 0


def test_cultural_guide_loads():
    """Test that cultural_guide.json loads and has expected structure."""
    with open(DATA_DIR / "cultural_guide.json") as f:
        data = json.load(f)
    
    assert "guidelines" in data
    assert len(data["guidelines"]) > 0
    
    for category, info in data["guidelines"].items():
        assert "tips" in info, f"{category} missing tips"
        assert len(info["tips"]) > 0, f"{category} has no tips"


def test_weather_module_imports():
    """Test that weather module can be imported."""
    from utils.weather import get_weather_for_location, LADAKH_LOCATIONS
    
    assert "leh" in LADAKH_LOCATIONS
    assert "pangong" in LADAKH_LOCATIONS
    assert "nubra" in LADAKH_LOCATIONS


def test_tool_functions_exist():
    """Test that all tool functions are defined."""
    from agent.tools import get_tools
    
    tools = get_tools()
    assert len(tools) == 6
    
    tool_names = [t.name for t in tools]
    expected = [
        "check_permit_requirements",
        "get_weather_info",
        "get_road_status",
        "get_altitude_advice",
        "find_homestays",
        "get_cultural_etiquette",
    ]
    for name in expected:
        assert name in tool_names, f"Missing tool: {name}"
