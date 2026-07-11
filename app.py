"""Flask web UI for the flight dashboard.

Serves a page that polls /api/flights for live aircraft data and renders
it as an auto-refreshing table in the browser.
"""

from dataclasses import asdict

from flask import Flask, jsonify, render_template, request

from flight_control.api import fetch_flights, filter_by_country

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


if __name__ == "__main__":
    app.run(debug=True)
