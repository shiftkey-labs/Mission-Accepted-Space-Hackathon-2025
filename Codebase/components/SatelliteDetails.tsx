"use client"

import { motion } from "framer-motion"
import { X, Calendar, Radio, Target, Info } from "lucide-react"
import type { Satellite } from "@/lib/types"

interface SatelliteDetailsProps {
  satellite: Satellite
  onClose: () => void
}

export default function SatelliteDetails({ satellite, onClose }: SatelliteDetailsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="rounded-lg border border-accent bg-accent/5 p-4"
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-bold text-foreground font-mono">{satellite.name}</h3>
        </div>
        <button
          onClick={onClose}
          className="rounded-lg p-1 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          aria-label="Close details"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="mt-4 space-y-3">
        {satellite.launchDate && (
          <div className="flex items-start gap-3">
            <Calendar className="mt-0.5 h-4 w-4 text-primary" />
            <div>
              <p className="text-xs text-muted-foreground">Launch Date</p>
              <p className="text-sm font-medium text-foreground">{satellite.launchDate}</p>
            </div>
          </div>
        )}

        {satellite.operator && (
          <div className="flex items-start gap-3">
            <Radio className="mt-0.5 h-4 w-4 text-primary" />
            <div>
              <p className="text-xs text-muted-foreground">Operator</p>
              <p className="text-sm font-medium text-foreground">{satellite.operator}</p>
            </div>
          </div>
        )}

        {satellite.purpose && (
          <div className="flex items-start gap-3">
            <Target className="mt-0.5 h-4 w-4 text-primary" />
            <div>
              <p className="text-xs text-muted-foreground">Mission</p>
              <p className="text-sm font-medium text-foreground">{satellite.purpose}</p>
            </div>
          </div>
        )}

        <div className="flex items-start gap-3">
          <Info className="mt-0.5 h-4 w-4 text-primary" />
          <div>
            <p className="text-xs text-muted-foreground">Status</p>
            <div className="mt-1 flex items-center gap-2">
              <div
                className={`h-2 w-2 rounded-full ${
                  satellite.status === "active" ? "bg-accent animate-pulse-glow" : "bg-muted-foreground"
                }`}
              />
              <p className="text-sm font-medium capitalize text-foreground">{satellite.status}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 rounded-lg bg-background/50 p-3">
        <p className="text-xs leading-relaxed text-muted-foreground">
          This satellite is part of Canada's space infrastructure, contributing to national security, scientific
          research, and Earth observation capabilities.
        </p>
      </div>
    </motion.div>
  )
}
