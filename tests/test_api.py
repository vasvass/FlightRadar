from flight_control.api import Flight

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
]


def test_from_state_vector_parses_fields():
    flight = Flight.from_state_vector(SAMPLE_STATE)

    assert flight.icao24 == "a1b2c3"
    assert flight.callsign == "UAL123"
    assert flight.origin_country == "United States"
    assert flight.altitude_m == 10668.0
    assert flight.on_ground is False
