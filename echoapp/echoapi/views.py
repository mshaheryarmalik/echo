from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def get_emad(request):
    """API view to handle the request for fetching map images."""
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            center_lat = data.get('latitude')
            center_lon = data.get('longitude')
            api_key = data.get('api_key')

            if not center_lat or not center_lon:
                return JsonResponse({'error': 'Missing latitude, longitude, or API key'}, status=400)
            
            data = {
                'status': 'success',
                'message': 'Data fetched successfully!',
                'data': {'key1': 'value1', 'key2': 'value2'}
                }
    
            return JsonResponse(data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)