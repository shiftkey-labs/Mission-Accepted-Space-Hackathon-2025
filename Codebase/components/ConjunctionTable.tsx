"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import { AlertTriangle, Clock, TrendingUp } from "lucide-react";
import { format } from "date-fns";
import type { ConjunctionEvent } from "@/lib/types";
import { CANADIAN_SATELLITES } from "@/lib/canadianSatellites";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface ConjunctionTableProps {
  conjunctions: ConjunctionEvent[];
  onSatelliteSelect: (noradId: number) => void;
}

export default function ConjunctionTable({
  conjunctions,
  onSatelliteSelect,
}: ConjunctionTableProps) {
  // Risk level priority for sorting
  const getRiskPriority = (level: string): number => {
    switch (level) {
      case "high":
        return 3;
      case "medium":
        return 2;
      case "low":
        return 1;
      default:
        return 0;
    }
  };

  // Convert probability to readable format (e.g., "1 in 75,000")
  const formatProbability = (probability: number): string => {
    if (probability <= 0) return "0";
    if (probability >= 1) return "1 in 1";

    const inverse = Math.round(1 / probability);
    return `1 in ${inverse.toLocaleString()}`;
  };

  // Group conjunctions by satellite
  const conjunctionsBySatellite = useMemo(() => {
    const grouped: Record<number, ConjunctionEvent[]> = {};

    // Initialize with all Canadian satellites
    CANADIAN_SATELLITES.forEach((sat) => {
      grouped[sat.noradId] = [];
    });

    // Group conjunctions by satellite
    conjunctions.forEach((conj) => {
      const sat1 = CANADIAN_SATELLITES.find((s) => s.noradId === conj.noradId1);
      const sat2 = CANADIAN_SATELLITES.find((s) => s.noradId === conj.noradId2);

      if (sat1) {
        if (!grouped[conj.noradId1]) grouped[conj.noradId1] = [];
        grouped[conj.noradId1].push(conj);
      }
      if (sat2) {
        if (!grouped[conj.noradId2]) grouped[conj.noradId2] = [];
        grouped[conj.noradId2].push(conj);
      }
    });

    // Sort conjunctions for each satellite by collision risk (probability descending, then min range ascending)
    Object.keys(grouped).forEach((noradId) => {
      grouped[Number(noradId)].sort((a, b) => {
        // Primary sort: probability (descending - highest risk first)
        const probDiff = b.probability - a.probability;
        if (probDiff !== 0) return probDiff;

        // Secondary sort: minimum range (ascending - closest first)
        return a.minRange - b.minRange;
      });
    });

    return grouped;
  }, [conjunctions]);

  const getRiskColor = (level: string) => {
    switch (level) {
      case "high":
        return "text-destructive";
      case "medium":
        return "text-yellow-500";
      default:
        return "text-muted-foreground";
    }
  };

  const getRiskBg = (level: string) => {
    switch (level) {
      case "high":
        return "bg-destructive/10 border-destructive";
      case "medium":
        return "bg-yellow-500/10 border-yellow-500";
      default:
        return "bg-muted border-border";
    }
  };

  return (
    <div className="space-y-3">
      <div className="rounded-lg border border-border bg-card p-3">
        <div className="flex items-center gap-2 text-sm">
          <AlertTriangle className="h-4 w-4 text-yellow-500" />
          <span className="font-medium text-foreground font-mono">
            {conjunctions.length} Active Conjunctions
          </span>
        </div>
        <p className="mt-1 text-xs text-muted-foreground">
          Monitoring potential collision events
        </p>
      </div>

      <Accordion type="single" collapsible className="w-full">
        {CANADIAN_SATELLITES.sort((a, b) => {
          const aConjunctions = conjunctionsBySatellite[a.noradId]?.length || 0;
          const bConjunctions = conjunctionsBySatellite[b.noradId]?.length || 0;
          return bConjunctions - aConjunctions; // Most conjunctions first
        }).map((satellite) => {
          const satelliteConjunctions =
            conjunctionsBySatellite[satellite.noradId] || [];

          return (
            <AccordionItem
              key={satellite.noradId}
              value={`satellite-${satellite.noradId}`}
            >
              <AccordionTrigger className="hover:no-underline">
                <div className="flex items-center justify-between w-full pr-4">
                  <div className="flex items-center gap-3">
                    <div className="text-left">
                      <div className="font-semibold text-foreground font-mono">
                        {satellite.name}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {satellite.purpose}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {satelliteConjunctions.length > 0 && (
                      <span className="rounded-full bg-destructive/10 px-2 py-0.5 text-xs font-mono text-destructive">
                        {satelliteConjunctions.length}
                      </span>
                    )}
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                {satelliteConjunctions.length > 0 ? (
                  <div className="space-y-2 pt-2">
                    {satelliteConjunctions.map((conj, index) => (
                      <motion.div
                        key={conj.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className={`rounded-lg border p-3 ${getRiskBg(
                          conj.riskLevel
                        )}`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <AlertTriangle
                                className={`h-3 w-3 ${getRiskColor(
                                  conj.riskLevel
                                )}`}
                              />
                              <span
                                className={`text-xs font-bold uppercase ${getRiskColor(
                                  conj.riskLevel
                                )}`}
                              >
                                {conj.riskLevel} Risk
                              </span>
                            </div>

                            <div className="mt-2 space-y-1">
                              <button
                                onClick={() => onSatelliteSelect(conj.noradId1)}
                                className="block text-sm font-semibold text-foreground hover:text-primary transition-colors font-mono"
                              >
                                {conj.satellite1}
                              </button>
                              <div className="text-xs text-muted-foreground">
                                ↕
                              </div>
                              <button
                                onClick={() => onSatelliteSelect(conj.noradId2)}
                                className="block text-sm font-semibold text-foreground hover:text-primary transition-colors font-mono"
                              >
                                {conj.satellite2}
                              </button>
                            </div>
                          </div>
                        </div>

                        <div className="mt-2 grid grid-cols-2 gap-2 border-t border-border/50 pt-2">
                          <div>
                            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              <span>TCA</span>
                            </div>
                            <p className="mt-1 text-xs font-medium text-foreground font-mono">
                              {format(conj.tca, "MMM dd, HH:mm")}
                            </p>
                          </div>

                          <div>
                            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                              <TrendingUp className="h-3 w-3" />
                              <span>Min Range</span>
                            </div>
                            <p className="mt-1 text-xs font-medium text-foreground font-mono">
                              {conj.minRange.toFixed(3)} km
                            </p>
                          </div>
                        </div>

                        <div className="mt-2 grid grid-cols-2 gap-2">
                          <div>
                            <div className="text-xs text-muted-foreground">
                              Dilution Threshold
                            </div>
                            <p className="mt-1 text-xs font-medium text-foreground font-mono">
                              {conj.dilutionThreshold
                                ? conj.dilutionThreshold.toFixed(3)
                                : "N/A"}{" "}
                              km
                            </p>
                          </div>

                          <div>
                            <div className="text-xs text-muted-foreground">
                              Relative Speed
                            </div>
                            <p className="mt-1 text-xs font-medium text-foreground font-mono">
                              {conj.relativeVelocity.toFixed(3)} km/s
                            </p>
                          </div>
                        </div>

                        <div className="mt-2 rounded bg-background/50 p-2">
                          <div className="text-xs text-muted-foreground">
                            Collision Probability
                          </div>
                          <div className="mt-1 text-sm font-bold text-foreground font-mono">
                            {formatProbability(conj.probability)}
                          </div>
                          <div className="text-xs text-muted-foreground mt-1">
                            ({(conj.probability * 100).toExponential(2)}%)
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="py-4 text-center">
                    <p className="text-sm text-muted-foreground font-mono">
                      No conjunctions detected
                    </p>
                  </div>
                )}
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </div>
  );
}
