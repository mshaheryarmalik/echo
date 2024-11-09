from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
import requests

# Create your views here.

API_KEY = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"

@csrf_exempt
def get_emad(request):
    """API view to handle the request for fetching map images."""
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            center_lat = data.get('latitude')
            center_lon = data.get('longitude')

            if not center_lat or not center_lon:
                return JsonResponse({'error': 'Missing latitude, longitude, or API key'}, status=400)
            
            images = fetch_images(center_lat, center_lon, API_KEY)
            
            data = {
                'status': 'success',
                'message': 'Data fetched successfully!',
                'data': {'count_images': len(images)}
                }
    
            return JsonResponse(data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)
    
def get_image_url(lat, lon, zoom, size, api_key):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}x{size}&maptype=satellite&key={api_key}"

def fetch_images(center_lat, center_lon, api_key):
    urls = []
    latitude_offset = 0.09  # Approximate offset in degrees for 10 km (latitude)
    longitude_offset = 0.09  # Approximate offset in degrees for 10 km (longitude)
    zoom = 13               # Adjusted for larger area coverage
    size = 200              # Size of each image tile in pixels

    for i in range(-1, 3):  # For 4x4 grid around center point
        for j in range(-1, 3):
            lat = center_lat + (i * latitude_offset)
            lon = center_lon + (j * longitude_offset)
            url = get_image_url(lat, lon, zoom, size, api_key)
            urls.append(url)

    images = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            images.append(response.content)  # Add image data to the list
        else:
            print(f"Failed to fetch image at {url}")

    return images

# Example usage
#api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"
#center_lat = 37.7749  # Replace with actual latitude from frontend
#center_lon = -122.4194  # Replace with actual longitude from frontend

#images = fetch_images(center_lat, center_lon, api_key)
#print(images[0])

# 'images' now contains the raw image data for each tile, which you can assemble into a 4x4 grid.

"""
from PIL import Image
import requests
from io import BytesIO

def get_image_url(lat, lon, zoom, size, api_key):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}x{size}&maptype=satellite&key={api_key}"

def fetch_images(center_lat, center_lon, api_key):
    urls = []
    latitude_offset = 0.09
    longitude_offset = 0.09
    zoom = 13
    size = 200
    
    for i in range(-1, 3):
        for j in range(-1, 3):
            lat = center_lat + (i * latitude_offset)
            lon = center_lon + (j * longitude_offset)
            url = get_image_url(lat, lon, zoom, size, api_key)
            urls.append(url)
    
    images = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            images.append(img)
        else:
            print(f"Failed to fetch image at {url}")
    
    return images

def create_grid(images, grid_size=4, tile_size=(200, 200)):
    grid_image = Image.new('RGB', (tile_size[0] * grid_size, tile_size[1] * grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            img = images[i * grid_size + j]
            img = img.resize(tile_size)  # Ensure each tile is the same size
            print(img)
            grid_image.paste(img, (j * tile_size[0], i * tile_size[1]))
    
    return grid_image

# Example usage
api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"
center_lat = 66.5078
center_lon = 25.7235

# Fetch and display images
images = fetch_images(center_lat, center_lon, api_key)
grid_image = create_grid(images)
grid_image.show()  # Opens the image in the default viewer

# Optionally, save the grid image
grid_image.save("map_grid.png")
"""

#api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"