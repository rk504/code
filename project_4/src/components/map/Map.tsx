import { MapContainer, TileLayer } from 'react-leaflet';
import { useStore } from '../../store/useStore';
import { MapMarker } from './MapMarker';
import { useMapConfig } from './hooks/useMapConfig';
import 'leaflet/dist/leaflet.css';

export function Map() {
  const { opportunities, setSelectedOpportunity } = useStore();
  const { center, zoom, tileLayer } = useMapConfig();

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className="w-full h-full"
      zoomControl={false}
      attributionControl={false}
    >
      <TileLayer {...tileLayer} />
      {opportunities.map((opportunity) => (
        <MapMarker
          key={opportunity.id}
          opportunity={opportunity}
          onSelect={setSelectedOpportunity}
        />
      ))}
    </MapContainer>
  );
}