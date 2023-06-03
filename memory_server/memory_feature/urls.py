from django.urls import path
from .views import MemoryCreateAPIView 

urlpatterns = [
    path('memories/', MemoryCreateAPIView.as_view(), name='memory_list_create'),
]
