from unittest.mock import patch

from app import app
from flight_control.api import Flight

SAMPLE_FLIGHT = Flight(
    icao24="a1b2c3",
    callsign="UAL123",
    origin_country="United States",
    longitude=-118.24,
    latitude=34.05,
    altitude_m=10668.0,
    velocity_ms=230.5,
    heading_deg=270.0,
    vertical_rate_ms=-2.5,
    on_ground=False,
)


def test_index_returns_html():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Flight Control Center" in response.data


@patch("app.fetch_flights", return_value=[SAMPLE_FLIGHT])
def test_api_flights_returns_json(mock_fetch):
    client = app.test_client()
    response = client.get("/api/flights")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["callsign"] == "UAL123"


@patch("app.fetch_flights", return_value=[SAMPLE_FLIGHT])
def test_api_flights_filters_by_country(mock_fetch):
    client = app.test_client()
    response = client.get("/api/flights?country=france")

    assert response.status_code == 200
    assert response.get_json() == []


def test_aircraft_detail_returns_html():
    client = app.test_client()
    response = client.get("/aircraft/a1b2c3")

    assert response.status_code == 200
    assert b"a1b2c3" in response.data


@patch("app.fetch_flight", return_value=SAMPLE_FLIGHT)
def test_api_aircraft_returns_flight_and_profile(mock_fetch):
    client = app.test_client()
    response = client.get("/api/aircraft/a1b2c3")

    assert response.status_code == 200
    data = response.get_json()
    assert data["flight"]["icao24"] == "a1b2c3"
    assert "manufacturer" in data["profile"]


@patch("app.fetch_flight", return_value=None)
def test_api_aircraft_404s_when_not_tracked(mock_fetch):
    client = app.test_client()
    response = client.get("/api/aircraft/ffffff")

    assert response.status_code == 404


# --- root route ---

def test_index_content_type_is_html():
    client = app.test_client()
    response = client.get("/")

    assert "text/html" in response.content_type


# --- /api/flights edge cases ---

def test_api_flights_rejects_invalid_bbox():
    client = app.test_client()
    response = client.get("/api/flights?bbox=not,valid")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_api_flights_rejects_non_numeric_bbox():
    client = app.test_client()
    response = client.get("/api/flights?bbox=a,b,c,d")

    assert response.status_code == 400


@patch("app.fetch_flights")
def test_api_flights_excludes_on_ground(mock_fetch):
    grounded = Flight(
        icao24="dead01",
        callsign="GND001",
        origin_country="Germany",
        longitude=13.4,
        latitude=52.5,
        altitude_m=0.0,
        velocity_ms=0.0,
        heading_deg=0.0,
        vertical_rate_ms=0.0,
        on_ground=True,
    )
    mock_fetch.return_value = [grounded, SAMPLE_FLIGHT]
    client = app.test_client()
    response = client.get("/api/flights")

    data = response.get_json()
    assert all(not f["on_ground"] for f in data)
    assert len(data) == 1


@patch("app.fetch_flights")
def test_api_flights_caps_results_at_25(mock_fetch):
    flights = [
        Flight(
            icao24=f"{i:06x}",
            callsign=f"FLT{i:03}",
            origin_country="United States",
            longitude=-118.0,
            latitude=34.0,
            altitude_m=10000.0 + i,
            velocity_ms=200.0,
            heading_deg=90.0,
            vertical_rate_ms=0.0,
            on_ground=False,
        )
        for i in range(30)
    ]
    mock_fetch.return_value = flights
    client = app.test_client()
    response = client.get("/api/flights")

    assert response.status_code == 200
    assert len(response.get_json()) == 25


@patch("app.fetch_flights")
def test_api_flights_sorted_by_altitude_descending(mock_fetch):
    low = Flight(
        icao24="aaa000", callsign="LOW", origin_country="France",
        longitude=2.3, latitude=48.9, altitude_m=5000.0,
        velocity_ms=200.0, heading_deg=0.0, vertical_rate_ms=0.0, on_ground=False,
    )
    high = Flight(
        icao24="bbb000", callsign="HIGH", origin_country="France",
        longitude=2.3, latitude=48.9, altitude_m=35000.0,
        velocity_ms=250.0, heading_deg=0.0, vertical_rate_ms=0.0, on_ground=False,
    )
    mock_fetch.return_value = [low, high]
    client = app.test_client()
    response = client.get("/api/flights")

    data = response.get_json()
    assert data[0]["callsign"] == "HIGH"
    assert data[1]["callsign"] == "LOW"


@patch("app.fetch_flights")
def test_api_flights_accepts_custom_bbox(mock_fetch):
    mock_fetch.return_value = [SAMPLE_FLIGHT]
    client = app.test_client()
    response = client.get("/api/flights?bbox=40.4,-74.3,41.0,-73.6")

    assert response.status_code == 200
    _, kwargs = mock_fetch.call_args
    assert kwargs["bbox"] == (40.4, -74.3, 41.0, -73.6)


# --- /api/aircraft/<icao24> ---

@patch("app.fetch_flight", return_value=SAMPLE_FLIGHT)
def test_api_aircraft_profile_has_expected_fields(mock_fetch):
    client = app.test_client()
    data = client.get("/api/aircraft/a1b2c3").get_json()

    profile = data["profile"]
    for field in ("manufacturer", "model", "engines", "engine_type", "wingspan_m", "length_m"):
        assert field in profile


@patch("app.fetch_flight", return_value=SAMPLE_FLIGHT)
def test_api_aircraft_flight_fields_match_sample(mock_fetch):
    client = app.test_client()
    data = client.get("/api/aircraft/a1b2c3").get_json()

    flight = data["flight"]
    assert flight["icao24"] == SAMPLE_FLIGHT.icao24
    assert flight["callsign"] == SAMPLE_FLIGHT.callsign
    assert flight["altitude_m"] == SAMPLE_FLIGHT.altitude_m
