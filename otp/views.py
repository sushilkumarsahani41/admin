from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OTPTransaction
import secrets
import requests
from admin.decorator import api_key_required  # Import your custom decorator
import random

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


import requests

def send_sms(mobile, otp):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    params = {
        'authorization': '1KQz6nWiyG2SbrXLNcC0IeYuJOj4H3mPA9DFxUwBMtVZ7okhfdQFElGpzvuDmg1WHsOYxNUjXtrL3dZM',
        'route': 'dlt',
        'sender_id': 'GRTSHK',
        'message': 171744,
        'variables_values': f'{otp}|CK GOAT Farm|',
        'flash': '0',
        'numbers': mobile,
    }
    
    response = requests.get(url, params=params)
    
    return response

# Example usage



@api_view(['GET'])
@api_key_required  # No scope required
def create_otp_transaction(request):
    transaction_id = secrets.token_urlsafe(8)
    otp = generate_otp()
    mobile_no = request.GET.get('mobile_no')
    if not mobile_no:
        return Response({'error': 'mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
    print(otp)
    smsStatus = send_sms(mobile_no, otp)
    print(smsStatus.json())
    if smsStatus.status_code == 200: 
        otp_transaction = OTPTransaction(mobile_no=mobile_no, transaction_id=transaction_id, otp=otp)
        otp_transaction.save()
        data = {'transaction_id': transaction_id, 'mobile_no':mobile_no, 'status':"Send Successfully"}
        return Response(data, status=status.HTTP_201_CREATED)

    return Response({"error":"Message Not Sent", "code": 00})



@api_view(['GET'])
@api_key_required
def verify_otp(request):
    transaction_id = request.GET.get('transaction_id')
    otp = request.GET.get('otp')

    if not transaction_id or not otp:
        return Response({'error': 'transaction_id and otp are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the OTP transaction from the database
        otp_transaction = OTPTransaction.objects.get(transaction_id=transaction_id)
    except OTPTransaction.DoesNotExist:
        return Response({'error': 'Invalid transaction_id'}, status=status.HTTP_404_NOT_FOUND)

    # Compare the provided OTP with the one stored in the database
    if otp_transaction.otp == otp:
        # OTP is correct
        return Response({'code': 1,'status': 'OTP verified successfully'}, status=status.HTTP_200_OK)
    else:
        # OTP is incorrect
        return Response({'code': 0,'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)