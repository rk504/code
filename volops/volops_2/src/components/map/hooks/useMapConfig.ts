import { MapConfig } from '../types/map';

export function useMapConfig(): MapConfig {
  return {
    center: [40.7831, -73.9712], // NYC center (Manhattan)
    zoom: 12,
    tileLayer: {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    },
  };
}