import openai
from geopy.geocoders import Nominatim

# Set up your OpenAI API key
openai.api_key = "YOUR_API_KEY_HERE"

# Function to get geographic information from coordinates
def get_geographic_information(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude))
    return location.address if location else "Unknown Location"

# Input your latitude and longitude
latitude = 40.7128
longitude = -74.0060

# Get the geographic information
geographic_info = get_geographic_information(latitude, longitude)

# Define your prompt with the geographic information
prompt = f"""
Generate a comprehensive report based on the given satellite data. The data includes:
1. **Labels from the AID model**: [List of labels]
2. **Forest condition details**: [Details, including multiclass labels]
3. **Geographic area**: {geographic_info}

Considering the specific environmental and geographical characteristics of this area, the report should include:
- An overview of the labeled data
- A detailed analysis of forest conditions or environmental status
- Geographic or regional influences, such as local climate or ecosystem patterns
- Any critical trends, anomalies, or relevant environmental concerns
- Recommendations or insights tailored to this location

Use a structured format with headings and bullet points. The language should be clear, professional, and informative.
"""

# Request to the OpenAI API
response = openai.Completion.create(
    engine="text-davinci-003",  # Use "gpt-4" if you have access
    prompt=prompt,
    max_tokens=1000,  # Adjust based on the desired length of the report
    temperature=0.5   # Tweak for creativity vs. focus
)

# Print the generated report
report = response.choices[0].text
print(report)
