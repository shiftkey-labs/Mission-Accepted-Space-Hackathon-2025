"use client";
import dynamic from "next/dynamic";
import type {
  SatellitePosition,
  OrbitPath,
  ConjunctionEvent,
} from "@/lib/types";

// Dynamically import Globe to avoid SSR issues
const Globe = dynamic(() => import("./Globe"), { ssr: false });

interface GlobeViewerProps {
  satellites: SatellitePosition[];
  orbits: OrbitPath[];
  conjunctions: ConjunctionEvent[];
  selectedSatellite: number | null;
  onSatelliteClick: (noradId: number) => void;
}

export default function GlobeViewer({
  satellites,
  orbits,
  conjunctions,
  selectedSatellite,
  onSatelliteClick,
}: GlobeViewerProps) {
  return (
    <div className="globe-container h-full w-full">
      <Globe
        satellites={satellites}
        orbits={orbits}
        conjunctions={conjunctions}
        selectedSatellite={selectedSatellite}
        onSatelliteClick={onSatelliteClick}
      />
    </div>
  );
}
