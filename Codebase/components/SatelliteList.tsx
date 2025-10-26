"use client"

import { motion } from "framer-motion"
import { Satellite, MapPin, Gauge } from "lucide-react"
import type { SatellitePosition } from "@/lib/types"

interface SatelliteListProps {
  satellites: SatellitePosition[]
  selectedSatellite: number | null
  onSatelliteSelect: (noradId: number) => void
}

export default function SatelliteList({ satellites, selectedSatellite, onSatelliteSelect }: SatelliteListProps) {
  return (
    <div className="space-y-2">
      {satellites.map((sat, index) => (
        <motion.button
          key={sat.noradId}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.05 }}
          onClick={() => onSatelliteSelect(sat.noradId)}
          className={`w-full rounded-lg border p-3 text-left transition-all ${
            selectedSatellite === sat.noradId
              ? "border-accent bg-accent/10 shadow-lg shadow-accent/20"
              : "border-border bg-card hover:border-primary hover:bg-muted"
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <div
                className={`mt-0.5 rounded-lg p-2 ${
                  selectedSatellite === sat.noradId
                    ? "bg-accent text-accent-foreground"
                    : "bg-primary text-primary-foreground"
                }`}
              >
                <Satellite className="h-4 w-4" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-foreground leading-tight">{sat.name}</h3>
                <p className="text-xs text-muted-foreground mt-0.5">NORAD {sat.noradId}</p>
              </div>
            </div>
            {selectedSatellite === sat.noradId && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="h-2 w-2 rounded-full bg-accent animate-pulse-glow"
              />
            )}
          </div>

          <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <MapPin className="h-3 w-3" />
              <span>{sat.altitude.toFixed(0)} km</span>
            </div>
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <Gauge className="h-3 w-3" />
              <span>{sat.velocity.toFixed(2)} km/s</span>
            </div>
          </div>

          <div className="mt-2 text-xs text-muted-foreground">
            {sat.latitude.toFixed(2)}°, {sat.longitude.toFixed(2)}°
          </div>
        </motion.button>
      ))}

      {satellites.length === 0 && (
        <div className="rounded-lg border border-dashed border-border p-8 text-center">
          <Satellite className="mx-auto h-12 w-12 text-muted-foreground opacity-50" />
          <p className="mt-2 text-sm text-muted-foreground">No satellites found</p>
        </div>
      )}
    </div>
  )
}
