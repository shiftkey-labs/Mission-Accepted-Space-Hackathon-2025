"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Play, Pause, RotateCcw, FastForward, Rewind, Clock } from "lucide-react"
import { format, addMinutes } from "date-fns"

interface TimeControlsProps {
  timeOffset: number
  isPlaying: boolean
  onTimeChange: (offset: number) => void
  onPlayPause: () => void
  onReset: () => void
}

export default function TimeControls({ timeOffset, isPlaying, onTimeChange, onPlayPause, onReset }: TimeControlsProps) {
  const [speed, setSpeed] = useState(1)

  const currentTime = addMinutes(new Date(), timeOffset)
  const isRealTime = Math.abs(timeOffset) < 1

  const handleSpeedChange = (newSpeed: number) => {
    setSpeed(newSpeed)
  }

  const handleSkip = (minutes: number) => {
    onTimeChange(timeOffset + minutes)
  }

  return (
    <motion.div
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.3 }}
      className="absolute bottom-6 left-1/2 -translate-x-1/2"
    >
      <div className="rounded-xl border border-border bg-card/95 p-4 shadow-2xl backdrop-blur-sm">
        <div className="mb-3 flex items-center justify-center gap-2 text-sm">
          <Clock className="h-4 w-4 text-primary" />
          <span className="font-mono font-medium text-foreground">{format(currentTime, "yyyy-MM-dd HH:mm:ss")}</span>
          {!isRealTime && (
            <span className="rounded bg-accent/20 px-2 py-0.5 text-xs font-medium text-accent">
              {timeOffset > 0 ? "+" : ""}
              {Math.round(timeOffset)} min
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Skip backward */}
          <button
            onClick={() => handleSkip(-60)}
            className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            aria-label="Skip backward 1 hour"
          >
            <Rewind className="h-5 w-5" />
          </button>

          {/* Skip backward 10 min */}
          <button
            onClick={() => handleSkip(-10)}
            className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            aria-label="Skip backward 10 minutes"
          >
            <Rewind className="h-4 w-4" />
          </button>

          {/* Play/Pause */}
          <button
            onClick={onPlayPause}
            className="rounded-lg bg-primary p-3 text-primary-foreground transition-all hover:bg-primary/90 hover:scale-105"
            aria-label={isPlaying ? "Pause" : "Play"}
          >
            {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
          </button>

          {/* Skip forward 10 min */}
          <button
            onClick={() => handleSkip(10)}
            className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            aria-label="Skip forward 10 minutes"
          >
            <FastForward className="h-4 w-4" />
          </button>

          {/* Skip forward */}
          <button
            onClick={() => handleSkip(60)}
            className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            aria-label="Skip forward 1 hour"
          >
            <FastForward className="h-5 w-5" />
          </button>

          {/* Divider */}
          <div className="mx-1 h-8 w-px bg-border" />

          {/* Reset */}
          <button
            onClick={onReset}
            className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground disabled:opacity-50"
            disabled={isRealTime}
            aria-label="Reset to current time"
          >
            <RotateCcw className="h-5 w-5" />
          </button>
        </div>

        {/* Speed control */}
        <div className="mt-3 flex items-center justify-center gap-2">
          <span className="text-xs text-muted-foreground">Speed:</span>
          {[0.5, 1, 2, 5, 10].map((s) => (
            <button
              key={s}
              onClick={() => handleSpeedChange(s)}
              className={`rounded px-2 py-1 text-xs font-medium transition-colors ${
                speed === s
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
