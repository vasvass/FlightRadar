# Flight Control Center

A terminal dashboard that tracks live aircraft using the free
[OpenSky Network](https://opensky-network.org/) API — built as a Python
learning project.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (CLI dashboard)

```bash
python main.py
```

By default it tracks the Los Angeles basin. Pass your own bounding box:

```bash
python main.py --bbox 40.4 -74.3 41.0 -73.6   # New York area
```

Filter by origin country:

```bash
python main.py --country "United States"
```

## Run (web UI)

```bash
python app.py
```

Then open http://127.0.0.1:5000. The page polls `/api/flights` every 15s and
supports the same country filter as the CLI, typed into the box in the
header. Bounding box can be overridden via a `?bbox=lamin,lomin,lamax,lomax`
query parameter.

Click any flight row to open its aircraft detail page: a blueprint diagram
and a cockpit instrument panel (airspeed, altimeter, heading, vertical
speed, and an approximated attitude indicator) driven by that aircraft's
live telemetry. OpenSky's free feed has no aircraft-model field (its old
metadata lookup API is discontinued), so the model/blueprint shown is
assigned deterministically from a small bundled catalog — illustrative,
not the real airframe. The gauge values themselves (speed, altitude,
heading, vertical rate) are genuine live data.

## Test

```bash
pip install pytest
python -m pytest
```

## Project layout

- `flight_control/api.py` — talks to the OpenSky REST API, parses raw state
  vectors into `Flight` objects; `fetch_flight()` looks up a single aircraft
- `flight_control/aircraft_catalog.py` — bundled catalog of illustrative
  aircraft profiles, deterministically assigned per `icao24`
- `flight_control/dashboard.py` — turns a list of `Flight`s into a `rich`
  table (used by the CLI)
- `main.py` — CLI entry point, polling loop
- `app.py` — Flask web UI; serves pages plus `/api/flights` and
  `/api/aircraft/<icao24>` JSON endpoints
- `templates/`, `static/` — the web UI's HTML/CSS/JS, including the SVG
  aircraft blueprints (`static/blueprints/`) and cockpit gauge logic
  (`static/cockpit.js`)
- `tests/` — unit tests

## Roadmap

- Persist snapshots to SQLite and chart altitude/speed history for one flight
- Add alerting (e.g. flash a row when a plane descends below a threshold)
- Live map view (Leaflet.js) plotting aircraft by lat/lon
- Turn-rate estimation (derived from heading deltas between polls) for a
  turn coordinator gauge
