const M_TO_FT = 3.28084;
const MS_TO_KTS = 1.94384;
const REFRESH_MS = 15000;

const tbody = document.getElementById("flights-body");
const countryInput = document.getElementById("country");
const statusEl = document.getElementById("status");

async function loadFlights() {
  const params = new URLSearchParams();
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
    const altitude = f.altitude_m ? Math.round(f.altitude_m * M_TO_FT).toLocaleString() : "-";
    const speed = f.velocity_ms ? Math.round(f.velocity_ms * MS_TO_KTS) : "-";
    const heading = f.heading_deg != null ? `${Math.round(f.heading_deg)}°` : "-";

    row.innerHTML = `
      <td>${f.callsign || f.icao24}</td>
      <td>${f.origin_country}</td>
      <td>${altitude}</td>
      <td>${speed}</td>
      <td>${heading}</td>
    `;
    tbody.appendChild(row);
  }
}

countryInput.addEventListener("change", loadFlights);
loadFlights();
setInterval(loadFlights, REFRESH_MS);
