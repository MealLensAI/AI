import requests

def get_location():
    try:
        # Get IP address and location information using ipinfo.io
        response = requests.get('https://ipinfo.io/json')
        
        # Check if the response was successful
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        location_info = {
            'ip': data.get('ip'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'coordinates': data.get('loc', '').split(',')
        }
        
        return location_info
        
    except requests.RequestException as e:
        print(f"Error occurred while fetching location data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    location = get_location()
    if location:
        print(f"Location: {location['city']}, {location['region']}, {location['country']}")
