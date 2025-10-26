import React from 'react'
import { calculateYearsInOrbit } from '../utils/dateUtils'

function SatelliteCard({ satellite, isSelected, onClick, t }) {
  const yearsInOrbit = calculateYearsInOrbit(satellite.launchDate)
  
  return (
    <div 
      className={`satellite-card ${isSelected ? 'selected' : ''} ${satellite.featured ? 'featured' : ''}`}
      onClick={onClick}
    >
      <div className="satellite-card-header">
        <h3 className="satellite-name">{satellite.name}</h3>
        <span className={`status-badge ${satellite.status}`}>
          {t.status[satellite.status]}
        </span>
      </div>
      
      <div className="satellite-card-body">
        <div className="satellite-info">
          <span className="info-label">{t.types[satellite.type]}</span>
          <span className="info-value">{yearsInOrbit} {t.detail.yearsInOrbit.toLowerCase()}</span>
        </div>
        
        {satellite.position && (
          <div className="satellite-position">
            <div className="position-item">
              <span className="position-label">Lat:</span>
              <span className="position-value">{satellite.position.latitude.toFixed(2)}°</span>
            </div>
            <div className="position-item">
              <span className="position-label">Lon:</span>
              <span className="position-value">{satellite.position.longitude.toFixed(2)}°</span>
            </div>
            <div className="position-item">
              <span className="position-label">Alt:</span>
              <span className="position-value">{satellite.position.altitude.toFixed(0)} km</span>
            </div>
          </div>
        )}
      </div>
      
      {satellite.featured && (
        <div className="featured-badge">⭐</div>
      )}
    </div>
  )
}

export default SatelliteCard
