export interface Satellite {
  noradId: number;
  name: string;
  line1: string;
  line2: string;
  launchDate?: string;
  status: "active" | "inactive" | "decayed";
  operator?: string;
  purpose?: string;
}

export interface SatellitePosition {
  noradId: number;
  name: string;
  latitude: number;
  longitude: number;
  altitude: number;
  velocity: number;
  timestamp: Date;
}

export interface ConjunctionEvent {
  id: string;
  satellite1: string;
  satellite2: string;
  noradId1: number;
  noradId2: number;
  tca: Date; // Time of Closest Approach
  minRange: number; // km
  probability: number; // 0-1
  relativeVelocity: number; // km/s
  riskLevel: "low" | "medium" | "high";
}

export interface OrbitPoint {
  lat: number;
  lng: number;
  alt: number;
}

export interface OrbitPath {
  noradId: number;
  positions: OrbitPoint[];
}
