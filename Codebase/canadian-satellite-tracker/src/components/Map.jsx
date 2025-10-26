import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix Leaflet default marker icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

// Custom satellite icon
const createSatelliteIcon = (isActive, isFeatured) => {
  const color = isFeatured ? '#FFD700' : isActive ? '#32B8C6' : '#626C71'
  const size = isFeatured ? 14 : 10
  
  return L.divIcon({
    className: 'satellite-marker',
    html: `<div style="
      width: ${size}px;
      height: ${size}px;
      background: ${color};
      border: 2px solid white;
      border-radius: 50%;
      box-shadow: 0 0 10px ${color};
      animation: pulse 2s infinite;
    "></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2]
  })
}

// Component to handle map updates
function MapUpdater({ satellites, selectedSatellite }) {
  const map = useMap()
  
  useEffect(() => {
    if (selectedSatellite?.position) {
      map.setView(
        [selectedSatellite.position.latitude, selectedSatellite.position.longitude],
        4,
        { animate: true }
      )
    }
  }, [selectedSatellite, map])
  
  return null
}

function Map({ satellites, selectedSatellite, setSelectedSatellite }) {
  return (
    <div className="map-container">
      <MapContainer
        center={[56.1304, -106.3468]} // Center of Canada
        zoom={3}
        style={{ height: '100%', width: '100%' }}
        minZoom={2}
        maxZoom={8}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        
        {satellites.map(satellite => {
          if (!satellite.position) return null
          
          return (
            <Marker
              key={satellite.id}
              position={[satellite.position.latitude, satellite.position.longitude]}
              icon={createSatelliteIcon(satellite.status === 'active', satellite.featured)}
              eventHandlers={{
                click: () => setSelectedSatellite(satellite)
              }}
            >
              <Popup>
                <div style={{ minWidth: '200px' }}>
                  <h3 style={{ margin: '0 0 10px 0', color: '#21808D' }}>{satellite.name}</h3>
                  <p style={{ margin: '5px 0' }}>
                    <strong>Status:</strong> {satellite.status}
                  </p>
                  <p style={{ margin: '5px 0' }}>
                    <strong>Type:</strong> {satellite.type}
                  </p>
                  <p style={{ margin: '5px 0' }}>
                    <strong>Altitude:</strong> {satellite.position.altitude.toFixed(0)} km
                  </p>
                  <p style={{ margin: '5px 0' }}>
                    <strong>Velocity:</strong> {satellite.position.velocity.toFixed(2)} km/s
                  </p>
                </div>
              </Popup>
            </Marker>
          )
        })}
        
        <MapUpdater satellites={satellites} selectedSatellite={selectedSatellite} />
      </MapContainer>
    </div>
  )
}

export default Map
