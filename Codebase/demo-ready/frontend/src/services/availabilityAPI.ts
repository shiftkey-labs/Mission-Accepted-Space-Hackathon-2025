import api from "../api/mapAPI";
import type { AvailableDatesResponse } from "../types";

export const fetchAvailableDates = async (): Promise<string[]> => {
  try {
      const res = await api.get<AvailableDatesResponse>("/ice_extent/available_dates");
      console.log("Available dates response:", res.data);
      return res.data.dates ?? [];
  } catch (err: any) { 
    const status = err?.response?.status ?? "network";
    throw new Error(`Available dates request failed! (${status})`);
  }
};

