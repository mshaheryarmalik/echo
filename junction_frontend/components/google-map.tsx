'use client';

import { useLoadScript, GoogleMap } from '@react-google-maps/api';

const center = {
  lat: 60.1699,
  lng: 24.9384
};

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
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
  });

  if (!isLoaded) {
    return <div className="h-[500px] w-full flex items-center justify-center bg-gray-900/90 rounded-lg">Loading map...</div>;
  }

  return (
    <GoogleMap
      zoom={13}
      center={center}
      mapContainerStyle={mapContainerStyle}
      options={mapOptions}
    />
  );
}