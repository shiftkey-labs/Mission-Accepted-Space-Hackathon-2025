"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Info, X, ExternalLink } from "lucide-react"

export default function InfoPanel() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.5 }}
        onClick={() => setIsOpen(true)}
        className="absolute bottom-6 right-6 rounded-full bg-primary p-3 text-primary-foreground shadow-lg transition-all hover:scale-110 hover:shadow-xl"
        aria-label="Show information"
      >
        <Info className="h-5 w-5" />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm"
            />

            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="fixed left-1/2 top-1/2 z-50 w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 rounded-xl border border-border bg-card p-6 shadow-2xl"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-foreground">About Canadian Satellite Viz</h2>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Real-time orbital tracking and conjunction analysis
                  </p>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  aria-label="Close"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="mt-6 space-y-4 text-sm leading-relaxed text-foreground">
                <p>
                  This application provides real-time visualization of Canadian satellites in orbit, tracking their
                  positions, orbital paths, and potential collision risks through conjunction analysis.
                </p>

                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <h3 className="mb-2 font-semibold text-foreground">Key Features</h3>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Interactive 3D globe with satellite tracking</li>
                    <li>• Real-time orbit propagation using SGP4/SDP4 algorithms</li>
                    <li>• Conjunction event monitoring and risk assessment</li>
                    <li>• Time simulation controls for future/past projections</li>
                    <li>• Comprehensive analytics and reporting</li>
                  </ul>
                </div>

                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <h3 className="mb-2 font-semibold text-foreground">Data Sources</h3>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Space-Track.org - TLE orbital elements</li>
                    <li>• Celestrak SOCRATES - Conjunction analysis</li>
                    <li>• Canadian Space Agency - Satellite information</li>
                  </ul>
                </div>

                <div className="rounded-lg border border-accent bg-accent/10 p-4">
                  <h3 className="mb-2 font-semibold text-accent">Educational Purpose</h3>
                  <p className="text-sm text-muted-foreground">
                    This tool is designed for educational and informational purposes. For operational space situational
                    awareness, please consult official sources and space agencies.
                  </p>
                </div>

                <div className="flex gap-3 pt-2">
                  <a
                    href="https://www.asc-csa.gc.ca/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                  >
                    Canadian Space Agency
                    <ExternalLink className="h-4 w-4" />
                  </a>
                  <a
                    href="https://www.space-track.org/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-muted"
                  >
                    Space-Track.org
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
