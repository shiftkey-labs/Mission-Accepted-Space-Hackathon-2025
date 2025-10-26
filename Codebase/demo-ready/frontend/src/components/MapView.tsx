import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import parsedEnv from "../config/env";
import { useIceExtentContext } from "../context/IceExtentContext";
import AnimatedRouteOverlay, { type RouteControls } from "./routePredictions/AnimatedRouteOverlay";
import "./MapView.css";

type MapViewProps = {
  onRouteStatusChange?: (status: string) => void;
  onRouteControlsChange?: (controls: RouteControls) => void;
  predictedData?: GeoJSON.FeatureCollection | null;
};

const MapView = ({ onRouteStatusChange, onRouteControlsChange, predictedData }: MapViewProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const { data: iceData, isLoading } = useIceExtentContext();
  const accessToken = parsedEnv.VITE_MAPBOX_TOKEN;

  // Initialize the map
  useEffect(() => {
    if (!accessToken) {
      console.error("VITE_MAPBOX_TOKEN is missing; Mapbox map cannot initialize.");
      return;
    }

    if (mapRef.current || !mapContainer.current) return;

    mapboxgl.accessToken = accessToken;

    // set the default center of the map to hudson bay
    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/dark-v11",
      center: [-74.0060152, 40.7127281],
      zoom: 5,
      maxZoom: 6
    });
    mapRef.current = map;

    map.on("load", () => {
      setIsMapLoaded(true);
    });

    return () => {
      setIsMapLoaded(false);
      map.remove();
      mapRef.current = null;
    };
  }, [accessToken]);

  // Update ice extent data on the map
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !isMapLoaded || !iceData) return;

    // Remove previous layer/source if they exist
    if (map.getLayer("iceLoss-fill")) {
      map.removeLayer("iceLoss-fill");
    }
    if (map.getSource("iceLoss")) {
      map.removeSource("iceLoss");
    }

    // Add new source and layer
    map.addSource("iceLoss", {
      type: "geojson",
      data: iceData
    });

    map.addLayer({
      id: "iceLoss-fill",
      type: "circle",
      source: "iceLoss",
      paint: {
        "circle-radius": 3,
        "circle-color": "#ff4b4b",
        "circle-opacity": 0.7,
      },
    });
  }, [iceData, isMapLoaded]);

  // Update predicted data on the map (separate layer)
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !isMapLoaded) return;

    if (map.getLayer("predictedIce-fill")) {
      map.removeLayer("predictedIce-fill");
    }
    if (map.getSource("predictedIce")) {
      map.removeSource("predictedIce");
    }

    if (!predictedData) return;

    map.addSource("predictedIce", {
      type: "geojson",
      data: predictedData,
    });

    map.addLayer({
      id: "predictedIce-fill",
      type: "circle",
      source: "predictedIce",
      paint: {
        "circle-radius": 3,
        "circle-color": "#4bd7ff",
        "circle-opacity": 0.9,
      },
    });
  }, [predictedData, isMapLoaded]);

  return (
    <div className="map-container">
      <div ref={mapContainer} className="map-canvas" />
      {isLoading ? (
        <div className="map-loading-overlay" role="status" aria-live="polite">
          <div className="map-loading-spinner" />
          <div className="map-loading-text">Loading data…</div>
        </div>
      ) : null}
      <AnimatedRouteOverlay
        map={mapRef.current}
        isMapLoaded={isMapLoaded}
        onStatusChange={onRouteStatusChange}
        onControlsChange={onRouteControlsChange}
      />
    </div>
  );
};

export default MapView;
