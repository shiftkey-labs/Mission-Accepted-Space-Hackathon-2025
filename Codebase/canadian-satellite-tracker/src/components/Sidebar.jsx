import React from 'react'
import SatelliteCard from './SatelliteCard'

function Sidebar({ 
  satellites, 
  selectedSatellite, 
  setSelectedSatellite, 
  filter, 
  setFilter, 
  searchQuery, 
  setSearchQuery, 
  t 
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <input
          type="text"
          className="search-input"
          placeholder={t.search}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            {t.filters.all}
          </button>
          <button
            className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
            onClick={() => setFilter('active')}
          >
            {t.filters.active}
          </button>
          <button
            className={`filter-btn ${filter === 'featured' ? 'active' : ''}`}
            onClick={() => setFilter('featured')}
          >
            {t.filters.featured}
          </button>
        </div>
      </div>

      <div className="satellite-list">
        {satellites.map(satellite => (
          <SatelliteCard
            key={satellite.id}
            satellite={satellite}
            isSelected={selectedSatellite?.id === satellite.id}
            onClick={() => setSelectedSatellite(satellite)}
            t={t}
          />
        ))}
        
        {satellites.length === 0 && (
          <div className="no-results">
            No satellites found
          </div>
        )}
      </div>
    </aside>
  )
}

export default Sidebar
