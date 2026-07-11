from flight_control.aircraft_catalog import CATALOG, profile_for


def test_profile_for_is_deterministic():
    assert profile_for("a1b2c3") == profile_for("a1b2c3")


def test_profile_for_returns_a_catalog_entry():
    assert profile_for("abcdef") in CATALOG
