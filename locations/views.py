from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_district_and_state(request, pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data[0]['Status'] == "Success":
            post_office_info = data[0]['PostOffice'][0]  # Assuming you want the first post office in the list
            district = post_office_info['District']
            state = post_office_info['State']
            return Response({'district': district, 'state': state}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Pincode'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Failed to fetch data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
