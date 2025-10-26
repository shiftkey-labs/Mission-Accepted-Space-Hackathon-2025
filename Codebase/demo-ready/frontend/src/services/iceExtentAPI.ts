import type { IceExtentResponse } from "../types";
import api from "../api/mapAPI";

export const fetchIceExtentCoordinates = async (
  date: string,
  radiusKm = 500
): Promise<IceExtentResponse> => {
  try {
      const response = await api.get<IceExtentResponse>("/ice_extent", {
      params: { date, radius_km: radiusKm },
    });
    return response.data;
  } catch (err: any) {
    const status = err?.response?.status ?? "network";
    throw new Error(`Ice extent request failed! (${status})`);
  }
};
