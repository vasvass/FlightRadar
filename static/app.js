const M_TO_FT = 3.28084;
const MS_TO_KTS = 1.94384;
const REFRESH_MS = 15000;

const tbody = document.getElementById("flights-body");
const countryInput = document.getElementById("country");
const statusEl = document.getElementById("status");

async function loadFlights() {
  const params = new URLSearchParams();

  const pageParams = new URLSearchParams(window.location.search);
  const bbox = pageParams.get("bbox");
  if (bbox) {
    params.set("bbox", bbox);
  }

  if (countryInput.value.trim()) {
    params.set("country", countryInput.value.trim());
  }

  try {
    const response = await fetch(`/api/flights?${params}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const flights = await response.json();
    renderFlights(flights);
    statusEl.textContent = `${flights.length} flights · updated ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  }
}

function renderFlights(flights) {
  tbody.innerHTML = "";
  for (const f of flights) {
    const row = document.createElement("tr");
    row.classList.add("flight-row");
    row.addEventListener("click", () => {
      window.location.href = `/aircraft/${f.icao24}`;
    });

    const altitude = f.altitude_m != null ? Math.round(f.altitude_m * M_TO_FT).toLocaleString() : "-";
    const speed = f.velocity_ms != null ? Math.round(f.velocity_ms * MS_TO_KTS) : "-";
    const heading = f.heading_deg != null ? `${Math.round(f.heading_deg)}°` : "-";

    const cells = [
      f.callsign || f.icao24,
      f.origin_country,
      altitude,
      speed,
      heading,
    ];

    for (const value of cells) {
      const td = document.createElement("td");
      td.textContent = String(value);
      row.appendChild(td);
    }
    tbody.appendChild(row);
}

countryInput.addEventListener("change", loadFlights);
loadFlights();
setInterval(loadFlights, REFRESH_MS);
