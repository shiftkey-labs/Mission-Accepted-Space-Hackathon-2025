import { useMemo, useState, useCallback, useRef, useEffect } from "react";
import { useIceExtentContext } from "../context/IceExtentContext";
import "./Calendar.css";

export const Calendar = () => {
  const { isoDate, setDateFromIso, availableDates, selectedDate, isLoading } = useIceExtentContext();

  // Ensure dates are sorted in ascending order
  const list = useMemo(() => {
    const sorted = [...(availableDates ?? [])].sort((a, b) => a.localeCompare(b));
    return sorted;
  }, [availableDates]);

  const max = Math.max(list.length - 1, 0);
  const sliderIndex = useMemo(() => Math.max(0, list.indexOf(isoDate)), [list, isoDate]);

  const [isSliding, setIsSliding] = useState(false);
  const [pendingIndex, setPendingIndex] = useState<number | null>(null);

  const commitPendingIndex = useCallback(() => {
    setIsSliding(false);
    setPendingIndex((idx) => {
      if (idx === null) return null;
      const iso = list[Math.min(Math.max(idx, 0), max)];
      if (iso && iso !== isoDate) {
        setDateFromIso(iso);
      }
      return null;
    });
  }, [isoDate, list, max, setDateFromIso]);

  const handleStart = useCallback(() => setIsSliding(true), []);
  const handleEnd = useCallback(() => {
    commitPendingIndex();
  }, [commitPendingIndex]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const idx = Math.min(Math.max(0, Number(e.target.value)), list.length - 1);
    setPendingIndex(idx);
  }, [list.length]);

  const formatDateOnly = (d?: Date | null) => {
    if (!d) return "";
    const y = d.getUTCFullYear();
    const m = String(d.getUTCMonth() + 1).padStart(2, "0");
    const day = String(d.getUTCDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
  };

  // Calculate bubble position as percent across the track
  const activeIndex = pendingIndex ?? sliderIndex;
  const percent = max > 0 ? (activeIndex / max) * 100 : 0;
  const bubbleRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (bubbleRef.current) {
      bubbleRef.current.style.left = `${percent}%`;
    }
  }, [percent]);

  const bubbleDate = useMemo(() => {
    if (pendingIndex !== null) {
      const iso = list[Math.min(Math.max(pendingIndex, 0), max)];
      if (iso) {
        return new Date(`${iso}T00:00:00Z`);
      }
    }
    return selectedDate;
  }, [list, max, pendingIndex, selectedDate]);

  return (
    <div className="calendar-horizontal">
      <div className="calendar-horizontal__inner">
        {/* year labels */}
        <div className="calendar-horizontal__years">
          <div className="calendar-horizontal__year--start">{list[0]?.slice(0, 4) ?? ""}</div>
          <div className="calendar-horizontal__year--end">{list[list.length - 1]?.slice(0, 4) ?? ""}</div>
        </div>

        {/* floating bubble above thumb - left percentage is dynamic */}
        <div
          aria-hidden
          ref={bubbleRef}
          className={`calendar-horizontal__bubble ${isSliding ? "is-sliding" : ""}`}
        >
          {isSliding || isLoading ? (
            <div className="calendar-horizontal__bubble-inner">
              <span className="calendar-horizontal__spinner" aria-hidden />
              <span className="calendar-horizontal__bubble-text">{formatDateOnly(bubbleDate)}</span>
            </div>
          ) : null}
        </div>

        {/* slider */}
        <input
          className="calendar-horizontal__slider"
          aria-label="date-slider"
          type="range"
          min={0}
          max={max}
          step={1}
          value={Math.min(Math.max(activeIndex, 0), max)}
          onChange={handleChange}
          onMouseDown={handleStart}
          onTouchStart={handleStart}
          onMouseUp={handleEnd}
          onTouchEnd={handleEnd}
          onTouchCancel={handleEnd}
          onKeyDown={handleStart}
          onKeyUp={handleEnd}
          onBlur={handleEnd}
          disabled={list.length === 0}
        />
      </div>
    </div>
  );
};
