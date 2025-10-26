import * as satellite from "satellite.js";
import type { Satellite, SatellitePosition, OrbitPath } from "./types";

// Earth radius in kilometers
export const EARTH_RADIUS_KM = 6371;

/**
 * Convert geodetic coordinates (lat, lng, alt) to Cartesian (x, y, z)
 * Used for accurate orbital path rendering
 */
export function latLngAltToCartesian(
  lat: number,
  lng: number,
  alt: number
): { x: number; y: number; z: number } {
  const phi = (lat * Math.PI) / 180; // latitude in radians
  const theta = (lng * Math.PI) / 180; // longitude in radians
  const r = EARTH_RADIUS_KM + alt; // radius from Earth center

  return {
    x: r * Math.cos(phi) * Math.cos(theta),
    y: r * Math.cos(phi) * Math.sin(theta),
    z: r * Math.sin(phi),
  };
}

export function propagateSatellite(
  sat: Satellite,
  date: Date = new Date()
): SatellitePosition | null {
  try {
    const satrec = satellite.twoline2satrec(sat.line1, sat.line2);
    const positionAndVelocity = satellite.propagate(satrec, date);

    if (
      !positionAndVelocity ||
      typeof positionAndVelocity.position === "boolean" ||
      typeof positionAndVelocity.velocity === "boolean"
    ) {
      return null;
    }

    const positionEci = positionAndVelocity.position;
    const velocityEci = positionAndVelocity.velocity;

    if (!positionEci || !velocityEci) return null;

    const gmst = satellite.gstime(date);
    const positionGd = satellite.eciToGeodetic(positionEci, gmst);

    const velocity = Math.sqrt(
      velocityEci.x * velocityEci.x +
        velocityEci.y * velocityEci.y +
        velocityEci.z * velocityEci.z
    );

    return {
      noradId: sat.noradId,
      name: sat.name,
      latitude: satellite.degreesLat(positionGd.latitude),
      longitude: satellite.degreesLong(positionGd.longitude),
      altitude: positionGd.height,
      velocity,
      timestamp: date,
    };
  } catch (error) {
    console.error(`Error propagating satellite ${sat.name}:`, error);
    return null;
  }
}

export function generateOrbitPath(
  sat: Satellite,
  startDate: Date = new Date(),
  durationMinutes = 100,
  steps = 200
): OrbitPath {
  const positions: OrbitPath["positions"] = [];
  const stepMs = (durationMinutes * 60 * 1000) / steps;

  for (let i = 0; i <= steps; i++) {
    const date = new Date(startDate.getTime() + i * stepMs);
    const position = propagateSatellite(sat, date);

    if (position) {
      positions.push({
        lat: position.latitude,
        lng: position.longitude,
        alt: position.altitude,
      });
    }
  }

  return { noradId: sat.noradId, positions };
}

/**
 * Generate a smooth, closed orbital path for one full orbital period in the
 * Earth-centered inertial (ECI) frame. We convert all sampled ECI positions to
 * geodetic coordinates using a FIXED GMST taken at startDate. This prevents the
 * Earth's rotation from warping the path into a ground track and yields the
 * expected elliptical-looking orbit ring around the globe.
 */
export function generateInertialOrbitPath(
  sat: Satellite,
  startDate: Date = new Date(),
  steps = 512
): OrbitPath {
  const positions: OrbitPath["positions"] = [];

  try {
    const satrec = satellite.twoline2satrec(sat.line1, sat.line2);

    // Mean motion (rad/min). Orbital period (minutes) = 2π / no
    const meanMotionRadPerMin = satrec.no;
    if (!meanMotionRadPerMin || !isFinite(meanMotionRadPerMin)) {
      // Fallback to ~100 minutes if not available
      return generateOrbitPath(sat, startDate, 100, steps);
    }

    const periodMinutes = (2 * Math.PI) / meanMotionRadPerMin;
    const stepMs = (periodMinutes * 60 * 1000) / steps;

    // FIXED GMST so the orbit is shown in inertial space
    const fixedGmst = satellite.gstime(startDate);

    for (let i = 0; i <= steps; i++) {
      const date = new Date(startDate.getTime() + i * stepMs);
      const pv = satellite.propagate(satrec, date);
      if (
        !pv ||
        typeof pv.position === "boolean" ||
        typeof pv.velocity === "boolean" ||
        !pv.position
      ) {
        continue;
      }

      const gd = satellite.eciToGeodetic(pv.position, fixedGmst);
      positions.push({
        lat: satellite.degreesLat(gd.latitude),
        lng: satellite.degreesLong(gd.longitude),
        alt: gd.height,
      });
    }
  } catch (err) {
    console.error("Error generating inertial orbit path:", err);
    return generateOrbitPath(sat, startDate, 100, steps);
  }

  return { noradId: sat.noradId, positions };
}

/**
 * Split orbital path into segments to avoid discontinuities
 * Uses both Cartesian distance and longitude jumps to detect wrapping
 * This prevents weird connecting lines across the globe
 */
export function splitOrbitPathAtDiscontinuities(
  positions: OrbitPath["positions"],
  maxDistance = 800
): OrbitPath["positions"][] {
  if (positions.length === 0) return [];

  const segments: OrbitPath["positions"][] = [];
  let currentSegment: OrbitPath["positions"] = [positions[0]];

  const toCartesian = (point: OrbitPath["positions"][number]) =>
    latLngAltToCartesian(point.lat, point.lng, point.alt);

  for (let i = 1; i < positions.length; i++) {
    const prev = positions[i - 1];
    const curr = positions[i];

    // Check for longitude wrapping (anti-meridian crossing)
    const lngDiff = Math.abs(curr.lng - prev.lng);
    const isLongitudeWrap = lngDiff > 180;

    // Check Cartesian distance
    const prevCartesian = toCartesian(prev);
    const currCartesian = toCartesian(curr);
    const dx = currCartesian.x - prevCartesian.x;
    const dy = currCartesian.y - prevCartesian.y;
    const dz = currCartesian.z - prevCartesian.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

    // Split if there's a longitude wrap or large distance jump
    if (isLongitudeWrap || distance > maxDistance) {
      if (currentSegment.length > 0) {
        segments.push(currentSegment);
      }
      currentSegment = [curr];
    } else {
      currentSegment.push(curr);
    }
  }

  if (currentSegment.length > 0) {
    segments.push(currentSegment);
  }

  return segments.filter((seg) => seg.length > 1);
}

export function calculateDistance(
  pos1: SatellitePosition,
  pos2: SatellitePosition
): number {
  // Simple Euclidean distance in 3D space (km)
  const R = 6371; // Earth radius in km

  const lat1 = (pos1.latitude * Math.PI) / 180;
  const lon1 = (pos1.longitude * Math.PI) / 180;
  const lat2 = (pos2.latitude * Math.PI) / 180;
  const lon2 = (pos2.longitude * Math.PI) / 180;

  const x1 = (R + pos1.altitude) * Math.cos(lat1) * Math.cos(lon1);
  const y1 = (R + pos1.altitude) * Math.cos(lat1) * Math.sin(lon1);
  const z1 = (R + pos1.altitude) * Math.sin(lat1);

  const x2 = (R + pos2.altitude) * Math.cos(lat2) * Math.cos(lon2);
  const y2 = (R + pos2.altitude) * Math.cos(lat2) * Math.sin(lon2);
  const z2 = (R + pos2.altitude) * Math.sin(lat2);

  return Math.sqrt(
    Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2) + Math.pow(z2 - z1, 2)
  );
}
