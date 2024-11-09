'use client';

import { useState, useCallback } from 'react';
import { useLoadScript, GoogleMap, Marker } from '@react-google-maps/api';
const center = { lat: 37.7749, lng: -122.4194 };
interface Pin {
  lat: number;
  lng: number;
}

const mapContainerStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  width: '80%',
  height: '500px',
  borderRadius: '8px'
};

const mapOptions = {
  disableDefaultUI: true,
  zoomControl: true,
  styles: [
    {
      featureType: 'all',
      elementType: 'labels.text.fill',
      stylers: [{ color: '#6c7983' }]
    }
  ]
};

export default function GoogleMapView() {
  const [pin, setPin] = useState<Pin | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
  });

  const onLoad = useCallback((map: google.maps.Map) => {
    setMap(map);
  }, []);

  const handleMapClick = (e: google.maps.MapMouseEvent) => {
    if (e.latLng) {
      const newPin = {
        lat: e.latLng.lat(),
        lng: e.latLng.lng()
      };
      setPin(newPin);
      map?.panTo(newPin);
    }
  };

  if (!isLoaded) {
    return <div className="h-[500px] w-full flex items-center justify-center bg-gray-900/90 rounded-lg">Loading map...</div>;
  }

  return (
    <GoogleMap
      zoom={13}
      center={center}
      mapContainerStyle={mapContainerStyle}
      options={mapOptions}
      onClick={handleMapClick}
      onLoad={onLoad}
    >
      {pin && (
        <Marker
          position={pin}
        />
      )}
    </GoogleMap>
  );
}
