"""Client for the OpenSky Network REST API.

Docs: https://openskynetwork.github.io/opensky-api/rest.html
Anonymous requests are free but rate-limited (~400/day, 10s resolution).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests

STATES_URL = "https://opensky-network.org/api/states/all"


@dataclass
class Flight:
    icao24: str
    callsign: str
    origin_country: str
    longitude: Optional[float]
    latitude: Optional[float]
    altitude_m: Optional[float]
    velocity_ms: Optional[float]
    heading_deg: Optional[float]
    vertical_rate_ms: Optional[float]
    on_ground: bool

    @classmethod
    def from_state_vector(cls, state: list) -> "Flight":
        return cls(
            icao24=state[0],
            callsign=(state[1] or "").strip(),
            origin_country=state[2],
            longitude=state[5],
            latitude=state[6],
            altitude_m=state[7],
            on_ground=state[8],
            velocity_ms=state[9],
            heading_deg=state[10],
            vertical_rate_ms=state[11],
        )


def fetch_flights(bbox: Optional[tuple] = None) -> list:
    """Fetch current flight state vectors.

    bbox is (lamin, lomin, lamax, lomax) to restrict the query area;
    omit it to fetch every aircraft OpenSky is currently tracking worldwide.
    """
    params = {}
    if bbox:
        lamin, lomin, lamax, lomax = bbox
        params.update(lamin=lamin, lomin=lomin, lamax=lamax, lomax=lomax)

    response = requests.get(STATES_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    states = data.get("states") or []
    return [Flight.from_state_vector(s) for s in states]


def filter_by_country(flights: list, country: str) -> list:
    """Keep only flights whose origin country contains `country` (case-insensitive)."""
    needle = country.lower()
    return [f for f in flights if needle in f.origin_country.lower()]


def fetch_flight(icao24: str) -> Optional[Flight]:
    """Fetch the current state of a single aircraft by its icao24 address."""
    response = requests.get(STATES_URL, params={"icao24": icao24}, timeout=10)
    response.raise_for_status()
    states = response.json().get("states") or []
    return Flight.from_state_vector(states[0]) if states else None
