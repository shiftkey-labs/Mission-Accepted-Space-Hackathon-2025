import { useCallback, useState } from "react";
import { Calendar } from "../components/Calendar";
import MapView from "../components/MapView";
import RightStatsPanel from "../components/RightStatsPanel";
import type { RouteControls } from "../components/routePredictions/AnimatedRouteOverlay";
import { predictIceExtent } from "../services/icePredictionAPI";
import type { FeatureCollection } from "geojson";

const HomePage = () => {
  const [routeStatus, setRouteStatus] = useState("idle");
  const [routeControls, setRouteControls] = useState<RouteControls>({
    clearMarkers: () => {},
    hasMarkers: false,
  });
  const [predictedData, setPredictedData] = useState<FeatureCollection | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [predictError, setPredictError] = useState<string | null>(null);

  // form state for prediction
  const [predictDate, setPredictDate] = useState<string>("2026-01-01");
  const [predictRadius, setPredictRadius] = useState<number>(500);
  const [predictThresh, setPredictThresh] = useState<number>(0.5);

  const handleRouteControlsChange = useCallback((controls: RouteControls) => {
    setRouteControls((prev) => {
      if (prev.clearMarkers === controls.clearMarkers && prev.hasMarkers === controls.hasMarkers) {
        return prev;
      }
      return controls;
    });
  }, []);

  const routeStatusLabel =
    routeStatus === "requesting"
      ? "Calculating route..."
      : routeControls.hasMarkers
      ? "Pins ready. Start animation on map."
      : "Tap the map twice to set route pins.";

  return (
    <div className="app-shell">
      <div className="map-frame">
        <div className="tool-bar">
          <div id="mission-tools-panel">
            <div className="tool-card tool-card--stacked tool-card--route">
              <h3>Route Tools</h3>
              <button
                type="button"
                onClick={routeControls.clearMarkers}
                disabled={!routeControls.hasMarkers || routeStatus === "requesting"}
              >
                Clear pins
              </button>
              <span className="animated-route-status">{routeStatusLabel}</span>
            </div>
            <div className="tool-card tool-card--stacked tool-card--predict">
              <h3>Predict Ice</h3>
              <label>
                Date
                <input
                  type="date"
                  value={predictDate}
                  onChange={(e) => setPredictDate(e.target.value)}
                />
              </label>
              <label>
                Radius (km)
                <input
                  type="number"
                  value={predictRadius}
                  onChange={(e) => setPredictRadius(Number(e.target.value))}
                />
              </label>
              <label>
                Threshold
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  value={predictThresh}
                  onChange={(e) => setPredictThresh(Number(e.target.value))}
                />
              </label>
              <div className="predict-controls">
                <button
                  type="button"
                  onClick={async () => {
                    setPredicting(true);
                    setPredictError(null);
                    try {
                      const result = await predictIceExtent(predictDate, predictRadius, predictThresh);
                      setPredictedData(result);
                    } catch (err: any) {
                      setPredictError(err?.message ?? String(err));
                      setPredictedData(null);
                    } finally {
                      setPredicting(false);
                    }
                  }}
                  disabled={predicting}
                >
                  {predicting ? "Predicting…" : "Predict"}
                </button>
                <button type="button" onClick={() => setPredictedData(null)} disabled={predicting}>
                  Clear
                </button>
              </div>
              {predictError ? <div className="error">{predictError}</div> : null}
            </div>
          </div>
        </div>

        {/* Persistent vertical date slider, independent of the tool bar */}
        <Calendar />

        <MapView
          onRouteStatusChange={setRouteStatus}
          onRouteControlsChange={handleRouteControlsChange}
          predictedData={predictedData}
        />
      </div>
      <RightStatsPanel />
    </div>
  );
};

export default HomePage;
