"""A small bundled catalog of real aircraft profiles.

OpenSky's free live-state feed has no aircraft type/model field, and its
old per-aircraft metadata endpoint is discontinued (HTTP 410 Gone). So we
can't know which real airframe a given icao24 actually is. Instead, each
flight is assigned a profile from this catalog deterministically by its
icao24 (same tail always gets the same profile), purely to drive the
blueprint and cockpit visualizations. It is illustrative, not a claim
about the real aircraft.

The `blueprint` field names an SVG in static/blueprints/, derived from
tar1090 (GPLv2+) — see static/blueprints/NOTICE.md for attribution and
license details.
"""

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class AircraftProfile:
    manufacturer: str
    model: str
    blueprint: str  # matches an SVG file in static/blueprints/ (no extension)
    engines: int
    engine_type: str
    wingspan_m: float
    length_m: float
    typical_cruise_alt_ft: int


CATALOG = [
    AircraftProfile("Boeing", "737-800", "b738", 2, "turbofan", 35.8, 39.5, 35000),
    AircraftProfile("Airbus", "A320neo", "a320", 2, "turbofan", 35.8, 37.6, 37000),
    AircraftProfile("Boeing", "777-300ER", "heavy_2e", 2, "turbofan", 64.8, 73.9, 40000),
    AircraftProfile("Airbus", "A350-900", "a359", 2, "turbofan", 64.8, 66.8, 41000),
    AircraftProfile("Embraer", "E175", "airliner", 2, "turbofan", 26.0, 31.9, 32000),
    AircraftProfile("Bombardier", "CRJ900", "jet_swept", 2, "turbofan", 24.9, 36.4, 33000),
    AircraftProfile("ATR", "72-600", "twin_small", 2, "turboprop", 27.0, 27.2, 24000),
]


def profile_for(icao24: str) -> AircraftProfile:
    digest = hashlib.sha1(icao24.encode()).digest()
    return CATALOG[digest[0] % len(CATALOG)]
