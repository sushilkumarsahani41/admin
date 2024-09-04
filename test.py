import os
import json
import requests
from time import sleep

def fetch_and_store_location(pincode, output_data):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data[0]['Status'] == "Success" and data[0]['PostOffice']:
            post_office_info = data[0]['PostOffice'][0]
            district = post_office_info['District']
            state = post_office_info['State']
            
            # Store in the output_data dictionary
            output_data[pincode] = {
                'district': district,
                'state': state
            }
            print(f'Successfully fetched {district}, {state} ({pincode})')
        else:
            print(f'Invalid pincode or no data: {pincode}')
    else:
        print(f'Failed to fetch data for pincode: {pincode}')

def main():
    start_pincode = 110001
    end_pincode = 999999
    output_data = {}

    for pincode in range(start_pincode, end_pincode + 1):
        fetch_and_store_location(pincode, output_data)
        # sleep(0.1)  # To avoid overwhelming the server with requests, add a slight delay

    # Save the output_data dictionary to a JSON file
    with open('locations.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
        print('Data has been stored in locations.json')

if __name__ == "__main__":
    main()
