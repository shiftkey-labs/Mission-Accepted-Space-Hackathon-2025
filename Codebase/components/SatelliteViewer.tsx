"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import GlobeViewer from "./GlobeViewer";
import Dashboard from "./Dashboard";
import Header from "./Header";
import StatsOverlay from "./StatsOverlay";
import InfoPanel from "./InfoPanel";
import LoadingScreen from "./LoadingScreen";
import {
  propagateSatellite,
  generateInertialOrbitPath,
} from "@/lib/satelliteUtils";
import type {
  SatellitePosition,
  OrbitPath,
  ConjunctionEvent,
  Satellite,
} from "@/lib/types";

export default function SatelliteViewer() {
  const [satellites, setSatellites] = useState<SatellitePosition[]>([]);
  const [orbits, setOrbits] = useState<OrbitPath[]>([]);
  const [conjunctions, setConjunctions] = useState<ConjunctionEvent[]>([]);
  const [selectedSatellite, setSelectedSatellite] = useState<number | null>(
    null
  );
  const [searchQuery, setSearchQuery] = useState("");
  const [showDashboard, setShowDashboard] = useState(true);
  const [loading, setLoading] = useState(true);
  const [satelliteData, setSatelliteData] = useState<Satellite[]>([]);

  // Initial data fetch
  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("[SatelliteViewer] Fetching satellite data from API...");

        const satellitesResponse = await fetch("/api/satellites");
        const satellitesData: Satellite[] = await satellitesResponse.json();
        console.log(
          "[SatelliteViewer] Fetched satellites:",
          satellitesData.length
        );
        setSatelliteData(satellitesData);

        console.log("[SatelliteViewer] Fetching conjunction data from API...");
        // Add cache-busting timestamp to ensure fresh data
        const conjunctionsResponse = await fetch("/api/conjunctions", {
          cache: "no-store",
          headers: {
            "Cache-Control": "no-cache",
          },
        });
        const conjunctionsData: ConjunctionEvent[] =
          await conjunctionsResponse.json();
        console.log(
          "[SatelliteViewer] Fetched conjunctions:",
          conjunctionsData.length
        );
        setConjunctions(conjunctionsData);

        setTimeout(() => {
          setLoading(false);
        }, 1500);
      } catch (error) {
        console.error("[SatelliteViewer] Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Periodic refresh of conjunction data (every 5 minutes)
  useEffect(() => {
    const fetchConjunctions = async () => {
      try {
        console.log("[SatelliteViewer] Refreshing conjunction data...");
        // Add cache-busting timestamp to ensure fresh data
        const conjunctionsResponse = await fetch("/api/conjunctions", {
          cache: "no-store",
          headers: {
            "Cache-Control": "no-cache",
          },
        });
        const conjunctionsData: ConjunctionEvent[] =
          await conjunctionsResponse.json();
        console.log(
          "[SatelliteViewer] Refreshed conjunctions:",
          conjunctionsData.length
        );
        setConjunctions(conjunctionsData);
      } catch (error) {
        console.error(
          "[SatelliteViewer] Error refreshing conjunctions:",
          error
        );
      }
    };

    // Set up interval to refresh every 5 minutes (300000 ms)
    const interval = setInterval(fetchConjunctions, 300000);

    return () => clearInterval(interval);
  }, []);

  // Update satellite positions in real-time
  useEffect(() => {
    if (loading || satelliteData.length === 0) return;

    const updatePositions = () => {
      const currentDate = new Date(); // Always use current real time

      const positions = satelliteData
        .map((sat) => propagateSatellite(sat, currentDate))
        .filter((pos): pos is SatellitePosition => pos !== null);

      setSatellites(positions);

      // Generate orbital path only for selected satellite
      if (selectedSatellite !== null) {
        const selectedSat = satelliteData.find(
          (s) => s.noradId === selectedSatellite
        );
        if (selectedSat) {
          const path = generateInertialOrbitPath(selectedSat, currentDate);
          setOrbits([path]);
          console.log(
            `[SatelliteViewer] Generated orbital path for ${selectedSat.name}`
          );
        }
      } else {
        setOrbits([]);
      }
    };

    // Initial update
    updatePositions();

    // Update positions every 5 seconds for real-time tracking
    const interval = setInterval(updatePositions, 5000);

    return () => clearInterval(interval);
  }, [selectedSatellite, loading, satelliteData]);

  const handleSatelliteClick = useCallback((noradId: number) => {
    setSelectedSatellite((prev) => (prev === noradId ? null : noradId));
  }, []);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const filteredSatellites = satellites.filter(
    (sat) =>
      sat.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sat.noradId.toString().includes(searchQuery)
  );

  const selectedSatelliteData = selectedSatellite
    ? satelliteData.find((s) => s.noradId === selectedSatellite)
    : null;

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <div className="relative h-screen w-full overflow-hidden bg-background">
      <Header
        onSearch={handleSearch}
        searchQuery={searchQuery}
        onToggleDashboard={() => setShowDashboard(!showDashboard)}
      />

      <div className="flex h-[calc(100vh-64px)] w-full">
        <AnimatePresence>
          {showDashboard && (
            <motion.div
              initial={{ x: -400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -400, opacity: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="h-full w-96 flex-shrink-0 border-r border-border bg-card"
            >
              <Dashboard
                satellites={filteredSatellites}
                conjunctions={conjunctions}
                selectedSatellite={selectedSatellite}
                onSatelliteSelect={handleSatelliteClick}
                satelliteDetails={selectedSatelliteData}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <div className="relative flex-1">
          <GlobeViewer
            satellites={satellites}
            orbits={orbits}
            conjunctions={conjunctions}
            selectedSatellite={selectedSatellite}
            onSatelliteClick={handleSatelliteClick}
          />

          <StatsOverlay satellites={satellites} conjunctions={conjunctions} />

          <InfoPanel />
        </div>
      </div>
    </div>
  );
}
