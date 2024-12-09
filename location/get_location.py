import requests

def get_location_info():
    # Get IP-based location
    try:
        # Using ip-api.com for free geolocation based on IP
        ip_api_url = "http://ip-api.com/json/"
        response = requests.get(ip_api_url)
        location_data = response.json()

        if location_data['status'] == 'success':
            latitude = location_data['lat']
            longitude = location_data['lon']
            city = location_data.get('city', 'Unknown')
            region = location_data.get('regionName', 'Unknown')
            country = location_data.get('country', 'Unknown')

            print(f"Location based on IP: {city}, {region}, {country}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            
            # Get elevation using a public API
            elevation_api_url = f"https://api.open-elevation.com/api/v1/lookup"
            elevation_response = requests.post(elevation_api_url, json={"locations": [{"latitude": latitude, "longitude": longitude}]})
            elevation_data = elevation_response.json()

            if 'results' in elevation_data and elevation_data['results']:
                elevation = elevation_data['results'][0].get('elevation', 'Unknown')
                print(f"Elevation: {elevation} meters")
            else:
                print("Could not retrieve elevation.")
        else:
            print("Error fetching location data.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_location_info()
