"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { TrendingUp, AlertCircle } from "lucide-react";
import type { ConjunctionEvent } from "@/lib/types";

interface RiskChartProps {
  conjunctions: ConjunctionEvent[];
}

export default function RiskChart({ conjunctions }: RiskChartProps) {
  // Handle empty state
  if (!conjunctions || conjunctions.length === 0) {
    return (
      <div className="space-y-4">
        <div className="rounded-lg border border-border bg-card p-8 text-center">
          <AlertCircle className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold text-foreground mb-2">
            No Conjunction Data
          </h3>
          <p className="text-sm text-muted-foreground">
            No conjunction events are currently available for analysis.
          </p>
        </div>
      </div>
    );
  }

  const riskDistribution = useMemo(() => {
    const distribution = { high: 0, medium: 0, low: 0 };
    conjunctions.forEach((conj) => {
      distribution[conj.riskLevel]++;
    });
    return [
      { name: "High Risk", value: distribution.high, color: "#ef4444" },
      { name: "Medium Risk", value: distribution.medium, color: "#f59e0b" },
      { name: "Low Risk", value: distribution.low, color: "#6b7280" },
    ];
  }, [conjunctions]);

  const timelineData = useMemo(() => {
    const now = new Date();
    const buckets = [
      { name: "0-6h", count: 0 },
      { name: "6-12h", count: 0 },
      { name: "12-24h", count: 0 },
      { name: "24-48h", count: 0 },
      { name: "48h+", count: 0 },
    ];

    conjunctions.forEach((conj) => {
      if (!conj.tca || !(conj.tca instanceof Date)) return;
      const hoursUntil =
        (conj.tca.getTime() - now.getTime()) / (1000 * 60 * 60);
      if (hoursUntil < 6) buckets[0].count++;
      else if (hoursUntil < 12) buckets[1].count++;
      else if (hoursUntil < 24) buckets[2].count++;
      else if (hoursUntil < 48) buckets[3].count++;
      else buckets[4].count++;
    });

    return buckets;
  }, [conjunctions]);

  // More meaningful analytics calculations
  const maxProbability =
    conjunctions.length > 0
      ? Math.max(...conjunctions.map((c) => c.probability))
      : 0;
  const avgProbability =
    conjunctions.length > 0
      ? conjunctions.reduce((sum, c) => sum + c.probability, 0) /
        conjunctions.length
      : 0;

  // Calculate risk-weighted metrics
  const highRiskCount =
    riskDistribution.find((r) => r.name === "High Risk")?.value || 0;
  const mediumRiskCount =
    riskDistribution.find((r) => r.name === "Medium Risk")?.value || 0;
  const lowRiskCount =
    riskDistribution.find((r) => r.name === "Low Risk")?.value || 0;

  // Calculate time-based urgency
  const now = new Date();
  const urgentConjunctions = conjunctions.filter((conj) => {
    if (!conj.tca || !(conj.tca instanceof Date)) return false;
    const hoursUntil = (conj.tca.getTime() - now.getTime()) / (1000 * 60 * 60);
    return hoursUntil <= 24 && conj.riskLevel === "high";
  }).length;

  // Calculate average minimum range
  const avgMinRange =
    conjunctions.length > 0
      ? conjunctions.reduce((sum, c) => sum + c.minRange, 0) /
        conjunctions.length
      : 0;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <AlertCircle className="h-4 w-4" />
            <span>Total Conjunctions</span>
          </div>
          <p className="mt-2 text-2xl font-bold text-foreground">
            {conjunctions.length}
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Active collision risks
          </p>
        </div>

        <div className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <AlertCircle className="h-4 w-4 text-destructive" />
            <span>Urgent High Risk</span>
          </div>
          <p className="mt-2 text-2xl font-bold text-destructive">
            {urgentConjunctions}
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            High risk within 24h
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-4">
          <div className="flex items-center gap-2 text-sm text-destructive">
            <AlertCircle className="h-4 w-4" />
            <span>High Risk</span>
          </div>
          <p className="mt-2 text-xl font-bold text-destructive">
            {highRiskCount}
          </p>
          <p className="text-xs text-destructive/70 mt-1">
            {conjunctions.length > 0
              ? `${((highRiskCount / conjunctions.length) * 100).toFixed(1)}%`
              : "0%"}{" "}
            of total
          </p>
        </div>

        <div className="rounded-lg border border-yellow-500/20 bg-yellow-500/5 p-4">
          <div className="flex items-center gap-2 text-sm text-yellow-600">
            <AlertCircle className="h-4 w-4" />
            <span>Medium Risk</span>
          </div>
          <p className="mt-2 text-xl font-bold text-yellow-600">
            {mediumRiskCount}
          </p>
          <p className="text-xs text-yellow-600/70 mt-1">
            {conjunctions.length > 0
              ? `${((mediumRiskCount / conjunctions.length) * 100).toFixed(1)}%`
              : "0%"}{" "}
            of total
          </p>
        </div>

        <div className="rounded-lg border border-muted-foreground/20 bg-muted-foreground/5 p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <AlertCircle className="h-4 w-4" />
            <span>Low Risk</span>
          </div>
          <p className="mt-2 text-xl font-bold text-muted-foreground">
            {lowRiskCount}
          </p>
          <p className="text-xs text-muted-foreground/70 mt-1">
            {conjunctions.length > 0
              ? `${((lowRiskCount / conjunctions.length) * 100).toFixed(1)}%`
              : "0%"}{" "}
            of total
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <TrendingUp className="h-4 w-4" />
            <span>Max Collision Probability</span>
          </div>
          <p className="mt-2 text-2xl font-bold text-foreground">
            {(maxProbability * 100).toExponential(2)}%
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Highest individual risk
          </p>
        </div>

        <div className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <TrendingUp className="h-4 w-4" />
            <span>Average Min Range</span>
          </div>
          <p className="mt-2 text-2xl font-bold text-foreground">
            {avgMinRange.toFixed(1)} km
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Closest approach distance
          </p>
        </div>
      </div>

      <div className="rounded-lg border border-border bg-card p-4">
        <h3 className="mb-4 text-sm font-semibold text-foreground">
          Risk Distribution
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={riskDistribution}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {riskDistribution.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value, name) => [
                `${value} events (${
                  conjunctions.length > 0
                    ? ((value / conjunctions.length) * 100).toFixed(1)
                    : 0
                }%)`,
                name,
              ]}
              contentStyle={{
                backgroundColor: "rgb(10, 15, 35)",
                border: "1px solid rgb(30, 41, 59)",
                borderRadius: "8px",
                color: "rgb(240, 250, 255)",
              }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="mt-4 space-y-2">
          {riskDistribution.map((item) => (
            <div
              key={item.name}
              className="flex items-center justify-between text-xs"
            >
              <div className="flex items-center gap-2">
                <div
                  className="h-3 w-3 rounded"
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-muted-foreground">{item.name}</span>
              </div>
              <span className="font-medium text-foreground">{item.value}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-lg border border-border bg-card p-4">
        <h3 className="mb-4 text-sm font-semibold text-foreground">
          Time to Closest Approach
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={timelineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgb(30, 41, 59)" />
            <XAxis
              dataKey="name"
              stroke="rgb(156, 163, 175)"
              style={{ fontSize: "12px" }}
            />
            <YAxis stroke="rgb(156, 163, 175)" style={{ fontSize: "12px" }} />
            <Tooltip
              formatter={(value, name) => [`${value} conjunctions`, "Count"]}
              labelFormatter={(label) => `Timeframe: ${label}`}
              contentStyle={{
                backgroundColor: "rgb(10, 15, 35)",
                border: "1px solid rgb(30, 41, 59)",
                borderRadius: "8px",
                color: "rgb(240, 250, 255)",
              }}
            />
            <Bar
              dataKey="count"
              fill="rgb(59, 130, 246)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
