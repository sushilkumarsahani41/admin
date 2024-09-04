from django.urls import path
from .views import get_district_and_state

urlpatterns = [
    path('pincode/<str:pincode>/', get_district_and_state, name='get_district_and_state'),
]
