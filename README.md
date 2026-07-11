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

## Test

```bash
pip install pytest
python -m pytest
```

## Project layout

- `flight_control/api.py` — talks to the OpenSky REST API, parses raw state
  vectors into `Flight` objects
- `flight_control/dashboard.py` — turns a list of `Flight`s into a `rich`
  table (used by the CLI)
- `main.py` — CLI entry point, polling loop
- `app.py` — Flask web UI; serves the page and a `/api/flights` JSON endpoint
- `templates/`, `static/` — the web UI's HTML/CSS/JS
- `tests/` — unit tests

## Roadmap

- Aircraft info per flight: model, engines, a labeled blueprint diagram
  (looked up from `icao24`/aircraft type — likely a small bundled reference
  dataset rather than a live paid API)
- A cockpit-style instrument panel (attitude indicator, altimeter, airspeed,
  heading) driven by a selected flight's live telemetry
- Persist snapshots to SQLite and chart altitude/speed history for one flight
- Add alerting (e.g. flash a row when a plane descends below a threshold)
- Live map view (Leaflet.js) plotting aircraft by lat/lon
