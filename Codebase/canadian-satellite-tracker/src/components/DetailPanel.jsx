import React, { useState, useEffect } from 'react'
import { formatDate, calculateYearsInOrbit, formatDuration } from '../utils/dateUtils'
import { calculateOrbitalPeriod, calculatePasses } from '../utils/tleUtils'
import { CANADIAN_CITIES } from '../data/satellites'

function DetailPanel({ satellite, onClose, selectedCity, setSelectedCity, t, language }) {
  const [passes, setPasses] = useState([])
  const [isCalculating, setIsCalculating] = useState(false)
  
  const yearsInOrbit = calculateYearsInOrbit(satellite.launchDate)
  const description = language === 'fr' ? satellite.descriptionFr : satellite.descriptionEn
  
  useEffect(() => {
    if (satellite.tle && selectedCity) {
      setIsCalculating(true)
      const city = CANADIAN_CITIES.find(c => c.id === selectedCity)
      
      setTimeout(() => {
        const calculatedPasses = calculatePasses(
          satellite.tle,
          city.lat,
          city.lon,
          0,
          7
        )
        setPasses(calculatedPasses)
        setIsCalculating(false)
      }, 500)
    }
  }, [satellite, selectedCity])
  
  const orbitalPeriod = satellite.tle ? calculateOrbitalPeriod(satellite.tle) : 0
  
  return (
    <div className="detail-panel">
      <div className="detail-header">
        <div>
          <h2>{satellite.name}</h2>
          <span className={`status-badge ${satellite.status}`}>
            {t.status[satellite.status]}
          </span>
        </div>
        <button className="close-btn" onClick={onClose}>✕</button>
      </div>
      
      <div className="detail-content">
        <section className="detail-section">
          <h3>{t.detail.mission}</h3>
          <p className="mission-description">{description}</p>
          
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">{t.detail.launched}</span>
              <span className="info-value">{formatDate(satellite.launchDate, language)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">{t.detail.yearsInOrbit}</span>
              <span className="info-value">{yearsInOrbit}</span>
            </div>
            <div className="info-item">
              <span className="info-label">{t.detail.operator}</span>
              <span className="info-value">{satellite.operator}</span>
            </div>
            <div className="info-item">
              <span className="info-label">{t.detail.type}</span>
              <span className="info-value">{t.types[satellite.type]}</span>
            </div>
          </div>
        </section>
        
        {satellite.position && (
          <section className="detail-section">
            <h3>{t.detail.orbit}</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">{t.detail.altitude}</span>
                <span className="info-value">{satellite.position.altitude.toFixed(2)} km</span>
              </div>
              <div className="info-item">
                <span className="info-label">{t.detail.velocity}</span>
                <span className="info-value">{satellite.position.velocity.toFixed(2)} km/s</span>
              </div>
              {orbitalPeriod > 0 && (
                <div className="info-item">
                  <span className="info-label">{t.detail.period}</span>
                  <span className="info-value">{formatDuration(orbitalPeriod)}</span>
                </div>
              )}
            </div>
          </section>
        )}
        
        {satellite.tle && satellite.status === 'active' && (
          <section className="detail-section">
            <h3>{t.detail.passes}</h3>
            
            <div className="city-select">
              <label>{t.detail.selectCity}:</label>
              <select 
                value={selectedCity} 
                onChange={(e) => setSelectedCity(e.target.value)}
                className="city-dropdown"
              >
                {CANADIAN_CITIES.map(city => (
                  <option key={city.id} value={city.id}>{city.name}</option>
                ))}
              </select>
            </div>
            
            {isCalculating ? (
              <div className="passes-loading">{t.detail.calculating}</div>
            ) : passes.length > 0 ? (
              <div className="passes-list">
                {passes.map((pass, index) => (
                  <div key={index} className="pass-item">
                    <div className="pass-time">
                      <strong>{t.detail.nextPass} {index + 1}:</strong>
                      <span>{formatDate(pass.startTime, language)} - {new Date(pass.startTime).toLocaleTimeString(language === 'fr' ? 'fr-CA' : 'en-CA')}</span>
                    </div>
                    <div className="pass-details">
                      <span>{t.detail.duration}: {formatDuration((pass.endTime - pass.startTime) / 60000)}</span>
                      <span>{t.detail.maxElevation}: {pass.maxElevation.toFixed(1)}°</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-passes">{t.detail.noPasses}</div>
            )}
          </section>
        )}
      </div>
    </div>
  )
}

export default DetailPanel
