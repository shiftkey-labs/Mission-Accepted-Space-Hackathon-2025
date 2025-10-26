// API Response types for fetch, Request, and Response
import type { Position, FeatureCollection } from "geojson";

export type IceExtentContextValue = {
  selectedDate: Date;
  isoDate: string;
  availableDates: string[];
  data: FeatureCollection | null;
  metadata: Omit<IceExtentResponse, "feature_collection"> | null;
  isLoading: boolean;
  error?: string;
  shiftDate: (days: number) => void;
  setDateFromIso: (isoDate: string) => void;
  refetch: () => void;
};


export type IceExtentResponse = {
  date: string;
  source: string;
  radius_km: number;
  feature_collection: FeatureCollection;
};

export type AvailableDatesResponse = {
  count: number;
  dates: string[]; // ISO YYYY-MM-DD
};

export type YearResponse = {
  year: number;
  radius_km: number;
  days: Array<{
    date: string; // YYYY-MM-DD
    source: string;
    feature_collection: FeatureCollection;
  }>;
};

export interface PredictionRequest {
  start: Position;
  end: Position;
}

