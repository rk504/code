import React from 'react';
import { useStore } from '../../store/useStore';

export const MapContainer: React.FC = () => {
  const { opportunities } = useStore();
  
  return (
    <div className="w-full h-full bg-gray-200 relative">
      <div className="absolute inset-0 flex items-center justify-center">
        <p className="text-gray-600">Map Component (Replace with actual map implementation)</p>
      </div>
      {/* Add your map implementation here (e.g., Google Maps, Mapbox, etc.) */}
    </div>
  );
};