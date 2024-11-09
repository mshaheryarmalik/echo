import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_satellite_report(aid_labels, forest_conditions, location, provider="ollama", api_url=None):
    # Prepare the prompt dynamically
    prompt = f"""
    Data we will share in a list of 16 members, each member of the list will be about one frame.
    Generate a comprehensive report based on the given satellite data. The data includes:
    1. **Labels from the AID model**: {aid_labels}
    2. **Forest condition details**: {forest_conditions}
    3. **Geographic area**: {location}
    
    Considering the specific environmental and geographical characteristics of this area, the report should include:
    - An overview of the labeled data
    - A detailed analysis of forest conditions or environmental status
    - Geographic or regional influences, such as local climate or ecosystem patterns
    - Any critical trends, anomalies, or relevant environmental concerns
    - Recommendations or insights tailored to this location
    
    Use a structured format with headings and bullet points. The language should be clear, professional, and informative.
    """
    
    # Set up the request payload based on the provider
    if provider == "ollama":
        if api_url is None:
            api_url = "http://localhost:11434/v1/chat/completions"
        
        data = {
            "model": "llama3.2:3b",  # Adjust model name as needed for Ollama
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.5
        }
        
        # Send request to Ollama API
        response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        
    elif provider == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please add it to the .env file.")
        
        api_url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-3.5-turbo",  # Adjust model name as needed
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.5
        }
        
        # Send request to OpenAI API
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    else:
        raise ValueError("Invalid provider. Choose either 'ollama' or 'openai'.")
    
    # Check if the response was successful
    if response.status_code == 200:
        result = response.json()
        # Extract and return the generated report
        report = result["choices"][0]["message"]["content"]
        return report
    else:
        # Return error message if the request failed
        return f"Error {response.status_code}: {response.text}"

# Example usage:
aid_labels = ['Viaduct', 'Center', 'Park', 'Forest', 'School', 'River', 'RailwayStation', 'Square', 'Farmland', 'Church', 'Resort', 'BareLand', 'BaseballField', 'Industrial', 'Beach', 'Airport']
forest_conditions = [
    [('cloudy', 'haze', 'partly_cloudy', 'road', 'water')],
    [('agriculture', 'cloudy', 'habitation', 'haze', 'partly_cloudy', 'road', 'water')],
    # ... (add the rest of your data)
]
location = "Lahore"

# Generate report with OpenAI
report_openai = generate_satellite_report(aid_labels, forest_conditions, location, provider="openai")
print("OpenAI Report:\n", report_openai)
