import { twoline2satrec, propagate, gstime, eciToGeodetic } from 'satellite.js';

const EARTH_RADIUS_KM = 6371;

export function getOrbitPositions(tle1, tle2, numPoints = 150, startDate = new Date()) {
  const satrec = twoline2satrec(tle1, tle2);
  const start = startDate instanceof Date ? startDate : new Date(startDate);
  const periodMinutes = (2 * Math.PI) / satrec.no;
  const dtMs = (periodMinutes * 60 * 1000) / numPoints;

  const points = [];
  for (let i = 0; i < numPoints; i++) {
    const t = new Date(start.getTime() + i * dtMs);
    const pv = propagate(satrec, t);
    if (!pv.position) continue;

    const { x, y, z } = pv.position;
    points.push([x, y, z]);
  }

  return points;
}

export function getPositionAtTime(tle1, tle2, date) {
  const satrec = twoline2satrec(tle1, tle2);
  const pv = propagate(satrec, date);

  if (!pv.position) return null;

  const { x, y, z } = pv.position;
  return { x, y, z };
}

export function getGroundTrack(tle1, tle2, durationMin = 90, stepSec = 30) {
  const satrec = twoline2satrec(tle1, tle2);
  const start = new Date();
  const numPoints = Math.floor((durationMin * 60) / stepSec);
  const points = [];

  for (let i = 0; i < numPoints; i++) {
    const t = new Date(start.getTime() + i * stepSec * 1000);
    const pv = propagate(satrec, t);
    if (!pv.position) continue;
    const gmst = gstime(t);
    const gd = eciToGeodetic(pv.position, gmst);
    points.push({ lat: gd.latitude, lon: gd.longitude, altKm: gd.height });
  }
  return points;
}

export function geoToCartesianKm(latRad, lonRad, altKm = 0) {
  const r = EARTH_RADIUS_KM + altKm;
  const cosLat = Math.cos(latRad);
  const sinLat = Math.sin(latRad);
  const cosLon = Math.cos(lonRad);
  const sinLon = Math.sin(lonRad);
  const x = r * cosLat * cosLon;
  const y = r * sinLat; // Y up
  const z = r * cosLat * sinLon;
  return [x, y, z];
}

export { EARTH_RADIUS_KM };
