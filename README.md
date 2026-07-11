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

## Run

```bash
python main.py
```

By default it tracks the Los Angeles basin. Pass your own bounding box:

```bash
python main.py --bbox 40.4 -74.3 41.0 -73.6   # New York area
```

## Test

```bash
pip install pytest
python -m pytest
```

## Project layout

- `flight_control/api.py` — talks to the OpenSky REST API, parses raw state
  vectors into `Flight` objects
- `flight_control/dashboard.py` — turns a list of `Flight`s into a `rich`
  table
- `main.py` — CLI entry point, polling loop
- `tests/` — unit tests

## Ideas for extending this as you learn

- Add a `--country` filter to only show flights from a given origin country
- Persist snapshots to SQLite and chart altitude/speed history for one flight
- Add alerting (e.g. flash a row when a plane descends below a threshold)
- Swap the polling loop for `asyncio` + `aiohttp`
- Add a simple Flask/FastAPI endpoint that serves the same data as JSON
