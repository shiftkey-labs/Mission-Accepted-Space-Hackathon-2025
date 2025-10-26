"use client";

import { motion } from "framer-motion";
import { Satellite, AlertTriangle, Activity, Globe } from "lucide-react";
import type { SatellitePosition, ConjunctionEvent } from "@/lib/types";

interface StatsOverlayProps {
  satellites: SatellitePosition[];
  conjunctions: ConjunctionEvent[];
}

export default function StatsOverlay({
  satellites,
  conjunctions,
}: StatsOverlayProps) {
  const activeSatellites = satellites?.length || 0;
  const highRiskConjunctions =
    conjunctions?.filter((c) => c.riskLevel === "high").length || 0;
  const totalConjunctions = conjunctions?.length || 0;

  // Calculate more meaningful metrics
  const averageAltitude =
    satellites?.length > 0
      ? satellites.reduce((sum, sat) => sum + sat.altitude, 0) /
        satellites.length
      : 0;
  const averageVelocity =
    satellites?.length > 0
      ? satellites.reduce((sum, sat) => sum + sat.velocity, 0) /
        satellites.length
      : 0;

  // Calculate urgent conjunctions (high risk within 24 hours)
  const now = new Date();
  const urgentConjunctions =
    conjunctions?.filter((conj) => {
      if (!conj.tca || !(conj.tca instanceof Date)) return false;
      const hoursUntil =
        (conj.tca.getTime() - now.getTime()) / (1000 * 60 * 60);
      return hoursUntil <= 24 && conj.riskLevel === "high";
    }).length || 0;

  const stats = [
    {
      icon: Satellite,
      label: "Active Satellites",
      value: activeSatellites,
      color: "text-primary",
    },
    {
      icon: AlertTriangle,
      label: "Total Conjunctions",
      value: totalConjunctions,
      color: "text-orange-500",
    },
    {
      icon: AlertTriangle,
      label: "High Risk Events",
      value: highRiskConjunctions,
      color: "text-destructive",
    },
    {
      icon: Activity,
      label: "Urgent (24h)",
      value: urgentConjunctions,
      color: "text-red-600",
    },
  ];

  return (
    <motion.div
      initial={{ x: 100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay: 0.2 }}
      className="absolute right-6 top-6 space-y-3"
    >
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 + index * 0.1 }}
          className="rounded-lg border border-border bg-card/95 p-3 shadow-lg backdrop-blur-sm"
        >
          <div className="flex items-center gap-3">
            <div className={`rounded-lg bg-muted p-2 ${stat.color}`}>
              <stat.icon className="h-4 w-4" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">{stat.label}</p>
              <p className="text-lg font-bold text-foreground">{stat.value}</p>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
}
