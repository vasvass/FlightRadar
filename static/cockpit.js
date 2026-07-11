const ICAO24 = document.currentScript.dataset.icao24;
const REFRESH_MS = 8000;

const statusEl = document.getElementById("status");
const errorEl = document.getElementById("error");
const blueprintEl = document.getElementById("blueprint");
const profileEl = document.getElementById("profile-info");
const gaugesEl = document.getElementById("gauges");

const M_TO_FT = 3.28084;
const MS_TO_KTS = 1.94384;
const MS_TO_FPM = 196.85;

// Round dial gauges: a value is linearly mapped onto a 260° sweep, leaving
// a 100° gap at the bottom of the dial (the classic analog-gauge look).
const SWEEP_DEG = 260;

const GAUGE_CONFIGS = {
  airspeed: { label: "AIRSPEED (KTS)", min: 0, max: 500 },
  altitude: { label: "ALTITUDE (FT)", min: 0, max: 45000 },
  vsi: { label: "VERTICAL SPEED (FPM)", min: -4000, max: 4000 },
};

function buildGauge(key, config) {
  const wrapper = document.createElement("div");
  wrapper.className = "gauge";
  wrapper.innerHTML = `
    <svg viewBox="0 0 200 200">
      <circle class="dial-face" cx="100" cy="100" r="92" />
      <line class="needle" id="needle-${key}" x1="100" y1="100" x2="100" y2="25" />
      <circle class="hub" cx="100" cy="100" r="6" />
    </svg>
    <div class="gauge-label">${config.label}</div>
    <div class="gauge-value" id="value-${key}">--</div>
  `;
  return wrapper;
}

function buildCompass() {
  const wrapper = document.createElement("div");
  wrapper.className = "gauge";
  wrapper.innerHTML = `
    <svg viewBox="0 0 200 200">
      <circle class="dial-face" cx="100" cy="100" r="92" />
      <text x="100" y="20" class="compass-label" text-anchor="middle">N</text>
      <text x="180" y="105" class="compass-label" text-anchor="middle">E</text>
      <text x="100" y="188" class="compass-label" text-anchor="middle">S</text>
      <text x="20" y="105" class="compass-label" text-anchor="middle">W</text>
      <line class="needle" id="needle-heading" x1="100" y1="100" x2="100" y2="25" />
      <circle class="hub" cx="100" cy="100" r="6" />
    </svg>
    <div class="gauge-label">HEADING</div>
    <div class="gauge-value" id="value-heading">--</div>
  `;
  return wrapper;
}

function buildAttitude() {
  const wrapper = document.createElement("div");
  wrapper.className = "gauge";
  wrapper.innerHTML = `
    <svg viewBox="0 0 200 200">
      <clipPath id="horizon-clip">
        <circle cx="100" cy="100" r="92" />
      </clipPath>
      <g clip-path="url(#horizon-clip)">
        <rect id="sky" x="-50" y="-200" width="300" height="300" fill="#2e7cc7" />
        <rect id="ground" x="-50" y="100" width="300" height="300" fill="#8a5a2b" />
        <line id="horizon-line" x1="-50" y1="100" x2="250" y2="100" stroke="#d7e3ea" stroke-width="2" />
      </g>
      <circle class="dial-outline" cx="100" cy="100" r="92" />
      <line x1="70" y1="100" x2="130" y2="100" class="attitude-marker" />
    </svg>
    <div class="gauge-label">ATTITUDE (approx.)</div>
    <div class="gauge-value" id="value-attitude">--</div>
  `;
  return wrapper;
}

function initGauges() {
  gaugesEl.appendChild(buildGauge("airspeed", GAUGE_CONFIGS.airspeed));
  gaugesEl.appendChild(buildCompass());
  gaugesEl.appendChild(buildGauge("altitude", GAUGE_CONFIGS.altitude));
  gaugesEl.appendChild(buildGauge("vsi", GAUGE_CONFIGS.vsi));
  gaugesEl.appendChild(buildAttitude());
}

function setNeedle(key, angleDeg) {
  const needle = document.getElementById(`needle-${key}`);
  if (needle) needle.setAttribute("transform", `rotate(${angleDeg} 100 100)`);
}

function angleForLinearGauge(value, config) {
  const clamped = Math.max(config.min, Math.min(config.max, value));
  const ratio = (clamped - config.min) / (config.max - config.min);
  return -SWEEP_DEG / 2 + ratio * SWEEP_DEG;
}

function updateGauges(flight) {
  const speedKts = flight.velocity_ms != null ? flight.velocity_ms * MS_TO_KTS : 0;
  setNeedle("airspeed", angleForLinearGauge(speedKts, GAUGE_CONFIGS.airspeed));
  document.getElementById("value-airspeed").textContent = Math.round(speedKts);

  const altFt = flight.altitude_m != null ? flight.altitude_m * M_TO_FT : 0;
  setNeedle("altitude", angleForLinearGauge(altFt, GAUGE_CONFIGS.altitude));
  document.getElementById("value-altitude").textContent = Math.round(altFt).toLocaleString();

  const vsiFpm = flight.vertical_rate_ms != null ? flight.vertical_rate_ms * MS_TO_FPM : 0;
  setNeedle("vsi", angleForLinearGauge(vsiFpm, GAUGE_CONFIGS.vsi));
  document.getElementById("value-vsi").textContent = Math.round(vsiFpm);

  const heading = flight.heading_deg != null ? flight.heading_deg : 0;
  setNeedle("heading", heading);
  document.getElementById("value-heading").textContent = `${Math.round(heading)}°`;

  // Pitch is approximated as the climb angle (asin(vertical_rate / groundspeed)).
  // Bank angle has no equivalent field in OpenSky's free feed, so it stays at 0.
  let pitchDeg = 0;
  if (flight.velocity_ms > 1 && flight.vertical_rate_ms != null) {
    const ratio = Math.max(-1, Math.min(1, flight.vertical_rate_ms / flight.velocity_ms));
    pitchDeg = (Math.asin(ratio) * 180) / Math.PI;
  }
  const horizonShift = Math.max(-60, Math.min(60, pitchDeg * 3));
  document.getElementById("sky").setAttribute("y", -200 + horizonShift);
  document.getElementById("ground").setAttribute("y", 100 + horizonShift);
  document.getElementById("horizon-line").setAttribute("y1", 100 + horizonShift);
  document.getElementById("horizon-line").setAttribute("y2", 100 + horizonShift);
  document.getElementById("value-attitude").textContent = `${pitchDeg >= 0 ? "+" : ""}${pitchDeg.toFixed(1)}°`;
}

function renderProfile(profile) {
  profileEl.innerHTML = `
    <dt>Manufacturer</dt><dd>${profile.manufacturer}</dd>
    <dt>Model</dt><dd>${profile.model}</dd>
    <dt>Engines</dt><dd>${profile.engines} × ${profile.engine_type}</dd>
    <dt>Wingspan</dt><dd>${profile.wingspan_m} m</dd>
    <dt>Length</dt><dd>${profile.length_m} m</dd>
  `;
  blueprintEl.src = `/static/blueprints/${profile.category}.svg`;
  blueprintEl.alt = `${profile.manufacturer} ${profile.model} blueprint`;
}

async function refresh() {
  try {
    const response = await fetch(`/api/aircraft/${ICAO24}`);
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.error || `HTTP ${response.status}`);
    }
    const data = await response.json();
    errorEl.classList.add("hidden");
    renderProfile(data.profile);
    updateGauges(data.flight);
    statusEl.textContent = `${data.flight.callsign || data.flight.icao24} · updated ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    errorEl.textContent = `Error: ${err.message}`;
    errorEl.classList.remove("hidden");
  }
}

initGauges();
refresh();
setInterval(refresh, REFRESH_MS);
