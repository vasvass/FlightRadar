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
