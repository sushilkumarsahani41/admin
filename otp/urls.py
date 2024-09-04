from django.urls import path
from .views import create_otp_transaction, verify_otp

urlpatterns = [
    path('send/', create_otp_transaction, name='create_otp_transaction'),
    path('verify/', verify_otp, name='verify_otp')
]
