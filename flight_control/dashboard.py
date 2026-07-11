"""Terminal dashboard rendering for tracked flights."""

from rich.table import Table

M_TO_FT = 3.28084
MS_TO_KTS = 1.94384


def build_table(flights: list) -> Table:
    table = Table(title="Flight Control Center", expand=True)
    table.add_column("Callsign", style="cyan", no_wrap=True)
    table.add_column("Country", style="magenta")
    table.add_column("Altitude (ft)", justify="right")
    table.add_column("Speed (kts)", justify="right")
    table.add_column("Heading", justify="right")
    table.add_column("Status", justify="center")

    airborne = [f for f in flights if not f.on_ground]
    airborne.sort(key=lambda f: f.altitude_m or 0, reverse=True)

    for f in airborne[:25]:
        altitude_ft = f"{f.altitude_m * M_TO_FT:,.0f}" if f.altitude_m else "-"
        speed_kts = f"{f.velocity_ms * MS_TO_KTS:,.0f}" if f.velocity_ms else "-"
        heading = f"{f.heading_deg:.0f}°" if f.heading_deg is not None else "-"

        table.add_row(
            f.callsign or f.icao24,
            f.origin_country,
            altitude_ft,
            speed_kts,
            heading,
            "[green]AIRBORNE[/green]",
        )

    table.caption = f"{len(airborne)} airborne / {len(flights)} tracked"
    return table
