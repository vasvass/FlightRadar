from unittest.mock import Mock, patch

from flight_control.api import Flight, fetch_flight, filter_by_country

SAMPLE_STATE = [
    "a1b2c3",       # icao24
    "UAL123  ",     # callsign
    "United States", # origin_country
    None, None,
    -118.24,        # longitude
    34.05,           # latitude
    10668.0,         # altitude_m
    False,            # on_ground
    230.5,            # velocity_ms
    270.0,            # heading_deg
    -2.5,             # vertical_rate_ms
]


def test_from_state_vector_parses_fields():
    flight = Flight.from_state_vector(SAMPLE_STATE)

    assert flight.icao24 == "a1b2c3"
    assert flight.callsign == "UAL123"
    assert flight.origin_country == "United States"
    assert flight.altitude_m == 10668.0
    assert flight.on_ground is False


def test_filter_by_country_matches_case_insensitively():
    us_flight = Flight.from_state_vector(SAMPLE_STATE)
    uk_state = list(SAMPLE_STATE)
    uk_state[2] = "United Kingdom"
    uk_flight = Flight.from_state_vector(uk_state)

    result = filter_by_country([us_flight, uk_flight], "united states")

    assert result == [us_flight]


@patch("flight_control.api.requests.get")
def test_fetch_flight_returns_none_when_not_found(mock_get):
    mock_get.return_value = Mock(json=lambda: {"states": None})

    assert fetch_flight("ffffff") is None


@patch("flight_control.api.requests.get")
def test_fetch_flight_parses_single_state(mock_get):
    mock_get.return_value = Mock(json=lambda: {"states": [SAMPLE_STATE]})

    flight = fetch_flight("a1b2c3")

    assert flight.icao24 == "a1b2c3"
