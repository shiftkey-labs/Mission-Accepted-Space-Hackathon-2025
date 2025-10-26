# Mission Accepted 2025

This fork adds realistic satellite propagation and Earth rotation:

- Satellite positions are now computed from TLEs using `satellite.js` when a NORAD ID is available (fetched from Celestrak).
- Earth rotates using the sidereal rotation rate (86164 seconds per revolution) and respects a simulation speed multiplier.
- Satellites without TLEs use a physically-plausible circular-orbit fallback based on altitude and inclination.

How to run:

```powershell
npm install
npm run dev
```

Notes:

- TLE fetching is done on-demand per satellite and cached in the client store.
- The scene scales Earth radius to 1 unit (so km positions from `satellite.js` are scaled by 1/6371).
