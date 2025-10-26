"use client";

import { useEffect, useState, useMemo, useRef } from "react";
import Globe from "react-globe.gl";
import * as THREE from "three";
import {
  splitOrbitPathAtDiscontinuities,
  EARTH_RADIUS_KM,
} from "@/lib/satelliteUtils";
import type {
  SatellitePosition,
  OrbitPath,
  ConjunctionEvent,
} from "@/lib/types";

interface GlobeProps {
  satellites: SatellitePosition[];
  orbits: OrbitPath[];
  conjunctions: ConjunctionEvent[];
  selectedSatellite: number | null;
  onSatelliteClick: (noradId: number) => void;
}

export default function GlobeComponent({
  satellites,
  orbits,
  conjunctions,
  selectedSatellite,
  onSatelliteClick,
}: GlobeProps) {
  const [globeReady, setGlobeReady] = useState(false);
  const globeRef = useRef<any>();

  // Prepare satellite objects data - render as 3D spheres
  const satelliteObjects = useMemo(() => {
    return satellites.map((sat) => ({
      lat: sat.latitude,
      lng: sat.longitude,
      alt: sat.altitude / EARTH_RADIUS_KM, // Normalize to Earth radii
      noradId: sat.noradId,
      name: sat.name,
      velocity: sat.velocity,
      altitude: sat.altitude,
      isSelected: sat.noradId === selectedSatellite,
    }));
  }, [satellites, selectedSatellite]);

  // Prepare orbital paths data - render as a single continuous path
  const pathsData = useMemo(() => {
    if (orbits.length === 0) return [];

    // Only show orbital path for selected satellite
    const selectedOrbit = orbits.find(
      (orbit) => orbit.noradId === selectedSatellite
    );

    if (!selectedOrbit) return [];

    // Build one continuous path from the provided positions
    const coords = selectedOrbit.positions.map((p) => ({
      lat: p.lat,
      lng: p.lng,
      alt: p.alt / EARTH_RADIUS_KM,
    }));

    console.log(
      `[Globe] Rendering continuous path with ${coords.length} points`
    );

    return [
      {
        coords,
        id: `${selectedOrbit.noradId}`,
      },
    ];
  }, [orbits, selectedSatellite]);

  useEffect(() => {
    setGlobeReady(true);
  }, []);

  if (!globeReady) {
    return <div className="h-full w-full bg-slate-950" />;
  }

  return (
    <Globe
      ref={globeRef}
      // Globe appearance
      globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
      bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
      backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
      atmosphereColor="rgba(59, 130, 246, 0.3)"
      atmosphereAltitude={0.12}
      // Satellite objects - rendered as 3D spheres
      objectsData={satelliteObjects}
      objectLat="lat"
      objectLng="lng"
      objectAltitude="alt"
      objectThreeObject={(d: any) => {
        // Create a sphere for each satellite
        const radius = d.isSelected ? 8 : 4; // Larger for selected
        const geometry = new THREE.SphereGeometry(radius, 16, 16);
        const material = new THREE.MeshBasicMaterial({
          color: d.isSelected ? 0xff0000 : 0x00ffff, // Red or cyan
          transparent: true,
          opacity: 0.9,
        });
        const sphere = new THREE.Mesh(geometry, material);

        // Add a glow effect for selected satellite
        if (d.isSelected) {
          const glowGeometry = new THREE.SphereGeometry(radius * 1.3, 16, 16);
          const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0xff0000,
            transparent: true,
            opacity: 0.3,
          });
          const glow = new THREE.Mesh(glowGeometry, glowMaterial);
          sphere.add(glow);
        }

        return sphere;
      }}
      objectLabel={(d: any) => `
        <div style="background: rgba(10, 15, 35, 0.95); padding: 12px; border-radius: 8px; border: 1px solid ${
          d.isSelected ? "#ff0000" : "#00ffff"
        }; color: rgb(240, 250, 255); font-family: system-ui; max-width: 250px;">
          <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: ${
            d.isSelected ? "#ff0000" : "#00ffff"
          };">${d.name}</div>
          <div style="font-size: 12px; line-height: 1.6;">
            <div><strong>NORAD ID:</strong> ${d.noradId}</div>
            <div><strong>Altitude:</strong> ${d.altitude.toFixed(1)} km</div>
            <div><strong>Velocity:</strong> ${d.velocity.toFixed(2)} km/s</div>
            <div><strong>Position:</strong> ${d.lat.toFixed(
              2
            )}°, ${d.lng.toFixed(2)}°</div>
          </div>
        </div>
      `}
      onObjectClick={(obj: any) => onSatelliteClick(obj.noradId)}
      // Orbital paths
      pathsData={pathsData}
      pathPoints="coords"
      pathPointLat={(p: any) => p.lat}
      pathPointLng={(p: any) => p.lng}
      pathPointAlt={(p: any) => p.alt}
      pathColor={() => "#ffff00"} // Bright yellow
      pathStroke={2.5} // Slightly thinner
      pathDashLength={0} // No dashing - solid line
      pathDashGap={0}
      pathDashAnimateTime={0}
      pathTransitionDuration={0}
      // Disable all other layers
      pointsData={[]} // Explicitly disable points layer
      arcsData={[]}
      hexBinPointsData={[]}
      hexPolygonsData={[]}
      labelsData={[]}
      ringsData={[]}
      // Camera controls
      animateIn={false}
    />
  );
}
