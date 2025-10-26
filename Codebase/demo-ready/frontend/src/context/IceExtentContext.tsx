import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { FeatureCollection } from "geojson";
import { fetchIceExtentCoordinates } from "../services/iceExtentAPI";
import { fetchAvailableDates } from "../services/availabilityAPI";
import type { IceExtentResponse } from "../types";
import type { IceExtentContextValue } from "../types";

const IceExtentContext = createContext<IceExtentContextValue | undefined>(undefined);

const isoFromDate = (date: Date) => {
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

const dateFromIso = (iso: string): Date | null => {
  const parts = iso.split("-");
  if (parts.length !== 3) return null;
  const [yearStr, monthStr, dayStr] = parts;
  const year = Number.parseInt(yearStr, 10);
  const month = Number.parseInt(monthStr, 10);
  const day = Number.parseInt(dayStr, 10);
  if (!Number.isFinite(year) || !Number.isFinite(month) || !Number.isFinite(day)) {
    return null;
  }
  const dt = new Date(Date.UTC(year, month - 1, day));
  if (Number.isNaN(dt.getTime())) return null;
  return dt;
};

const EMPTY_COLLECTION: FeatureCollection = {
  type: "FeatureCollection",
  features: [],
};

export const IceExtentProvider = ({ children }: { children: ReactNode }) => {
  // Use a default date that will be updated once we have available dates
  const [selectedDate, setSelectedDate] = useState<Date>(() => new Date(Date.UTC(2000, 0, 1)));
  const [data, setData] = useState<FeatureCollection | null>(null);
  const [availableDates, setAvailableDates] = useState<string[]>([]);
  const [metadata, setMetadata] = useState<Omit<IceExtentResponse, "feature_collection"> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>();
  const [reloadToken, setReloadToken] = useState(0);

  const isoDate = useMemo(() => isoFromDate(selectedDate), [selectedDate]);

  // Load available dates and snap to nearest valid on first load
  useEffect(() => {
    let isActive = true;
    fetchAvailableDates()
      .then((list) => {
        if (!isActive) return;
        setAvailableDates(list);
        if (list.length > 0) {
          // Always select the latest available date
          const latestDate = list[list.length - 1];
          const dt = dateFromIso(latestDate);
          if (dt) setSelectedDate(dt);
        }
      })
      .catch(() => setAvailableDates([]));
    return () => { isActive = false; };
  }, []);

  const refetch = useCallback(() => {
    setReloadToken((token) => token + 1);
  }, []);

  useEffect(() => {
    let isActive = true;
    setIsLoading(true);
    setError(undefined);

    fetchIceExtentCoordinates(isoDate)
      .then((response) => {
        if (!isActive) return;
        setData(response.feature_collection ?? EMPTY_COLLECTION);
        const { feature_collection: _ignored, ...rest } = response;
        setMetadata(rest);
      })
      .catch((err: Error) => {
        if (!isActive) return;
        setError(err.message);
        setData(null);
        setMetadata(null);
      })
      .finally(() => {
        if (isActive) setIsLoading(false);
      });

    return () => {
      isActive = false;
    };
  }, [isoDate, reloadToken, selectedDate]);

  const shiftDate = useCallback((days: number) => {
    if (!Number.isFinite(days) || !days) return;
    setSelectedDate((prev) => {
      const next = new Date(prev);
      next.setUTCDate(next.getUTCDate() + days);
      return next;
    });
  }, []);

  const setDateFromIso = useCallback((iso: string) => {
    const parsed = dateFromIso(iso);
    if (!parsed) return;
    setSelectedDate(parsed);
  }, []);

  const value: IceExtentContextValue = useMemo(
    () => ({
      selectedDate,
      isoDate,
      availableDates,
      data,
      metadata,
      isLoading,
      error,
      shiftDate,
      setDateFromIso,
      refetch,
    }),
    [availableDates, data, error, isLoading, isoDate, metadata, refetch, selectedDate, setDateFromIso, shiftDate]
  );

  return <IceExtentContext.Provider value={value}>{children}</IceExtentContext.Provider>;
};

export const useIceExtentContext = () => {
  const ctx = useContext(IceExtentContext);
  if (!ctx) {
    throw new Error("useIceExtentContext must be used within an IceExtentProvider");
  }
  return ctx;
};
