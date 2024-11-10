'use client';

import { useState, useCallback } from 'react';
import { useLoadScript, GoogleMap, Marker, Autocomplete } from '@react-google-maps/api';
import Button from "@/components/button_view";
import AudioRing from "@/components/ring_anim";

const center = { lat: 60.16, lng: 24.90 };
interface Pin {
  lat: number;
  lng: number;
}



interface MapsProps {
  onDataReceived: (data: any) => void;
}

const newPin = {}

const mapContainerStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  width: '80%',
  height: '500px',
  borderRadius: '8px'
};

const mapOptions = {
  mapTypeId: 'satellite',
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

export default function GoogleMapView({ onDataReceived }: MapsProps) {
  const [pin, setPin] = useState<Pin | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [searchBox, setSearchBox] = useState<google.maps.places.Autocomplete | null>(null);
  const [loading, setLoading] = useState<boolean>(false);


  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
    libraries: ['places']
  });

  const onLoadSearchBox = (ref: google.maps.places.Autocomplete) => {
    setSearchBox(ref);
  };

  const onPlaceSelected = () => {
    if (searchBox) {
      const place = searchBox.getPlace();
      if (place.geometry?.location) {
        const newPin = {
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng()
        };
        setPin(newPin);
        map?.panTo(newPin);
        map?.setZoom(15);
      }
    }
  };

  const handleButtonClick = async (id:number) => {
    try {
      setLoading(true);
      const response = await fetch('http://34.55.73.80:8080/echoapi/get_emad/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          latitude: pin?.lat,
          longitude: pin?.lng
         })
      });
      
      const data = await response.json();
      let rep = data.report;
      // onResp(data);
      setLoading(false);
      onDataReceived(rep);
      return rep;
    } catch (error) {
      console.error('Error:', error);
      setLoading(false);
      onDataReceived("Temp data");
      throw error;
    }
  }

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
    <div>
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 w-[300px]">
        {isLoaded && (
          <Autocomplete
            onLoad={onLoadSearchBox}
            onPlaceChanged={onPlaceSelected}
          >
            <input
              type="text"
              placeholder="Search location..."
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 
              focus:outline-none focus:ring-2 focus:ring-blue-500 
              placeholder-gray-400 shadow-lg"
              style={{
                backdropFilter: 'blur(4px)',
              }}
            />
          </Autocomplete>
        )}
      </div>
      <div className="mt-20 h-[500px] w-full flex items-center justify-center bg-gray-900/90 rounded-lg">
        <GoogleMap
          zoom={13}
          center={center}
          mapContainerStyle={mapContainerStyle}
          options={mapOptions}
          onClick={handleMapClick}
          onLoad={onLoad}>
          {pin && (
            <Marker
              position={pin}
            />
          )}
        </GoogleMap>
        {loading == true ? (
          <div className="mt-4 z-10 absolute">
            <AudioRing />
          </div>
        ): null}
      </div>
    
      <div>
        <Button onClick={handleButtonClick} />
      </div>
    </div>

  );
}

