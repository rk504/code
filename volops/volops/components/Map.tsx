'use client'

import { useState } from 'react'
import Map, { Marker, Popup } from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = 'YOUR_MAPBOX_TOKEN_HERE' // Replace with your actual Mapbox token

export default function MapComponent({ opportunities }) {
  const [popupInfo, setPopupInfo] = useState(null)

  return (
    <Map
      initialViewState={{
        latitude: 40.7128,
        longitude: -74.0060,
        zoom: 11
      }}
      style={{width: '100%', height: '100%'}}
      mapStyle="mapbox://styles/mapbox/streets-v11"
      mapboxAccessToken={MAPBOX_TOKEN}
    >
      {opportunities.map((opportunity) => (
        <Marker
          key={opportunity.id}
          latitude={opportunity.latitude}
          longitude={opportunity.longitude}
          onClick={e => {
            e.originalEvent.stopPropagation()
            setPopupInfo(opportunity)
          }}
        >
          <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
            {opportunity.id}
          </div>
        </Marker>
      ))}

      {popupInfo && (
        <Popup
          anchor="top"
          latitude={popupInfo.latitude}
          longitude={popupInfo.longitude}
          onClose={() => setPopupInfo(null)}
        >
          <div>
            <h3 className="font-semibold">{popupInfo.title}</h3>
            <p className="text-sm">{popupInfo.organization}</p>
          </div>
        </Popup>
      )}
    </Map>
  )
}

