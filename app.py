"""Flask web UI for the flight dashboard.

Serves a page that polls /api/flights for live aircraft data and renders
it as an auto-refreshing table in the browser.
"""

from dataclasses import asdict

from flask import Flask, jsonify, render_template, request

from flight_control.aircraft_catalog import profile_for
from flight_control.api import fetch_flight, fetch_flights, filter_by_country

app = Flask(__name__)

# Los Angeles basin: (lamin, lomin, lamax, lomax)
DEFAULT_BBOX = (33.5, -118.9, 34.5, -117.5)


def _bbox_from_request() -> tuple:
    raw = request.args.get("bbox")
    if not raw:
        return DEFAULT_BBOX
    lamin, lomin, lamax, lomax = (float(v) for v in raw.split(","))
    return (lamin, lomin, lamax, lomax)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/flights")
def api_flights():
    bbox = _bbox_from_request()
    country = request.args.get("country")

    flights = fetch_flights(bbox=bbox)
    if country:
        flights = filter_by_country(flights, country)

    airborne = [f for f in flights if not f.on_ground]
    airborne.sort(key=lambda f: f.altitude_m or 0, reverse=True)

    return jsonify([asdict(f) for f in airborne[:25]])


@app.route("/aircraft/<icao24>")
def aircraft_detail(icao24):
    return render_template("aircraft.html", icao24=icao24)


@app.route("/api/aircraft/<icao24>")
def api_aircraft(icao24):
    flight = fetch_flight(icao24)
    if flight is None:
        return jsonify({"error": "aircraft not currently tracked"}), 404

    return jsonify({
        "flight": asdict(flight),
        "profile": asdict(profile_for(icao24)),
    })


if __name__ == "__main__":
    app.run()
