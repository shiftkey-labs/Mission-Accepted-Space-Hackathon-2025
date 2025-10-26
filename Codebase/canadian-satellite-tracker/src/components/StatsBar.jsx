import React from 'react'
import { formatTime } from '../utils/dateUtils'

function StatsBar({ totalSatellites, activeSatellites, lastUpdate, isLoading, t }) {
  return (
    <div className="stats-bar">
      <div className="stat-item">
        <span className="stat-label">{t.stats.total}</span>
        <span className="stat-value">{totalSatellites}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">{t.stats.active}</span>
        <span className="stat-value stat-value-active">{activeSatellites}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">{t.stats.tracking}</span>
        <span className={`stat-value ${isLoading ? 'stat-loading' : 'stat-tracking'}`}>
          {isLoading ? '...' : '●'}
        </span>
      </div>
      <div className="stat-item">
        <span className="stat-label">{t.stats.lastUpdate}</span>
        <span className="stat-value stat-time">
          {lastUpdate ? formatTime(lastUpdate) : '--:--:--'}
        </span>
      </div>
    </div>
  )
}

export default StatsBar
