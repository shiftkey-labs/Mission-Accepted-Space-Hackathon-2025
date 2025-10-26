"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import SatelliteList from "./SatelliteList"
import ConjunctionTable from "./ConjunctionTable"
import RiskChart from "./RiskChart"
import SatelliteDetails from "./SatelliteDetails"
import type { SatellitePosition, ConjunctionEvent, Satellite } from "@/lib/types"

interface DashboardProps {
  satellites: SatellitePosition[]
  conjunctions: ConjunctionEvent[]
  selectedSatellite: number | null
  onSatelliteSelect: (noradId: number) => void
  satelliteDetails: Satellite | null | undefined
}

export default function Dashboard({
  satellites,
  conjunctions,
  selectedSatellite,
  onSatelliteSelect,
  satelliteDetails,
}: DashboardProps) {
  const [activeTab, setActiveTab] = useState("satellites")

  return (
    <div className="flex h-full flex-col overflow-hidden">
      <div className="border-b border-border bg-card p-4">
        <h2 className="text-lg font-semibold text-foreground">Mission Control</h2>
        <p className="text-sm text-muted-foreground">Monitor Canadian space assets</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex flex-1 flex-col overflow-hidden">
        <TabsList className="mx-4 mt-4 grid w-[calc(100%-2rem)] grid-cols-3">
          <TabsTrigger value="satellites">Satellites</TabsTrigger>
          <TabsTrigger value="conjunctions">Conjunctions</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-hidden">
          <TabsContent value="satellites" className="h-full overflow-y-auto p-4 pt-2 m-0">
            {satelliteDetails && selectedSatellite ? (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-4">
                <SatelliteDetails satellite={satelliteDetails} onClose={() => onSatelliteSelect(selectedSatellite)} />
              </motion.div>
            ) : null}
            <SatelliteList
              satellites={satellites}
              selectedSatellite={selectedSatellite}
              onSatelliteSelect={onSatelliteSelect}
            />
          </TabsContent>

          <TabsContent value="conjunctions" className="h-full overflow-y-auto p-4 pt-2 m-0">
            <ConjunctionTable conjunctions={conjunctions} onSatelliteSelect={onSatelliteSelect} />
          </TabsContent>

          <TabsContent value="analytics" className="h-full overflow-y-auto p-4 pt-2 m-0">
            <RiskChart conjunctions={conjunctions} />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  )
}
