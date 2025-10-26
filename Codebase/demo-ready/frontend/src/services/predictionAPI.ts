
import type { Position, FeatureCollection } from "geojson";
import api from "../api/mapAPI";
import type { PredictionRequest } from "../types";

/**
 * Request a route prediction between two points
 * @param start Starting coordinates [longitude, latitude]
 * @param end Destination coordinates [longitude, latitude]
 * @returns Promise with GeoJSON FeatureCollection containing the predicted route
 */
export const getRoutePrediction = async (start: Position, end: Position): Promise<FeatureCollection> => {
  const response = await api.post<FeatureCollection>("/route_prediction", { start, end });
  return response.data;
};

/**
 * Request route prediction with validation
 * Includes type checking and coordinate validation
 */
export const requestPrediction = async (params: PredictionRequest): Promise<FeatureCollection> => {
  // Validate coordinates
  const [startLon, startLat] = params.start;
  const [endLon, endLat] = params.end;

  if (!isValidCoordinate(startLon, startLat) || !isValidCoordinate(endLon, endLat)) {
    throw new Error("Invalid coordinates provided");
  }

  return getRoutePrediction(params.start, params.end);
};

// Helper to validate coordinate bounds
const isValidCoordinate = (lon: number, lat: number): boolean => {
  return (
    typeof lon === "number" &&
    typeof lat === "number" &&
    lon >= -180 &&
    lon <= 180 &&
    lat >= -90 &&
    lat <= 90
  );
};