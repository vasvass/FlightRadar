"""Flight Control Center: a live terminal dashboard of real aircraft.

Fetches live aircraft state vectors from the OpenSky Network public API
and renders them as a refreshing table.
"""

import argparse
import time

from rich.console import Console
from rich.live import Live

from flight_control.api import fetch_flights, filter_by_country
from flight_control.dashboard import build_table

# Los Angeles basin: (lamin, lomin, lamax, lomax)
DEFAULT_BBOX = (33.5, -118.9, 34.5, -117.5)
REFRESH_SECONDS = 15


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live flight control dashboard")
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("LAMIN", "LOMIN", "LAMAX", "LOMAX"),
        default=DEFAULT_BBOX,
        help="Bounding box to track (default: Los Angeles basin)",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=REFRESH_SECONDS,
        help="Seconds between refreshes (default: 15)",
    )
    parser.add_argument(
        "--country",
        type=str,
        default=None,
        help="Only show flights whose origin country contains this text",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    console = Console()

    with Live(console=console, refresh_per_second=1) as live:
        while True:
            try:
                flights = fetch_flights(bbox=tuple(args.bbox))
                if args.country:
                    flights = filter_by_country(flights, args.country)
                live.update(build_table(flights))
            except Exception as exc:  # keep the dashboard running past transient API hiccups
                console.print(f"[red]Error fetching flights: {exc}[/red]")
            time.sleep(args.refresh)


if __name__ == "__main__":
    main()
