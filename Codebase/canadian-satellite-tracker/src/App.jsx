import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import StatsBar from './components/StatsBar'
import Sidebar from './components/Sidebar'
import Map from './components/Map'
import DetailPanel from './components/DetailPanel'
import { SATELLITES } from './data/satellites'
import { translations } from './data/translations'
import { fetchTLEData, propagateSatellite } from './utils/tleUtils'
import './styles/App.css'

function App() {
  const [language, setLanguage] = useState('en')
  const [satellites, setSatellites] = useState(SATELLITES)
  const [selectedSatellite, setSelectedSatellite] = useState(null)
  const [filter, setFilter] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [lastUpdate, setLastUpdate] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedCity, setSelectedCity] = useState('ottawa')
  const t = translations[language]

  // 2-minute refresh (120000ms)
  useEffect(() => {
    const updateSatellites = () => {
      setIsLoading(true)
      try {
        const now = new Date()
        const updatedSatellites = SATELLITES.map(sat => {
          const tle = fetchTLEData(sat.noradId)
          if (tle && tle.line1 && tle.line2) {
            const position = propagateSatellite(tle, now)
            return { ...sat, position, tle }
          }
          return { ...sat, position: null, tle: null }
        })
        setSatellites(updatedSatellites)
        setLastUpdate(now)
      } catch (error) {
        console.error('Error updating satellites:', error)
      } finally {
        setIsLoading(false)
      }
    }

    updateSatellites()
    const interval = setInterval(updateSatellites, 120000) // 2 min
    return () => clearInterval(interval)
  }, [])

  // Filtering logic
  const filteredSatellites = satellites.filter(sat => {
    const matchesSearch =
      sat.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sat.SATNAME?.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesFilter =
      filter === 'all' ? true
        : filter === 'active' ? sat.status === 'active'
        : filter === 'featured' ? sat.featured
        : true
    return matchesSearch && matchesFilter
  })

  const activeSatellites = satellites.filter(sat => sat.status === 'active').length

  return (
    <div className="app-wrapper">
      <Header
        language={language}
        setLanguage={setLanguage}
        t={t}
      />
      <StatsBar
        t={t}
        total={satellites.length}
        active={activeSatellites}
        tracking={filteredSatellites.length}
        lastUpdate={lastUpdate}
        isLoading={isLoading}
      />
      <div className="main-content">
        <Sidebar
          satellites={filteredSatellites}
          selectedSatellite={selectedSatellite}
          setSelectedSatellite={setSelectedSatellite}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          filter={filter}
          setFilter={setFilter}
          t={t}
        />
        <Map
          satellites={filteredSatellites}
          selectedSatellite={selectedSatellite}
          setSelectedSatellite={setSelectedSatellite}
          t={t}
        />
      </div>
      {selectedSatellite && (
        <DetailPanel
          satellite={selectedSatellite}
          onClose={() => setSelectedSatellite(null)}
          selectedCity={selectedCity}
          setSelectedCity={setSelectedCity}
          t={t}
          language={language}
        />
      )}
    </div>
  )
}

export default App
