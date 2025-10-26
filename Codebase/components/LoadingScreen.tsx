"use client"

import { motion } from "framer-motion"
import { Satellite } from "lucide-react"

export default function LoadingScreen() {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-background">
      <div className="text-center">
        <motion.div
          initial={{ scale: 0, rotate: 0 }}
          animate={{ scale: 1, rotate: 360 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-primary"
        >
          <Satellite className="h-10 w-10 text-primary-foreground" />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-2"
        >
          <h2 className="text-2xl font-bold text-foreground">Canadian Satellite Viz</h2>
          <p className="text-muted-foreground">Initializing orbital tracking system...</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-8 flex justify-center gap-2"
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1.5,
                repeat: Number.POSITIVE_INFINITY,
                delay: i * 0.2,
              }}
              className="h-2 w-2 rounded-full bg-primary"
            />
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-8 space-y-1 text-xs text-muted-foreground"
        >
          <p>Loading satellite ephemeris data...</p>
          <p>Calculating orbital parameters...</p>
          <p>Analyzing conjunction events...</p>
        </motion.div>
      </div>
    </div>
  )
}
