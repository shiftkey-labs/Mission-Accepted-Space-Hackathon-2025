import type { FeatureCollection } from "geojson";
import api from "../api/mapAPI";

export const predictIceExtent = async (
  date: string,
  radiusKm = 500,
  thresh = 0.5
): Promise<FeatureCollection> => {
  try {
    const response = await api.get<FeatureCollection>("/ice_extent/predict", {
      params: { date, radius_km: radiusKm, thresh },
    });
    return response.data as unknown as FeatureCollection;
  } catch (err: any) {
    const status = err?.response?.status ?? "network";
    throw new Error(`Prediction request failed! (${status})`);
  }
};
