import * as satellite from '../data/satellites'

// Fetch TLE data from CelesTrak
export async function fetchTLEData() {
  const tleData = {};
  try {
    // Build comma-separated list of NORAD catalog IDs from SATELLITES array
    const noradIds = SATELLITES.map(sat => sat.noradId).join(',');

    // Fetch TLE data from your backend, passing all relevant NORAD IDs
    const response = await fetch(`http://localhost:5000/api/tle?norad=${noradIds}`);
    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }
    const data = await response.json();

    // Parse and store TLE data by NORAD ID
    data.forEach(sat => {
      tleData[sat.NORAD_CAT_ID] = {
        line1: sat.TLE_LINE1,
        line2: sat.TLE_LINE2,
        name: sat.OBJECT_NAME
      };
    });
  } catch (error) {
    console.error('Error fetching TLE data:', error);
  }
  return tleData;
}

// Propagate satellite position
export function propagateSatellite(tle, date) {
  try {
    const satrec = satellite.twoline2satrec(tle.line1, tle.line2)
    const positionAndVelocity = satellite.propagate(satrec, date)
    
    if (positionAndVelocity.position && typeof positionAndVelocity.position !== 'boolean') {
      const positionEci = positionAndVelocity.position
      const gmst = satellite.gstime(date)
      const positionGd = satellite.eciToGeodetic(positionEci, gmst)
      
      return {
        latitude: satellite.degreesLat(positionGd.latitude),
        longitude: satellite.degreesLong(positionGd.longitude),
        altitude: positionGd.height,
        velocity: calculateVelocity(positionAndVelocity.velocity)
      }
    }
  } catch (error) {
    console.error('Error propagating satellite:', error)
  }
  
  return null
}

// Calculate velocity magnitude
function calculateVelocity(velocity) {
  if (velocity && typeof velocity !== 'boolean') {
    const vx = velocity.x
    const vy = velocity.y
    const vz = velocity.z
    return Math.sqrt(vx * vx + vy * vy + vz * vz)
  }
  return 0
}

// Calculate orbital period
export function calculateOrbitalPeriod(tle) {
  try {
    const satrec = satellite.twoline2satrec(tle.line1, tle.line2)
    const meanMotion = satrec.no // revolutions per day
    return 1440 / meanMotion // minutes per orbit
  } catch (error) {
    return 0
  }
}

// Calculate satellite passes over a location
export function calculatePasses(tle, observerLat, observerLon, observerAlt = 0, days = 7) {
  const passes = []
  const satrec = satellite.twoline2satrec(tle.line1, tle.line2)
  const now = new Date()
  const endDate = new Date(now.getTime() + days * 24 * 60 * 60 * 1000)
  
  const observerGd = {
    latitude: observerLat * (Math.PI / 180),
    longitude: observerLon * (Math.PI / 180),
    height: observerAlt / 1000 // convert to km
  }
  
  // Check every minute for passes
  for (let time = now.getTime(); time <= endDate.getTime(); time += 60000) {
    const date = new Date(time)
    const positionAndVelocity = satellite.propagate(satrec, date)
    
    if (positionAndVelocity.position && typeof positionAndVelocity.position !== 'boolean') {
      const positionEci = positionAndVelocity.position
      const gmst = satellite.gstime(date)
      const positionEcf = satellite.eciToEcf(positionEci, gmst)
      
      const lookAngles = satellite.ecfToLookAngles(observerGd, positionEcf)
      const elevation = lookAngles.elevation * (180 / Math.PI)
      
      // If satellite is above horizon (elevation > 0)
      if (elevation > 0) {
        // Check if this is a new pass
        if (passes.length === 0 || time - passes[passes.length - 1].endTime > 600000) {
          passes.push({
            startTime: date,
            endTime: date,
            maxElevation: elevation,
            maxElevationTime: date
          })
        } else {
          // Update current pass
          const currentPass = passes[passes.length - 1]
          currentPass.endTime = date
          if (elevation > currentPass.maxElevation) {
            currentPass.maxElevation = elevation
            currentPass.maxElevationTime = date
          }
        }
      }
    }
  }
  
  return passes.slice(0, 5) // Return first 5 passes
}


