"use client";

import { Search, Menu, Satellite } from "lucide-react";
import { motion } from "framer-motion";

interface HeaderProps {
  onSearch: (query: string) => void;
  searchQuery: string;
  onToggleDashboard: () => void;
}

export default function Header({
  onSearch,
  searchQuery,
  onToggleDashboard,
}: HeaderProps) {
  return (
    <motion.header
      initial={{ y: -64, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="flex h-16 items-center justify-between border-b border-border bg-card px-6"
    >
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleDashboard}
          className="rounded-lg p-2 text-foreground transition-colors hover:bg-muted"
          aria-label="Toggle dashboard"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
            <Satellite className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-bold leading-tight text-foreground">
              Canadian Satellite Viz
            </h1>
            <p className="text-xs text-muted-foreground">
              Real-time Orbital Tracking
            </p>
          </div>
        </div>
      </div>

      <div className="relative w-96">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search satellites by name..."
          value={searchQuery}
          onChange={(e) => onSearch(e.target.value)}
          className="h-10 w-full rounded-lg border border-input bg-background pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
        />
      </div>

      <div className="flex items-center gap-2">
        <div className="rounded-lg bg-accent/10 px-3 py-1.5 text-xs font-medium text-accent">
          Real-time Satellite Tracking
        </div>
      </div>
    </motion.header>
  );
}
